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
from svc_evolution_strategy import SVCEvolutionStrategy
from svc_crossvalidation_random import SVCCrossvalidationRandom
from svc_scaling_standardscore import SVCScalingStandardscore

class SVCBestWeighted(SVCEvolutionStrategy):

    _crossvalidation = SVCCrossvalidationRandom(fold = 5)

    # main evolution 
    def _run(self, (population, generation, m, l, lastfitness,\
        alpha, sigma)):

        self._count_generations += 1

        # generate l-children union with parents, 
        # take the m best.
        childgen = self.generate_children(population, sigma)
        children = [childgen.next() for child in range(0,l)]

        # Filter by checking feasiblity with SVC meta model, the 
        # meta model might be wrong, so we have to weighten between
        # the filtern with meta model and filtering with the 
        # true constraint function.
        beta = 0.5
        cut = int(floor(beta * len(children)))
        meta_children = children[:cut]
        constraint_children = children[cut:]

        # scaling and filter feasible with meta model
        scaled_meta_children = self._scaling.scale(meta_children)
        meta_feasible_children = filter(\
            self.is_meta_feasible, 
            scaled_meta_children)
        
        # Filter by true feasibility with constraind function, here we
        # can update the sliding feasibles and infeasibles.
        feasible_children = []
        infeasible_children = []
        best_feasible = []
        best_infeasible = []
        
        for meta_feasible in meta_feasible_children: 
            if(self.is_feasible(meta_feasible)):
                feasible_children.append(meta_feasible)               
            else:
                self._sum_wrong_class += 1
                infeasible_children.append(meta_feasible)

        # Filter the other part of the cut with the true constraint function. 
        # Using this information to update the meta model.
        for child in constraint_children:
            if(self.is_feasible(child)):
                feasible_children.append(child)
            else:
                infeasible_children.append(child) 
        
        next_population =\
            self.sortedbest(population + feasible_children)[:m]
        
        best_infeasibles = self.sortedbest(infeasible_children)[:m]
        best_feasibles = next_population[:m]

        # scaling, scaling factors are kept in scaling attribute.
        self._scaling = SVCScalingStandardscore(best_infeasibles + best_feasibles)
        scaled_best_feasibles = self._scaling.scale(best_feasibles)
        scaled_best_infeasibles = self._scaling.scale(best_infeasibles)

        parameter_c = m + m 
        parameter_gamma = 0.0

        self.train_metamodel(\
            scaled_best_feasibles,
            scaled_best_infeasibles,
            parameter_c,
            parameter_gamma)

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

        # initial training of the meta model

        best_feasibles = self.sortedbest(feasibles)[:m]
        best_infeasibles = self.sortedbest(infeasibles)[:m]

        # scaling, scaling factors are kept in scaling attribute.
        self._scaling = SVCScalingStandardscore(best_feasibles + best_infeasibles)
        scaled_best_feasibles = self._scaling.scale(best_feasibles)
        scaled_best_infeasibles = self._scaling.scale(best_infeasibles)

        parameter_c = m + m
        parameter_gamma = 0.0

        self.train_metamodel(\
            scaled_best_feasibles,
            scaled_best_infeasibles,
            parameter_c,
            parameter_gamma)

        result = self._run((feasible_parents, 0, m, l, 0, alpha, sigma))

        while result != True:
            result = self._run(result)

        return result

env = SVCBestWeighted()
env.run(2, 10, 15, 100, 0.5, 1)
