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

'''
NOTES

The meta model quality should be rated somehow. The approaches by KNN
meta model quality might not apply to this case of SVC meta modeling. 
Therefore I try different approaches experimentally. 

First approach: Let c be the amount of generated children and n + m = c.
Splitting the generated children and validate the feasibility of n children
by the meta model and the feasibility of m children by the constraint 
function. The m children might be feasible where the meta model predicts
unfeasibilty. Therefore the meta model needs to be corrected. The points 
which are really feasible and infeasible and are classified wrong by the
meta model are more important in the correction of the meta model. 
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

class SVCSlidingWeighted(SVCEvolutionStrategy): 

    _sliding_feasibles = deque(maxlen = 50) 
    _sliding_infeasibles = deque(maxlen = 50)

    # main evolution 
    def _run(self, (population, generation, m, l, lastfitness,\
        alpha, sigma)):

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

        meta_feasible_children = filter(self.is_meta_feasible, meta_children)
        
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

        # Filter the other part of the cut with the true constraint function. 
        # Using this information to update the meta model.
        for child in constraint_children:
            if(self.is_feasible(child)):
                feasible_children.append(child)
                # append this to _sliding_feasibles because it is a correct
                # feasible and near the current population.
                self._sliding_feasibles.append(child)
            else:
                # append this to _sliding_infeasibles because it is a correct
                # infeasible and near the current population.
                self._sliding_infeasibles.append(child)

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

env = SVCSlidingWeighted()
env.run(2, 10, 15, 100, 0.5, 1)
