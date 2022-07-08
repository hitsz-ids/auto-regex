from opendlp.regex_generation.config import conf
from opendlp.regex_generation.dataset import Dataset
from opendlp.regex_generation.bpe import learn_bpe
from opendlp.regex_generation.node_factory import NodeFactory
from opendlp.regex_generation.generations.random_generate import RandomGenerator
from opendlp.regex_generation.fitness.objective import Objective
from opendlp.regex_generation.fitness.fitness import Fitness
from opendlp.regex_generation.config.evolve_param import EvolveParam
from opendlp.regex_generation.evolution.evolve import evolve


def get_fitness_rank(population, objective):
    population_fitness = []
    for tree in population:
        fitness_arr = objective.cal_fitness(tree)
        population_fitness.append(Fitness(tree, fitness_arr))
    fitness_rank = sorted(population_fitness, reverse=True)
    return fitness_rank

def get_best_fitness_precison(fitness_sorted):
    """
    get best fitness with best sample precision in a sorted fitness arrat
    @param fitness_rank:
    @return:
    """
    best_fitness = fitness_sorted[0]
    for fit in fitness_sorted:
        if fit.fitness >= best_fitness.fitness and \
            fit.fitness_arr[0] > best_fitness.fitness_arr[0]:
            best_fitness = fit
        else:
            break
    return best_fitness


def generate(status, regex_name, train_data_file):
    # status先不处理，后续再处理

    # 创建数据集
    dataset = Dataset(train_data_file)
    dataset.build()
    ori_pos_sample_num = len(dataset.pos_examples)

    # 学习bpe token
    percent = conf.BPE_PERCENT
    bpe_tokens = learn_bpe(dataset.pos_examples(), percent)

    # 构建terminalSet和functionSet
    node_facto = NodeFactory()
    node_facto.build(bpe_tokens)    # 默认的terminalSet和functionSet初始化

    # 初始化种群
    max_depth = conf.MAX_DEPTH
    population_size = conf.POPULATION_SIZE
    # 暂时仅随机生成，没有用到数据集，后续考虑初始化时如何使用数据集
    rand_generator = RandomGenerator(max_depth, node_facto)
    population = rand_generator.generate(population_size)

    # 计算种群的适应度值
    objective = Objective(dataset)
    fitness_sorted = get_fitness_rank(population, objective)

    # 演化
    result_fitness = set()
    evolve_param = EvolveParam()
    iter_best = 0
    for g in range(conf.MAX_ITERATIONS):
        population = evolve(evolve_param, population, fitness_sorted)
        fitness_sorted = get_fitness_rank(population, objective)

        best_fitness = get_best_fitness_precison(fitness_sorted)
        best_precision = best_fitness.fitness_arr[0]
        iter_best += 1
        if best_precision >= conf.PRECISION_DIVIDE_CONQUER \
                and iter_best >= conf.ITERATION_DIVIDE_CONQUER:
            result_fitness.add(best_fitness)
            dataset.remove_by_regex(best_fitness.tree)
            if len(dataset.pos_examples) < ori_pos_sample_num * conf.NOISE_POSITIVE_SAMPLE_RATIO:
                break
            population = rand_generator.generate(population_size)
            iter_best = 0

    # 输出结果
    result_regexes = []
    for i, fitness in enumerate(result_fitness):
        sub_regex_string = ''
        fitness.tree.form(sub_regex_string, conf.RegexFlavour.Python)
        print('sub_regex_{}: {}'.format(i, sub_regex_string))
        result_regexes.append(sub_regex_string)

    regex_string = '|'.join(result_regexes)
    print('{}: {}'.format(regex_name, regex_string))

    #TODO: 计算regex_string的fitness值。待fitness模块实现相关函数后再添加。
    fitness_value = 0

    result = {'regex_name': regex_name,
              'regex_string': regex_string,
              'fitness': fitness_value}

    return status, result




