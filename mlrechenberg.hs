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

fitness :: Vector -> Fitness
fitness x = foldl (\x y -> x + y*y) 0 x

combine :: Vector -> Vector -> Vector
combine r s = map (\(x,y) -> (x+y)/2) $ zip r s 

rechenberg :: Sigma -> Probability -> Alpha -> Sigma
rechenberg oldsigma successprob alpha 
    | successprob > 1.0/5.0 = oldsigma / alpha
    | successprob < 1.0/5.0 = oldsigma * alpha
    | otherwise = oldsigma

mutate :: Vector -> Sigma -> StdGen -> Vector
mutate x sigma gen = map (\(x,y) -> x+y) $ zip x randoms
    where randoms = normals' (0, sigma) gen :: Vector

{- @todo combine parents, mutation and selection -}
process :: Population -> StdGen -> Sigma -> Population
process population gen newsigma = population

{- @todo generate population  -}
generate :: Lambda -> Dimension -> (StdGen, Sigma) -> Population
generate lambda d (gen, sigma) = [take d (randoms gen :: Vector)]

{- @todo combine parents; select best mu individuals -}
evolution :: [Population] -> (StdGen, Alpha, Sigma, Fitness) -> [Population]
evolution population (gen, alpha, oldsigma, lastbest)
    | minimum fitnesses < 0.1 = population 
    | otherwise = population ++ [(process (last population) gen newsigma)]
    where 
        newsigma = rechenberg oldsigma successprob alpha
        fitnesses = map fitness (last population)
        successprob = 1.0/5.0

main :: IO ()
main = do
    srnd <- getStdGen
    putStrLn (show (mutate [0.0, 0.0, 0.0] 1.0 srnd))
