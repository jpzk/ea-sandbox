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

