from functools import total_ordering

@total_ordering
class Fitness:
    def __init__(self, tree, fitness_arr):
        self.__tree = tree
        self.__fitness_arr = fitness_arr

    @property
    def tree(self):
        return self.__tree

    @property
    def fitness_arr(self):
        return self.__fitness_arr

    @property
    def fitness(self):
        return sum(self.__fitness_arr)

    def __eq__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

