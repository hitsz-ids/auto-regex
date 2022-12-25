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
        p, r = self.__fitness_arr[0], self.__fitness_arr[1]
        f1 = 2*p*r/(p+r) if p+r != 0 else 0
        return 0.7*f1 + 0.2*self.__fitness_arr[2] + 0.1*self.__fitness_arr[3]

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

