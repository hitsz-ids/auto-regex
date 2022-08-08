from opendlp.regex_generation.fitness.fitness import Fitness


# 对特殊字符转义
def escape(string):
    quotes = {'\\', '^',  '$', '*', '+', '?', '.', '[', ']', '(', ')', '{', '}', '|', '-'}
    new_string = ''
    for c in string:
        c = '\\'+c if c in quotes else c
        new_string += c
    return new_string

def get_fitness_rank(population, objective):
    population_fitness = []
    for tree in population:
        fitness_arr = objective.cal_fitness(tree)
        population_fitness.append(Fitness(tree, fitness_arr))
    fitness_rank = sorted(population_fitness, reverse=True)
    return fitness_rank

def get_best_fitness_precison(fitness_ranked):
    """
    get best fitness with best sample precision in a sorted fitness array
    @param fitness_rank:
    @return:
    """
    best_fitness = fitness_ranked[0]
    for fit in fitness_ranked:
        if fit.fitness >= best_fitness.fitness and \
            fit.fitness_arr[0] > best_fitness.fitness_arr[0]:
            best_fitness = fit
        else:
            break
    return best_fitness