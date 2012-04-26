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

from sklearn import svm

class SVCMetaModel:
    """ SVC meta model which classfies feasible and infeasible points """

    def train(self, feasible, infeasible):
        """ Train a meta model classification with new points """

        points_svm = [i for i in infeasible] + [f for f in feasible]
        labels = [-1] * len(infeasible) + [1] * len(feasible) 
        self._clf = svm.SVC()
        self._clf.fit(points_svm, labels)

    def check_feasibility(self, point):
        """ Check the feasibility with meta model """

        prediction = self._clf.predict(point) 
        if(prediction < 0):
            return False
        else:
            return True                


