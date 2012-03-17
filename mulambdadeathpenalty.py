#!/usr/bin/python
# encoding: utf-8

from random import * 

'''
mu+lambda EA with rechenberg-sigma gauss mutation for minimizing
sum(map(lambda x : pow(x,2), x)) with tangent restriction
sum(x) - 2.0 >= 0 for each valid solution.

generate_valid_population is a python generator, which generates
only valid, defined by is_valid function, population (random
solutions)

generate_valid_children is a python generator, which generates
only valid, defined by is_valid function, children. 

def run(dimensions, size, m, l, alpha, sigma):
    dimensions: R^dimensions
    size: values of [-size, size] possible
    m: mu, size of population, amount of parents
    l: amount of generated children
    alpha: factor of rechenberg
    sigma: start sigma for rechenberg

Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
'''

# return true if solution is valid, otherwise false.
def is_valid(x):
    return sum(x) - 2.0 >= 0

# return fitness, 0 is best.
def fitness(x):
    return sum(map(lambda x : pow(x,2), x)) 

# return combined child of parents x,y
def combine(pair): 
    return map(lambda i,j : (i+j)/2.0, pair[0], pair[1]) 

# mutate child with gauss devriation 
def mutate(child, sigma):
    return map(lambda value : value + gauss(0, sigma), child)

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

# python generator for inifinte list of valid parent population
def generate_valid_population(d, size):
    while(True):
        parent = map(lambda x : ((x * random()) - 0.5) * size *2,
            [1] * d)
        if(is_valid(parent)):
            yield(parent)            

# python generator for infinite list of valid children with 
# mutated and recombined with given parents.
def generate_valid_children(parents, sigma):
    while(True):
        child = mutate(combine(sample(parents,2)),
            sigma)
        if(is_valid(child)):
            yield child

# main evolution 
def _run((population, generation, m, l, lastfitness,\
    alpha, sigma)):

    # generate l-children union with parents, 
    # take the m best.
    childgen = generate_valid_children(population, sigma)
    children = [childgen.next() for child in range(0,l)]

    next_population = sortedbest(population + children)[:m]
   
    fitness_of_best = fitness(next_population[0])
    fitness_of_worst = fitness(next_population[m-1])

    # only for visual output purpose.
    print "generation " + str(generation) +\
        " biggest fitness " + str(fitness_of_worst) +\
        " smallest fitness " + str(fitness_of_best)

    # update sigma according to rechenberg.
    new_sigma = rechenberg(
        sigma, 
        success_probability(children, lastfitness),
        alpha)

    if(2-1*pow(10,-3) < fitness_of_best < 2+1*pow(10,-3)):
        print next_population[0]
        return True
    else:
        return (next_population, generation + 1, m,\
        l, fitness_of_best, alpha, new_sigma)

def run(dimensions,size,m,l,alpha,sigma):
    # create random population d-dimensional 
    # in interval [-s, s] but valid!
    genpop = generate_valid_population(dimensions, size)   
    result = _run(
        ([genpop.next() for x in range(0,m)],
        0, m, l, 0, alpha, sigma))

    while result != True:
        result = _run(result)

    return result

print run(2,10,15,100,0.5, 1)
