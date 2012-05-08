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

from svc_evolution_strategy import SVCEvolutionStrategy

class WithoutConstraintMetaModel(SVCEvolutionStrategy):

    # main evolution 
    def _run(self, (population, generation, m, l, lastfitness,\
        alpha, sigma)):

        self._count_generations += 1

        # generate l-children union with parents, 
        # take the m best.
        childgen = self.generate_children(population, sigma)

        feasible_children = []
        while(len(feasible_children) < l): 
            child = childgen.next()
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
        
        # check for feasiblity and initialize sliding feasible and 
        # infeasible populations.

        feasible_parents = []
        while(len(feasible_parents) < m):
            parent = genpop.next()
            if(self.is_feasible(parent)):
                feasible_parents.append(parent)

        result = self._run((feasible_parents, 0, m, l, 0, alpha, sigma))

        while result != True:
            result = self._run(result)

        return result
