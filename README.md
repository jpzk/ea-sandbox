# evolutionary-algorithms-sandbox

This repository is an public archive for some of my evolutionary-algorithms I implemented. Use it as an alternative example for these algorithms, just in case you want to learn evolutionary algorithms, which is great! In the following descriptions are illustrated. 

## Basic information

(1+1) means (mu+lambda) which is common in literature. mu is the amount of individuals to select and lambda is the amount of individuals to generate by mutation. There are two types of selection the plus- and comma-selection. The plus-selection considers old population and mutated population when selecting the fittest for the next generation. The comma-selection only takes account of the mutated population. 

## Bitflip (1+1)-EA

The goal of the Bitflip (1+1)-EA is to generate a sequence of bits where every bit is 1. Therefore the fitness function counts the ones in a sequence of bits. The mutation of this evolutionary algorithm influences each bit. With a certain probability, which is equal for each bit, a bit flips, e.g. the state 0 changes to 1. The selection of the Bitflip (1+1)-EA is defined by just selecting between the old sequence of bits or the mutated sequence of bits.

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

