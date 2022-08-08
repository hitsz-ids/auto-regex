from opendlp.regex_generation.config import conf

class PopulationInitializer:
    def __init__(self, dataset_popu_gen, random_popu_gen):
        self.dataset_popu_gen = dataset_popu_gen
        self.random_popu_gen = random_popu_gen

    def initlize(self, population_size):
        # 根据数据集初始化
        population = self.dataset_popu_gen.generate(population_size)

        # 随机生成
        random_size = population_size - len(population)
        if random_size > 0:
            random_population = self.random_popu_gen.generate(random_size)
            population.extend(random_population)

        return population