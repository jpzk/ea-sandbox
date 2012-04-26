#!/bin/env python
# encoding utf-8

''' 
This file is part of evolutionary-algorithms-sandbox.

evolutionary-algorithms-sandbox is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

evolutionary-algorithms-sandbox is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along with
evolutionary-algorithms-sandbox.  If not, see <http://www.gnu.org/licenses/>.
'''

from random import * 
from sklearn import svm
from numpy import array
from collections import deque # used for sliding window of individuals

import math

'''
mu+lambda EA with rechenberg-sigma gauss mutation for minimizing
sum(map(lambda x : pow(x,2), x)) with tangent constraint 
sum(x) - 2.0 >= 0 for each valid solution. 

def run(dimensions, size, m, l, alpha, sigma):
    dimensions: R^dimensions
    size: values of [-size, size] possible
    m: mu, size of population, amount of parents
    l: amount of generated children
    alpha: factor of rechenberg
    sigma: start sigma for rechenberg

Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
'''

class TestEnvironment:
    """ TestEnvironment is used for measuring function calls. """

    _count_is_feasible = 0
    _count_fitness = 0
    _sum_wrong_class = 0

    def print_statistics(self):
        print("constraint function calls: " + str(self._count_is_feasible))
        print("fitness function calls: " + str(self._count_fitness))

    # return true if solution is valid, otherwise false.
    def is_feasible(self, x):
        self._count_is_feasible += 1
        return sum(x) - 2.0 >= 0

    # return fitness, 0 is best.
    def fitness(self, x):
        self._count_fitness = self._count_fitness + 1
        return sum(map(lambda x : pow(x,2), x)) 

    # return combined child of parents x,y
    def combine(self, pair): 
        return map(lambda i,j : (i+j)/2.0, pair[0], pair[1]) 

    # mutate child with gauss devriation 
    def mutate(self, child, sigma):
        return map(lambda value : value + gauss(0, sigma), child)

    # return sorted (best, smallest, first) list of parents
    def sortedbest(self, children):
        return sorted(children, key=lambda child : self.fitness(child))

    # return new sigma (rechenberg)
    def rechenberg(self, old_sigma, success_probability, alpha):
        if success_probability > 1.0/5.0: return old_sigma / alpha
        if success_probability < 1.0/5.0: return old_sigma * alpha
        return sigma

    # return success_probabilty (rechenberg)
    def success_probability(self, children, success_fitness):
        return len(filter(
            lambda child: self.fitness(child) <= success_fitness, 
            children)) / len(children)

    # python generator for inifinte list of parent population
    def generate_population(self, d, size):
         while(True):
            parent = map(lambda x : ((x * random()) - 0.5) * size *2,
                [1] * d)
            yield(parent)            

    # python generator for infinite list of feasible and infeasible 
    # children. mutated and recombined with given parents.
    def generate_children(self, parents, sigma):
        while(True):
            child = self.mutate(self.combine(sample(parents,2)), sigma)
            yield child

    # main evolution 
    def _run(self, (population, generation, m, l, lastfitness,\
        alpha, sigma)):

        # generate l-children union with parents, 
        # take the m best.
        childgen = self.generate_children(population, sigma)
        children = [childgen.next() for child in range(0,l)]

        feasible_children = []
        for child in children:
            if(self.is_feasible(child)):
                feasible_children.append(child)
        
        next_population =\
            self.sortedbest(population + feasible_children)[:m]
  
        fitness_of_best = self.fitness(next_population[0])
        fitness_of_worst = self.fitness(\
            next_population[len(next_population)-1])

        # only for visual output purpose.
        print "generation " + str(generation) +\
        " smallest fitness " + str(fitness_of_best) 

        # update sigma according to rechenberg.
#        new_sigma = self.rechenberg(
#            sigma, 
#            self.success_probability(feasible_children, lastfitness),
#            alpha)

        new_sigma = sigma
    
        if(2 - 1 * pow(10, -2) < fitness_of_best < 2 + 1 * pow(10, -2)):
            print next_population[0]
            return True
        else:
            return (next_population, generation + 1, m,\
            l, fitness_of_best, alpha, new_sigma)

    def run(self, dimensions, size, m, l, alpha, sigma):
        # create random population d-dimensional 
        # in interval [-s, s] but valid!
        
        genpop = self.generate_population(dimensions, size)   
        population = [genpop.next() for x in range(0, m)]
        
        # check for feasiblity and initialize sliding feasible and 
        # infeasible populations.

        feasible_parents = []
        for parent in population: 
            if(self.is_feasible(parent)):
                feasible_parents.append(parent)

        result = self._run((feasible_parents, 0, m, l, 0, alpha, sigma))

        while result != True:
            result = self._run(result)

        return result

env = TestEnvironment()
env.run(2, 10, 15, 100, 0.5, 1)
env.print_statistics()
