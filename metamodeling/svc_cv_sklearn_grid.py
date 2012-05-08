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

from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import KFold
from sklearn.cross_validation import LeaveOneOut
from svc_parameterized_meta_model import SVCParameterizedMetaModel
from svc_cv_strategy import SVCCVStrategy

class SVCCVSkGrid(SVCCVStrategy):
    """ A strategy for crossvalidation """

    def __init__(self, fold):
        self._fold = fold

    def crossvalidate(self, feasible, infeasible):
        """ This method returns a pair (C, gamma) with classifcation rate
            is maximized. """

        tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]}]

        clf = GridSearchCV(SVC(), tuned_parameters)

        X = feasible + infeasible
        y = [1] * len(feasible) + [-1] * len(infeasible) 

        clf.fit(X, y, cv=KFold(n = len(y), k = self._fold))

        return (feasible,
            infeasible,
            clf.best_estimator_.c, 
            clf.best_estimator_.gamma)
