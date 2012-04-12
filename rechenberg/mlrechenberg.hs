{-
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
-}

import System.Random
import Data.Random.Normal

{- (m+l)-EA with Rechenbergs 1/5-rule.
 - Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de> -}

type Mu = Integer
type Lambda = Integer
type Dimension = Int
type Population = [Vector]
type Vector = [Float]
type Fitness = Float
type Sigma = Float
type Alpha = Float
type Probability = Float

{- The configuration record is changed when switching from one population 
 - to another. It defines a state of evolution parameters. -}

data Configuration = Configuration {
    lambda :: Lambda,
    sigma :: Sigma,
    alpha :: Alpha,
    lastbestfitness :: Fitness,
    mutationStdGen :: StdGen,
    pairingStdGen :: StdGen}

{- This is the fitness function, which we're trying to minimize with each 
 - step in the evolution function.-}

fitness :: Vector -> Fitness
fitness x = foldl (\x y -> x + y*y) 0 x

{- These functions mutate a population with a given sigma and StdGen, which 
 - is created in every iteration of evolution. -}

mutate :: Population -> Sigma -> StdGen -> Population
mutate pop sigma gen = mutate' pop mutations
    where mutations = (normals' (0, sigma) gen :: [Float])

mutate' :: Population -> [Float] -> Population
mutate' (x:xs) mutations 
    | xs == [] = x 
    | otherwise = mutateBy x : mutate' xs (drop (length x) mutations)
    where mutateBy x = map (\x y -> x+y) $ zip x (take (length x) mutations)

{- These combine functions are required to combine parents. It's important
 - to know that combinePairs is applied on random lists (for indices to 
 - combine) which are bound by the IO evolution function. -}

combine :: Vector -> Vector -> Vector
combine r s = map (\(x,y) -> (x+y)/2) $ zip r s 

combinePairs :: Population -> Lambda -> StdGen -> Population
combinePairs pop lambda gen = combinePairs' 0 lambda pop rndindices
    where rndindices = randomRs (0, ((length pop) - 1)) gen

combinePairs' :: Integer -> Lambda -> Population -> [Int] -> Population
combinePairs' i lambda pop rndindices 
    | i < lambda = combine' : next
    | i == lambda = []
    where 
        indices = take 2 rndindices
        combine' = combine (pop !! (indices !! 0)) (pop !! (indices !! 1))
        next = combinePairs' (i+1) lambda pop (drop 2 rndindices)

{- These two functions are required to generate an initial population 
 - by a given lambda (size of population) and dimension (dimensions of the
 - individuals. -} 

generate :: Lambda -> Dimension -> StdGen -> Sigma -> Population
generate lambda dim gen sigma = generate' 0 lambda dim randoms
    where randoms = normals' (0, sigma) gen :: [Float]

generate' :: Integer -> Lambda -> Dimension -> [Float] -> Population
generate' i lambda dim randoms 
    | i < lambda = take dim randoms : next
    | i == lambda = []
    where next = generate' (i+1) lambda dim (drop dim randoms)    

{- These two functions are required to use rechenberg's 1/5-rule
 - the first changes sigma according to the success probability
 - of the latter. Alpha is a constant. -}

rechenberg :: Sigma -> Probability -> Alpha -> Sigma
rechenberg oldsigma successprob alpha 
    | successprob > 1.0/5.0 = oldsigma / alpha
    | successprob < 1.0/5.0 = oldsigma * alpha
    | otherwise = oldsigma

success :: Population -> Fitness -> Probability
success pop fit = better / popsize
    where 
        better = fromIntegral (length (smaller fitnesses)) :: Float
        fitnesses = map fitness pop
        popsize = fromIntegral (length pop) :: Float
        smaller = filter (\x -> x < fit)  

{- The configuration record is changed when switching from one population 
 - to another. It defines a state of evolution parameters. -}

configurate :: Population -> Configuration -> StdGen -> StdGen -> Configuration
configurate pop config pgen mgen = 
    Configuration newlambda newsigma newalpha newbest pgen mgen 
    where
        newlambda = (lambda config)
        newsigma = rechenberg (sigma config) successprob (alpha config)
        newalpha = (alpha config) 
        newbest = minimum (map fitness pop)
        successprob = success pop (lastbestfitness config)

children :: Population -> Configuration -> Population 
children pop config = mutate combined (sigma config) (mutationStdGen config) 
    where combined = combinePairs pop (lambda config) (pairingStdGen config)

{- main evolution function which constructs the trajectory of populations.
 - the infinite random lists are consumed by mutation and combining.-}

evolution :: IO [Population] -> Configuration -> IO [Population]
evolution pop config
    | lastbestfitness config < 0.1 = pop
    | otherwise = do
        current <- pop
        pgen <- newStdGen
        mgen <- newStdGen
        next <- evolution (return ([offspring (last current)])) 
            (configurate (last current) config pgen mgen)
        return (current ++ next)
    where 
        offspring last = children last config 

main :: IO ()
main = do
    rndgen <- getStdGen
    putStrLn (show (initialPopulation rndgen))
    {-evolution (initialPopulation rndgen)-}
    return ()
    where 
        initialPopulation gen = (generate 2 2 gen 1.0)
