# evolutionary-algorithms-sandbox

This repository is a public repository for some of my evolutionary-algorithms I implemented. Use it as an alternative example for these algorithms, just in case you want to learn evolutionary algorithms, which is great! The publication of Hans-Georg Beyer and Hans-Paul Schwefel [http://www.cs.bham.ac.uk/~pxt/NIL/es.pdf](PDF-file) is a comprehensive introduction to evolution strategies. In the following descriptions are illustrated. 

## Basic information

(1+1) means (mu+lambda), which is common in literature. mu is the amount of individuals to select and lambda is the amount of individuals to generate by mutation. There are two types of selection the plus- and comma-selection. The plus-selection considers old population and mutated population when selecting the fittest for the next generation. The comma-selection only takes account of the mutated population. 

## bitflip.py: bitflip (1+1)-EA

The goal of the Bitflip (1+1)-EA is to generate a sequence of bits where every bit is 1. Therefore the fitness function counts the ones in a sequence of bits. The mutation of this evolutionary algorithm influences each bit. With a certain probability, which is equal for each bit, a bit flips, e.g. the state 0 changes to 1. The selection of the Bitflip (1+1)-EA is defined by just selecting between the old sequence of bits or the mutated sequence of bits.

## mlrechenberg.py: an EA with Rechenberg's rule

The (mu+lambda)-EA in mlrechenberg.py is an evolutionary algorithm to minimize sum(map(lambda x : pow(x,2), x)), which is the sphere function for the dimensionality of x. Rechenberg's rule of chance of success increments or decrements mutation step size depending on the chance of success, which in fact is the relative amount of good solutions in a given period of generations. A good solution is compared with an reference fitness e.g. the best of the last period. If the relative amount of good solutions in a period is greater than 1/5, then increment step size. If it is lower than 1/5 decrement, and otherwise keep the last step size. The outcome of this approach is finding an optimum solution in much less time.   

## To be continued

The descriptions of other algorithms will follow.

## License

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

