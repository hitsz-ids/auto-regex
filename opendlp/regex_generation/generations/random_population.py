import random


class RandomPopulationGenerator:
    def __init__(self, max_depth, node_factory):
        self.max_depth = max_depth
        self.node_factory = node_factory

    def generate(self, population_size):
        population = []
        pop_size_full = population_size // 2
        pop_size_growth = population_size - pop_size_full
        population.extend(self.growth_generate(pop_size_full))
        population.extend(self.fixed_generate(pop_size_growth))
        return population

    def growth_generate(self, population_size):
        """
        generate regex trees with growth depth.
        @param population_size: tree nums to be generate
        @return:
        """
        population = []
        i = 0
        while i < population_size:
            candidate = self.build(1, growth=True)
            if candidate.is_valid():
                population.append(candidate)
                i += 1
        return population

    def fixed_generate(self, population_size):
        """
        generate regex trees with fixed depth.
        @param population_size: tree nums to be generate
        @return:
        """
        population = []
        i = 0
        while i < population_size:
            candidate = self.build(1, growth=False)
            if candidate.is_valid():
                population.append(candidate)
                i += 1
        return population

    def build(self, depth, growth):
        tree = random.choice(self.node_factory.function_set).clone_tree()
        if depth>=self.max_depth-1:
            for i in range(tree.get_max_children_count() - tree.get_min_children_count(),
                           tree.get_max_children_count()):
                leaf = random.choice(self.node_factory.terminal_set).clone_tree()
                leaf.parent = tree
                tree.children.append(leaf)
        else:
            if growth:
                for i in range(tree.get_max_children_count() - tree.get_min_children_count(),
                               tree.get_max_children_count()):
                    if random.choice([True, False]):
                        leaf = random.choice(self.node_factory.terminal_set).clone_tree()
                        leaf.parent = tree
                        tree.children.append(leaf)
                    else:
                        node = self.build(depth+1, growth)
                        node.parent = tree
                        tree.children.append(node)
            else:
                for i in range(tree.get_max_children_count() - tree.get_min_children_count(),
                               tree.get_max_children_count()):
                    node = self.build(depth+1, growth)
                    node.parent = tree
                    tree.children.append(node)
        return tree
