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

from svc_parameterized_meta_model import SVCParameterizedMetaModel
from svc_crossvalidation_strategy import SVCCrossvalidationStrategy

class SVCCrossvalidationGrid(SVCCrossvalidationStrategy):
    """ A strategy for crossvalidation """

    _lower_bound_c = -5
    _upper_bound_c = 15
    _lower_bound_gamma = -15
    _upper_bound_gamma = 3

    def __init__(self, fold):
        self._fold = fold

    def crossvalidate(self, feasible, infeasible):
        """ This method returns a pair (C, gamma) with classifcation rate
            is maximized. """

        best_accuracy = 0.0
        best_parameter_c = 0.0
        best_parameter_gamma = 0.0
        best_training_feasible = []
        best_training_infeasible = []

        # seperating into n (fold) seperate equal-sized sets
       
        group_size_feasible = int(floor(len(feasible) / self._fold))
        groups_feasible =\
            [list(t) for t in zip(*[iter(feasible)] * group_size_feasible)]       

        group_size_infeasible = int(floor(len(infeasible) / self._fold))
        groups_infeasible =\
            [list(t) for t in zip(*[iter(infeasible)] * group_size_infeasible)] 
        
        group_indices = range(0, self._fold - 1)
 
        # for each i, j, test_group_index

        for i in range(self._lower_bound_c, self._upper_bound_c):
            for j in range(self._lower_bound_gamma, self._upper_bound_gamma):
                for test_group_index in group_indices:

                    # selecting training groups and test group

                    training_groups_indices = range(0, self._fold - 1)
                    training_groups_indices.remove(test_group_index)
                       
                    training_feasible = reduce(
                            lambda x,y: x + y, 
                            [groups_feasible[i] for i in training_groups_indices])

                    training_infeasible = reduce(
                            lambda x,y: x + y,
                            [groups_infeasible[i] for i in training_groups_indices])

                    test_feasible = groups_feasible[test_group_index]
                    test_infeasible = groups_infeasible[test_group_index]

                    # calculate C and gamma

                    parameter_c = 2 ** i
                    parameter_gamma = 2 ** j

                    # train the meta model with C and gamma

                    meta_model = SVCParameterizedMetaModel()
                    meta_model.train(\
                        training_feasible, 
                        training_infeasible,
                        parameter_c,
                        parameter_gamma)

                    # calculating accurary with test group

                    correct = 0.0
                    amount = len(test_feasible) + len(test_infeasible)
                    
                    for feasible in test_feasible:
                        if(meta_model.check_feasibility(feasible)):
                            correct += 1
                    
                    for infeasible in test_infeasible:
                        if(not meta_model.check_feasibility(infeasible)):
                            correct += 1

                    accuracy = correct / amount
                    
                    if(accuracy > best_accuracy):
                        best_accuracy = accuracy
                        best_parameter_c = parameter_c
                        best_parameter_gamma = parameter_gamma
                        best_training_feasible = training_feasible
                        best_training_infeasible = training_infeasible
        
        return (best_training_feasible,
            best_training_infeasible,
            best_parameter_c,
            best_parameter_gamma)
