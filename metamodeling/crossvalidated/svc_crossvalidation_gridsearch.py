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

from svc_meta_model import SVCMetaModel

class SVCCrossvalidationGridsearch(SVCCrossvalidationStrategy):
    """ A strategy for crossvalidation """

    def __init__(self, fold):
        print("fold")

    def tune_svc(self, feasible, infeasible):
        """ This method returns a pair (C, gamma) with classifcation rate
            is maximized. """
        print("tune")            
