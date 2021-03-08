from random import randint, random, sample
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


def convert(individual):
    sign = individual[0]
    value = individual[1:5]
    decimal = individual[5:11]
    d_individual = int(''.join(map(str, value)), 2)
    decimal_value = int(''.join(map(str, decimal)), 2) / 64
    d_value = d_individual + decimal_value
    if sign == 1:
        d_value = -d_value
    return d_value


def fitness(individual, target):
    """
    Determine the fitness of an individual. Higher is better.

    d_value: decimal value of individual
    polynomal: fitness function to be evaulated
    target: the target number individuals are aiming for

    """
    d_value = convert(individual)
    polynomial = 25 * d_value ** 5 + 18 * d_value ** 4 + 31 * d_value ** 3 - 14 * d_value ** 2 + 7 * d_value - 19
    return abs(target - polynomial)


def grade(pop, target):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x, target) for x in pop))
    return summed / (len(pop) * 1.0)


def evolve(pop, target, retain=0.35, random_select=0.05, mutate=0.01):
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
plot_range = range(-100, 100)
plot_values = sample(plot_range, 100)
targets = sorted(plot_values)
p_count = 200
i_length = 11
i_min = 0
i_max = 1
generations = 150
final_value = []

for j in targets:
    p = population(p_count, i_length, i_min, i_max)
    for i in range(generations):
        p = evolve(p, j)
        grade_p = grade(p, j)
        if grade_p < 2 or i == generations-1:
            final_value.append(convert(p[0]))
            break

print(final_value)

# plot final values against target values.
plt.plot(final_value, targets)
plt.show()
