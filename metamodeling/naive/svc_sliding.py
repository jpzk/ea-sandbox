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

from math import floor
from collections import deque # used for sliding window of individuals
from svc_evolution_strategy import SVCEvolutionStrategy

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

class SVCSliding(SVCEvolutionStrategy):
    
    _sliding_feasibles = deque(maxlen = 50) 
    _sliding_infeasibles = deque(maxlen = 50)

    # main evolution 
    def _run(self, (population, generation, m, l, lastfitness,\
        alpha, sigma)):
        
        self._count_generations += 1

        # generate l-children union with parents, 
        # take the m best.
        childgen = self.generate_children(population, sigma)
        children = [childgen.next() for child in range(0,l)]

        # Filter by checking feasiblity with SVC meta model        
        meta_feasible_children = filter(self.is_meta_feasible, children)

        # Filter by true feasibility with constraind function, here we
        # can update the sliding feasibles and infeasibles.
        feasible_children = []
        
        for meta_feasible in meta_feasible_children: 
            if(self.is_feasible(meta_feasible)):
                feasible_children.append(meta_feasible)               
                self._sliding_feasibles.append(meta_feasible)
            else:
                self._sum_wrong_class += 1
                self._sliding_infeasibles.append(meta_feasible)

        self.train_metamodel(\
            self._sliding_feasibles,
            self._sliding_infeasibles)

        next_population =\
            self.sortedbest(population + feasible_children)[:m]
  
        fitness_of_best = self.fitness(next_population[0])
        fitness_of_worst = self.fitness(\
            next_population[len(next_population)-1])

        # only for visual output purpose.
        print "generation " + str(generation) +\
        " smallest fitness " + str(fitness_of_best) 

        new_sigma = sigma

        if(2 - 1 * pow(10, -1) < fitness_of_best < 2 + 1 * pow(10, -1)):
            print next_population[0]
            return True
        else:
            return (next_population, generation + 1, m,\
            l, fitness_of_best, alpha, new_sigma)

    def run(self, dimensions, size, m, l, alpha, sigma):
        # create random population d-dimensional 
        # in interval [-s, s] but valid!
        
        genpop = self.generate_population(dimensions, size)   
        
        # check for feasiblity and initialize sliding feasible and 
        # infeasible populations.

        feasible_parents = []
        while(len(feasible_parents) < m): 
            parent = genpop.next()
            if(self.is_feasible(parent)):
                feasible_parents.append(parent)
                self._sliding_feasibles.append(parent)
            else:
                self._sliding_infeasibles.append(parent)

        # initial training of the meta model

        self.train_metamodel(\
            self._sliding_feasibles,
            self._sliding_infeasibles)

        result = self._run((feasible_parents, 0, m, l, 0, alpha, sigma))

        while result != True:
            result = self._run(result)

        return result

#env = SVCSliding()
#env.run(2, 10, 15, 100, 0.5, 1)