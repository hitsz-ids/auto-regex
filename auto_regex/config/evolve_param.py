

class EvolutionParam:
    def __init__(self, population_size_decay_rate, min_population_size):

        self.population_size_decay_rate = population_size_decay_rate
        self.min_population_size = min_population_size

        self.crossover_proba = 0.8
        self.mutation_proba = 0.1

        self.pick_node_proba = 0.9
        self.pick_leaf_proba = 0.1

        self.variation_tries = 20





