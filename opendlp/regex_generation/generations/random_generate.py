
from opendlp.regex_generation.generations.full import Full
from opendlp.regex_generation.generations.growth import Growth

class RandomGenerator:
    def __init__(self, max_depth, node_factory):
        self.full = Full(max_depth, node_factory)
        self.growth = Growth(max_depth, node_factory)

    def generate(self, population_size):
        population = []
        pop_size_full = population_size // 2
        pop_size_growth = population_size - pop_size_full
        population.append(self.full.generate(pop_size_full))
        population.append(self.growth.generate(pop_size_growth))