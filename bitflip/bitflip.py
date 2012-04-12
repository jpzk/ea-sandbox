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

from random import *

# (1+1)-EA
# Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de> 

def onemax(bitlist): return reduce((lambda x,y: x+y), bitlist)

def _run((bitlen, probability, current)):
    print current
    if(onemax(current) == bitlen): return True
    mutated = map(
        lambda probability, value: 
            abs(value - 1) if random() < probability else value,
        [probability] * len(current),
        current)
    if(onemax(current) >= onemax(mutated)):
        return (bitlen, probability, current)        
    else: return (bitlen, probability, mutated)

def run(bitlen, probability):
    result = (bitlen, probability, [0] * bitlen)
    while result != True:
        result = _run(result)

run(200, 0.25)        

