# bitflip.py & bitflip.hs: bitflip (1+1)-EA

The goal of the Bitflip (1+1)-EA is to generate a sequence of bits where every bit is 1. Therefore the fitness function counts the ones in a sequence of bits. The mutation of this evolutionary algorithm influences each bit. With a certain probability, which is equal for each bit, a bit flips, e.g. the state 0 changes to 1. The selection of the Bitflip (1+1)-EA is defined by just selecting between the old sequence of bits or the mutated sequence of bits.

