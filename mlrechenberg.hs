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

{- mutation consumes an infinite random list -}

mutate :: Vector -> Sigma -> StdGen -> Vector
mutate x sigma gen = map (\(x,y) -> x+y) $ zip x randoms
    where randoms = normals' (0, sigma) gen :: Vector

{- constructing a tupel list of parents to combine -}

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

{- generate and generate' are used to generate vectors from a 
 - normal distribution with sigma -}

generate :: Lambda -> Dimension -> StdGen -> Sigma -> Population
generate lambda dim gen sigma = generate' 0 lambda dim randoms
    where randoms = normals' (0, sigma) gen :: [Float]

generate' :: Integer -> Lambda -> Dimension -> [Float] -> Population
generate' i lambda dim randoms 
    | i < lambda = take dim randoms : next
    | i == lambda = []
    where next = generate' (i+1) lambda dim (drop dim randoms)    

{- main evolution function which constructs the trajectory of populations.
 - the infinite random lists are consumed by mutation and combining.-}

fitness :: Vector -> Fitness
fitness x = foldl (\x y -> x + y*y) 0 x

rechenberg :: Sigma -> Probability -> Alpha -> Sigma
rechenberg oldsigma successprob alpha 
    | successprob > 1.0/5.0 = oldsigma / alpha
    | successprob < 1.0/5.0 = oldsigma * alpha
    | otherwise = oldsigma

evolution :: [Population] -> (StdGen, Alpha, Sigma, Fitness) -> [Population]
evolution population (gen, alpha, oldsigma, lastbest)
    | minimum fitnesses < 0.1 = population 
    | otherwise = population ++ [last population]
    where 
        newsigma = rechenberg oldsigma successprob alpha
        fitnesses = map fitness (last population)
        successprob = 1.0/5.0

main :: IO ()
main = do
    srnd <- getStdGen
    putStrLn (show (mutate [0.0, 0.0, 0.0] 1.0 srnd))
