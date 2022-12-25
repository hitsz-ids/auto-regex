import random

class Selection:
    def select(self, fitness_ranked):
        '''
        select an individual from ranked fitness array
        @param fitness_ranked: 排好序的适应度列表
        @return:
        '''
        idxs = random.choices(range(len(fitness_ranked)), k=7)
        best = min(idxs)
        return fitness_ranked[best].tree