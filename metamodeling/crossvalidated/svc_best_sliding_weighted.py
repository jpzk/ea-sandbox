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
from collections import deque # used for sliding window for best
from svc_evolution_strategy import SVCEvolutionStrategy

class SVCBestSlidingWeighted(SVCEvolutionStrategy):
    """ Using the fittest feasible and infeasible individuals in a sliding
        window (between generations) to build a meta model using SVC. """

    def __init__(self, beta, window_size, append_to_window):
        self._beta = beta 
        self._window_size = window_size
        self._append_to_window = append_to_window
        self._sliding_best_feasibles = deque(maxlen = self._window_size)
        self._sliding_best_infeasibles = deque(maxlen = self._window_size)

    # main evolution 
    def _run(self, (population, generation, m, l, lastfitness,\
        alpha, sigma)):
        """ This method is called every generation. """

        self._count_generations += 1

        # generate l-children union with parents, 
        # take the m best.
        childgen = self.generate_children(population, sigma)
        children = [childgen.next() for child in range(0,l)]

        # Filter by checking feasiblity with SVC meta model, the 
        # meta model might be wrong, so we have to weighten between
        # the filtern with meta model and filtering with the 
        # true constraint function.
        cut = int(floor(self._beta * len(children)))
        meta_children = children[:cut]        
        constraint_children = children[cut:]

        # Filter by meta model
        meta_feasible_children = filter(self.is_meta_feasible, meta_children)
        
        # Filter by true feasibility with constraind function, here we
        # can update the sliding feasibles and infeasibles.
        feasible_children = []
        infeasible_children = []
       
        # Death penalty when feasible by meta model but is infeasible
        for meta_feasible in meta_feasible_children:             
            if(self.is_feasible(meta_feasible)):
                feasible_children.append(meta_feasible)                
            else:
                self._sum_wrong_class += 1
                infeasible_children.append(meta_feasible)

                # Because of Death Penalty we need a feasible reborn.
                reborn = []
                while(len(reborn) < 1):  
                    generated = childgen.next()
                    if(self.is_meta_feasible(generated)):
                        if(self.is_feasible(generated)):
                            reborn.append(generated)
                feasible_children.extend(reborn)                  

        # Filter the other part of the cut with the true constraint function. 
        # Using this information to update the meta model.
        for child in constraint_children:
            if(self.is_feasible(child)):
                feasible_children.append(child)
            else:
                infeasible_children.append(child) 
                # Because of Death Penalty we need a feasible reborn.

                reborn = []
                while(len(reborn) < 1):
                    generated = childgen.next()
                    if(self.is_feasible(generated)):
                        reborn.append(generated)
                feasible_children.extend(reborn)

        # feasible_children contains exactly lambda feasible children
        # and infeasible_children 
        next_population =\
            self.sortedbest(population + feasible_children)[:m]
        
        map(self._sliding_best_infeasibles.append,
            self.sortedbest(infeasible_children)[:self._append_to_window])

        map(self._sliding_best_feasibles.append,
            self.sortedbest(feasible_children)[:self._append_to_window])

        self.train_metamodel(\
            self._sliding_best_feasibles,
            self._sliding_best_infeasibles)

        fitness_of_best = self.fitness(next_population[0])
        fitness_of_worst = self.fitness(\
            next_population[len(next_population) - 1])

        # only for visual output purpose.
        print "generation " + str(generation) +\
        " smallest fitness " + str(fitness_of_best) 

        new_sigma = sigma

        if(2 - 1 * pow(10, -2) < fitness_of_best < 2 + 1 * pow(10, -2)):
            print next_population[0]
            return True
        else:
            return (next_population, generation + 1, m,\
            l, fitness_of_best, alpha, new_sigma)

    def run(self, dimensions, size, m, l, alpha, sigma):
        """ This method initializes the population etc. And starts the 
            recursion. """
        
        genpop = self.generate_population(dimensions, size)   
        
        # check for feasiblity and initialize sliding feasible and 
        # infeasible populations.

        feasible_parents = []
        best_feasibles = []
        feasibles = []
        best_infeasibles = []
        infeasibles = []

        # generate a feasible population

        while(len(feasible_parents) < m):
            parent = genpop.next()
            if(self.is_feasible(parent)):
                feasible_parents.append(parent)
                feasibles.append(parent)
            else:
                infeasibles.append(parent)

        # initial training of the meta model

        # just to be sure 
        while(len(infeasibles) < self._window_size):
            parent = genpop.next()
            if(not self.is_feasible(parent)):
                infeasibles.append(parent)

        while(len(feasibles) < self._window_size):
            parent = genpop.next()
            if(self.is_feasible(parent)):
                feasibles.append(parent)

        best_feasibles = self.sortedbest(feasibles)[:self._window_size]
        best_infeasibles = self.sortedbest(infeasibles)[:self._window_size]

        self.train_metamodel(\
            best_feasibles,
            best_infeasibles)

        result = self._run((feasible_parents, 0, m, l, 0, alpha, sigma))

        while result != True:
            result = self._run(result)

        return result

#env = SVCBestSlidingWeighted()
#env.run(2, 10, 15, 100, 0.5, 1)

