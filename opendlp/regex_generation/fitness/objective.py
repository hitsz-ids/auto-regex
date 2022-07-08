
class Objective:
    def __init__(self, dataset):
        raise NotImplementedError

    def cal_fitness(self, tree):
        """
        calculate fitness of a regex tree
        @param tree: a regex tree
        @return: fitness array with three value:[Ps, Pc, Lscore]
        """
        raise NotImplementedError
