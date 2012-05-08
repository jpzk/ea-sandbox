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

from random import random, sample, gauss
from svc_parameterized_meta_model import SVCParameterizedMetaModel

class SVCCVEvolutionStrategy:

    _count_is_feasible = 0
    _count_is_meta_feasible = 0
    _count_train_metamodel = 0
    _count_fitness = 0
    _count_generations = 0
    _sum_wrong_class = 0
    _meta_model = SVCParameterizedMetaModel()

    def get_statistics(self):
        return {
            "generations" : self._count_generations,
            "constraint-calls" : self._count_is_feasible,
            "metamodel-calls" : self._count_is_meta_feasible,
            "fitness-function-calls" : self._count_fitness,
            "train-function-calls" : self._count_train_metamodel,
            "sum-wrong-classification" : self._sum_wrong_class } 

    # return true if solution is valid, otherwise false.
    def is_feasible(self, x):
        self._count_is_feasible += 1
        return sum(x) - 2.0 >= 0

    # return true if solution is feasible in meta model, otherwise false.
    def is_meta_feasible(self, x):
        self._count_is_meta_feasible += 1
        return self._meta_model.check_feasibility(x)

    # train the metamodel with given points
    def train_metamodel(self, feasible, infeasible, parameter_c, parameter_gamma):
        self._count_train_metamodel += 1
        self._meta_model.train(feasible, infeasible, parameter_c, parameter_gamma)

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
    def rechenberg(self, old_sigma, success_probability, alpha, minstep=False):
        if minstep != False: 
            if old_sigma < minstep: 
                return old_sigma 
        if success_probability > 1.0/5.0: 
            sigma = old_sigma / alpha
            return sigma
        if success_probability < 1.0/5.0: 
            sigma = old_sigma * alpha
            return sigma
        return old_sigma

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


