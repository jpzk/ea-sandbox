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

from svc_cv_grid import SVCCVGrid
from svc_cv_best_sliding_weighted import SVCCVBestSlidingWeighted
from svc_best_sliding_weighted import SVCBestSlidingWeighted
from svc_best_weighted import SVCBestWeighted
from without_constraint_metamodel import WithoutConstraintMetaModel

import csv

writer = csv.writer(open('experiments/measurements/experimentC_b.csv', 'wb'), delimiter=';')
writer.writerow(\
    ["method",
    "train-function-calls",
    "sum-wrong-classification",
    "constraint-calls", 
    "metamodel-calls", 
    "fitness-function-calls", 
    "generations"])

for i in range(0, 200):
    method = WithoutConstraintMetaModel() 
    method.run(2, 10, 15, 100, 0.5, 1)
    stats = method.get_statistics()
    writer.writerow(\
        ["WithoutMetaModel",
        stats["train-function-calls"],
        stats["sum-wrong-classification"],
        stats["constraint-calls"],
        stats["metamodel-calls"],
        stats["fitness-function-calls"],
        stats["generations"]])
    print "WithoutMetaModel " + str(i)

for i in range(0, 200):
    method = SVCBestSlidingWeighted(0.9, 25, 10)

    method.run(2, 10, 15, 100, 0.5, 1)
    stats = method.get_statistics()
    writer.writerow(\
        ["SVCBestSlidingWeighted",
        stats["train-function-calls"],
        stats["sum-wrong-classification"],
        stats["constraint-calls"],
        stats["metamodel-calls"],
        stats["fitness-function-calls"],
        stats["generations"]])
    print "SVCBestSlidingWeighted " + str(i)

"""
for i in range(0, 200):
    method = SVCCVBestSlidingWeighted(
        beta = 0.9, 
        append_to_window = 10, 
        window_size = 25,
        crossvalidation = SVCCVGrid(fold = 5))

    method.run(2, 10, 15, 100, 0.5, 1)
    stats = method.get_statistics()
    writer.writerow(\
        ["SVCCVBestSlidingWeighted",
        stats["train-function-calls"],
        stats["sum-wrong-classification"],
        stats["constraint-calls"],
        stats["metamodel-calls"],
        stats["fitness-function-calls"],
        stats["generations"]])
    print "SVCCVBestSlidingWeighted " + str(i)        

for i in range(0, 200):
    method = SVCBestWeighted(beta = 0.9, amount_metamodel = 50)
    method.run(2, 10, 15, 100, 0.5, 1)
    stats = method.get_statistics()
    writer.writerow(\
        ["SVCBestWeighted",
        stats["train-function-calls"],
        stats["sum-wrong-classification"],
        stats["constraint-calls"],
        stats["metamodel-calls"],
        stats["fitness-function-calls"],
        stats["generations"]])
    print "SVCBestWeighted " + str(i)        
"""
#env = WithoutMetaModel()
#env.run(2, 10, 15, 100, 0.5, 1)
