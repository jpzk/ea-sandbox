# mlrechenberg.py: an EA with Rechenberg's rule

The (mu+lambda)-EA in mlrechenberg.py is an evolutionary algorithm to minimize sum(map(lambda x : pow(x,2), x)), which is the sphere function for the dimensionality of x. Rechenberg's rule of chance of success increments or decrements mutation step size depending on the chance of success, which in fact is the relative amount of good solutions in a given period of generations. A good solution is compared with an reference fitness e.g. the best of the last period. If the relative amount of good solutions in a period is greater than 1/5, then increment step size. If it is lower than 1/5 decrement, and otherwise keep the last step size. The outcome of this approach is finding an optimum solution in much less time.   


