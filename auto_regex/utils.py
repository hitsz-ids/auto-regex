from auto_regex.fitness.fitness import Fitness
import re

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


def match_count(examples, pattern):
    count = 0
    flags = re.DOTALL | re.MULTILINE
    for i in range(len(examples)):
        example = examples[i]
        matches = re.finditer(pattern, example, flags=flags)
        for match in matches:
            if match.span()[1] - match.span()[0] == len(example):
                count += 1

    return count

def get_final_metric(pos_examples, neg_examples, pattern):
    pos_count = match_count(pos_examples, pattern)
    neg_count = match_count(neg_examples, pattern)

    precision, recall = 0, 0
    if pos_count + neg_count != 0:
        precision = pos_count / (pos_count + neg_count)
    if len(pos_examples) != 0:
        recall = pos_count / len(pos_examples)

    return precision, recall