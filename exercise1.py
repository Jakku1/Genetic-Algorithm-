from random import randint, random
from operator import add
from functools import reduce
import matplotlib.pyplot as plt


def individual(length, min, max):
    'Create a member of the population.'
    return [randint(min, max) for x in range(length)]


def population(count, length, min, max):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values

    """
    return [individual(length, min, max) for x in range(count)]


def fitness(individual, target):
    """
    Determine the fitness of an individual. numbers use sign and magnitude.

    individual: the individual to evaluate
    sign: first bit which represents the sign
    value: following 8 bits which represent the magnitude
    d_individual: the decimal value of the binary number, used for comparison with the target
    target: the target number individuals are aiming for
    """
    # sum = reduce(add, individual, 0)
    sign = individual[0]
    value = individual[1:9]
    # b_individual = bin(int(''.join(map(str, individual)), 2) << 1)
    d_individual = int(''.join(map(str, value)), 2)
    if sign == 1:
        d_individual = -d_individual
    # d_individual = int(b_individual, 2)
    fitness_value = abs(target - d_individual)
    return fitness_value


def grade(pop, target):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x, target) for x in pop))
    return summed / (len(pop) * 1.0)


def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [(fitness(x, target), x) for x in pop]
    graded = [x[1] for x in sorted(graded)]
    retain_length = int(len(graded) * retain)
    parents = graded[:retain_length]
    # randomly add other individuals to
    # promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)
    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual) - 1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = randint(
                0, 1)
    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = int(len(male) / 2)
            child = male[:half] + female[half:]
            children.append(child)
    parents.extend(children)
    return parents


# Example Usage
target = 120 # randint(0, 255)
p_count = 100
i_length = 9
i_min = 0
i_max = 1
generations = 25
p = population(p_count, i_length, i_min, i_max)
fitness_history = [grade(p, target)]
for i in range(generations):
    p = evolve(p, target)
    grade_p = grade(p, target)
    fitness_history.append(grade_p)
    print(p)
    #if abs(grade_p) < abs(0.01 * target):
     #   break

for datum in fitness_history:
    print(datum)

plt.plot(fitness_history)
plt.show()
