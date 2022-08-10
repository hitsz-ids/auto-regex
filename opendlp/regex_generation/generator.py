from opendlp.regex_generation.config import conf
from opendlp.regex_generation.dataset import Dataset
from opendlp.regex_generation.bpe import learn_bpe
from opendlp.regex_generation.node_factory import NodeFactory
from opendlp.regex_generation.generations import DatasetPopulationGenerator
from opendlp.regex_generation.generations import RandomPopulationGenerator
from opendlp.regex_generation.generations import PopulationInitializer
from opendlp.regex_generation.fitness.objective import Objective
from opendlp.regex_generation.config.evolve_param import EvolutionParam
from opendlp.regex_generation.evolution import Evolution, Selection, Variation
from opendlp.regex_generation.utils import get_fitness_rank, get_best_fitness_precison


def generate(regex_name,
             train_data_file,
             init_population_size=1000,
             max_iterations=2000,
             precision_divide_conquer=0.8,
             iteration_divide_conquer=30,
             noise_positive_sample_ratio=0.05,
             population_size_decay_rate=0.95,
             min_population_size=200):
    """生成正则表达式

    Args:
        regex_name: 生成的正则表达式的名称
        train_data_file: 用于生成正则表达式的训练数据，有两列，列名分布为"positive"和"negative"，表示正、负样本
        init_population_size: 初始正则表达式种群大小
        max_iterations: 最大迭代次数
        precision_divide_conquer: 子正则表达式的最小精确率阈值
        iteration_divide_conquer: 子正则表达式的最小迭代次数阈值
        noise_positive_sample_ratio: 噪声正样本比例，即允许生成的正则表达式无法匹配少量噪声正样本
        population_size_decay_rate: 正则表达式种群大小衰减参数
        min_population_size: 最小正则表达式种群大小，达到该大小后不再衰减

    Returns:
        生成的正则表达式结果字典，
        形式为{"regex_name": str, "regex_pattern": str}。
    """

    # 创建数据集
    dataset = Dataset(train_data_file)
    dataset.build()
    ori_pos_sample_num = len(dataset.pos_examples)

    # 学习bpe token
    pair_percent = conf.BPE_PAIR_PERCENT_THRESHOLD
    char_percent = conf.BPE_CHAR_PERCENT_THRESHOLD
    bpe_token_dict = learn_bpe(dataset.pos_examples, pair_percent, char_percent, dataset.is_fixed_length)

    # 构建terminalSet和functionSet
    node_facto = NodeFactory()
    node_facto.build()    # 默认的terminalSet和functionSet初始化

    ### 初始化种群
    dataset_popu_gen = DatasetPopulationGenerator(dataset, bpe_token_dict)
    random_popu_gen = RandomPopulationGenerator(conf.MAX_DEPTH, node_facto)
    popu_initializer = PopulationInitializer(dataset_popu_gen, random_popu_gen)
    population = popu_initializer.initlize(init_population_size)

    # 演化
    objective = Objective(dataset)
    result_fitness = []
    evolve_param = EvolutionParam(population_size_decay_rate, min_population_size)
    selection = Selection()
    variation = Variation(evolve_param, bpe_token_dict, random_popu_gen)
    evolution = Evolution(evolve_param, selection, variation, random_popu_gen)
    iter_best = 0
    for g in range(max_iterations):
        fitness_ranked = get_fitness_rank(population, objective)
        best_fitness = get_best_fitness_precison(fitness_ranked)
        print('{}\t generation: {}\t best: {}\t '.format(regex_name, g,
                                                         best_fitness.tree.form('')))

        best_precision = best_fitness.fitness_arr[0]
        iter_best += 1
        if best_precision >= precision_divide_conquer \
                and iter_best >= iteration_divide_conquer:
            result_fitness.append(best_fitness)
            dataset.remove_by_regex(best_fitness.tree)
            if len(dataset.pos_examples) < ori_pos_sample_num * noise_positive_sample_ratio:
                break
            population = popu_initializer.initlize(len(population))
            iter_best = 0
        else:
            population = evolution.evolve(len(population), fitness_ranked)

    # 输出结果
    result_regexes = []
    for i, fitness in enumerate(result_fitness):
        sub_regex_string = fitness.tree.form('', conf.RegexFlavour.Python)
        print('sub_regex_{}: {}'.format(i, sub_regex_string))
        result_regexes.append(sub_regex_string)

    regex_string = '|'.join(result_regexes)
    print('{}: {}'.format(regex_name, regex_string))

    result = {'regex_name': regex_name,
              'regex_pattern': regex_string}

    return result





if __name__ == '__main__':
    import os
    import pandas as pd

    data_dir = '../../tests/data/regex_generation/test-data/'
    regex_names = ['ID_CARD', 'TELEPHONE', 'MOBILE_PHONE', 'EMAIL', 'LICENSE_PLATE',
                   'BANK_CARD', 'PASSPORT', 'SOCIAL_CREDIT_CODE', 'IPV4', 'IPV6', 'MAC',
                   'DOMAIN_NAME', 'POSTCODE', 'DATE']
    result_dict = {'regex_name': [], 'regex_pattern':[]}
    for regex_name in regex_names:
        train_data_file = os.path.join(data_dir, regex_name + '.csv')
        result = generate(regex_name, train_data_file)
        print('result: ', result)
        print('\n')

        result_dict['regex_name'].append(result['regex_name'])
        result_dict['regex_pattern'].append(result['regex_pattern'])

    df = pd.DataFrame(result_dict)
    df.to_csv('result.csv', index=False)

