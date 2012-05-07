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

from svc_cv_evolution_strategy import SVCCVEvolutionStrategy
from svc_scaling_standardscore import SVCScalingStandardscore
from svc_cv_grid import SVCCVGrid

class SVCCVBestSlidingWeighted(SVCCVEvolutionStrategy):
    """ Using the fittest feasible and infeasible individuals in a sliding
        window (between generations) to build a meta model using SVC. """
    
    _crossvalidation = SVCCVGrid(fold = 5) 
    _window_size = 25 
    _beta = 0.9
    _append_to_window = 10 
    _sliding_best_feasibles = deque(maxlen = _window_size)
    _sliding_best_infeasibles = deque(maxlen = _window_size)

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

        # check scaled against meta model, BUT the unscaled against 
        # the constraint function.
        meta_feasible_children = filter(\
            lambda child : self.is_meta_feasible(self._scaling.scale(child)), 
            meta_children)
        
        # Filter by true feasibility with constraind function, here we
        # can update the sliding feasibles and infeasibles.
        feasible_children = []
        infeasible_children = []
        
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
            next_population[:self._append_to_window])

        sliding_best_infeasibles =\
            [child for child in self._sliding_best_infeasibles]

        sliding_best_feasibles =\
            [child for child in self._sliding_best_feasibles]

        # new scaling because sliding windows changes
        self._scaling = SVCScalingStandardscore(\
            sliding_best_feasibles + sliding_best_infeasibles)

        scaled_best_feasibles = map(\
            self._scaling.scale, 
            self._sliding_best_feasibles)

        scaled_best_infeasibles = map(\
            self._scaling.scale,
            self._sliding_best_infeasibles)                

        best_parameters = self._crossvalidation.crossvalidate(\
            scaled_best_feasibles,
            scaled_best_infeasibles)

        self.train_metamodel(\
            best_parameters[0],
            best_parameters[1],
            best_parameters[2],
            best_parameters[3])

        fitness_of_best = self.fitness(next_population[0])
        fitness_of_worst = self.fitness(\
            next_population[len(next_population)-1])

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

        while(len(feasible_parents) < m):
            parent = genpop.next()
            if(self.is_feasible(parent)):
                feasible_parents.append(parent)
                feasibles.append(parent)
            else:
                infeasibles.append(parent)

        # just to be sure 
        while(len(infeasibles) < self._window_size):
            parent = genpop.next()
            if(not self.is_feasible(parent)):
                infeasibles.append(parent)

        while(len(feasibles) < self._window_size):
            parent = genpop.next()
            if(self.is_feasible(parent)):
                feasibles.append(parent)

        # initial training of the meta model

        best_feasibles = self.sortedbest(feasibles)[:self._window_size]
        best_infeasibles = self.sortedbest(infeasibles)[:self._window_size]
 
        # adding to sliding windows

        map(self._sliding_best_feasibles.append, best_feasibles)
        map(self._sliding_best_infeasibles.append, best_infeasibles)

        # scaling, scaling factors are kept in scaling attribute.
        self._scaling = SVCScalingStandardscore(best_feasibles + best_infeasibles)
        scaled_best_feasibles = self._scaling.scale(best_feasibles)
        scaled_best_infeasibles = self._scaling.scale(best_infeasibles)

        best_parameters = self._crossvalidation.crossvalidate(\
            scaled_best_feasibles,
            scaled_best_infeasibles)

        self.train_metamodel(\
            best_parameters[0],
            best_parameters[1],
            best_parameters[2],
            best_parameters[3])

        result = self._run((feasible_parents, 0, m, l, 0, alpha, sigma))

        while result != True:
            result = self._run(result)

        return result

#env = SVCCVBestSlidingWeighted()
#env.run(2, 10, 15, 100, 0.5, 1)

