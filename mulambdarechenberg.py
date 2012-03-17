#!/usr/bin/python
# encoding: utf-8

from random import * 
from itertools import *

'''
mu+lambda EA with rechenberg-sigma gauss mutation,

def run(dimensions, size, m, l, alpha, sigma):
    dimensions: R^dimensions
    size: values of [-size, size] possible
    m: mu, size of population, amount of parents
    l: amount of generated children
    alpha: factor of rechenberg
    sigma: start sigma for rechenberg

Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
'''

# return fitness, 0 is best.
def fitness(x):
    return sum(map(lambda x : pow(x,2), x)) 

# return combined child of parents x,y
def combine(pair): 
    return map(lambda i,j : (i+j)/2.0, pair[0], pair[1]) 

# create a list in d length and in interval [-size, size]
def create(d, size): 
    return map(
        lambda x : ((x * random()) - 0.5) * size * 2,
        [1] * d)

# mutate child with gauss devriation 
def mutate(child, sigma):
    return map(lambda value : value + gauss(0, sigma), child)

# return all combination of parents
def shuffled_parent_pairs(parents): 
    return sorted(
        [x for x in combinations(parents,2)],
        key=lambda i : random())

# return sorted (best, smallest, first) list of parents
def sortedbest(children):
    return sorted(children, key=lambda child : fitness(child))

# return new sigma (rechenberg)
def rechenberg(old_sigma, success_probability, alpha):
    if success_probability > 1.0/5.0: return old_sigma / alpha
    if success_probability < 1.0/5.0: return old_sigma * alpha
    return sigma

# return success_probabilty (rechenberg)
def success_probability(children, success_fitness):
    return len(filter(
        lambda child: fitness(child) <= success_fitness, 
        children)) / len(children)

# return l children combined with combine function, 
# and mutated with mutate function.
def generate_children(parents, l, sigma):
    return map(mutate, 
        map(combine, shuffled_parent_pairs(parents))[:l],
        [sigma] * l)

# main evolution 
def _run((population, generation, m, l, lastfitness,\
    alpha, sigma)):

    # generate l-children union with parents, 
    # take the m best.
    children = generate_children(population, l, sigma)
    next_population = sortedbest(population + children)[:m]
   
    fitness_of_best = fitness(next_population[0])
    fitness_of_worst = fitness(next_population[m-1])

    # only for visual output purpose.
    print "generation " + str(generation) +\
        " worst fitness " + str(fitness_of_worst) +\
        " best fitness " + str(fitness_of_best)

    # update sigma according to rechenberg.
    new_sigma = rechenberg(
        sigma, 
        success_probability(children, lastfitness),
        alpha)

    if(-1*pow(10,-10) < fitness_of_best < pow(10,-10)):
        print next_population[0]
        return True
    else:
        return (next_population, generation + 1, m,\
        l, fitness_of_best, alpha, new_sigma)

def run(dimensions,size,m,l,alpha,sigma):
    # create random population d-dimensional 
    # in interval [-s, s]
    result = _run(
        ([create(dimensions,size) for x in range(0,m)],
        0, m, l, 0, alpha, sigma))

    while result != True:
        result = _run(result)

    return result

print run(3,10,15,100,0.5, 1)
