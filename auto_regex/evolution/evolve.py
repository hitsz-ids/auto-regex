import random

class Evolution:
    def __init__(self, evolve_param, selection, variation, random_popu_gen):
        self.param = evolve_param
        self.selection = selection
        self.variation = variation
        self.random_popu_gen = random_popu_gen

    def evolve(self, old_pop_size, fitness_ranked):
        """
        evolve
        @param old_pop_size:
        @param fitness_ranked:
        @return: new_population
        """
        new_population = []
        new_pop_size = max(self.param.population_size_decay_rate * old_pop_size,
                           self.param.min_population_size)
        while len(new_population) < int(new_pop_size * 0.9):
            rand = random.random()
            if rand <= self.param.crossover_proba:
                tree1 = self.selection.select(fitness_ranked)
                tree2 = self.selection.select(fitness_ranked)
                new_tree1, new_tree2 = self.variation.crossover(tree1, tree2, self.param.variation_tries)
                if new_tree1 is not None:
                    new_population.append(new_tree1)
                    new_population.append(new_tree2)
                else:
                    new_population.append(tree1)
                    new_population.append(tree2)
            elif rand <= self.param.crossover_proba + self.param.mutation_proba:
                tree = self.selection.select(fitness_ranked)
                new_tree = self.variation.mutate(tree, self.param.variation_tries)
                if new_tree is not None:
                    new_population.append(new_tree)
                else:
                    new_population.append(tree)
            else:
                tree = self.selection.select(fitness_ranked)
                new_population.append(tree)

        size = new_pop_size - len(new_population)
        trees = self.random_popu_gen.growth_generate(size)
        new_population.extend(trees)

        return new_population