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

{- (1+1)-EA bitflip
 - Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de> -}

type Bit = Bool
type Probability = Float 

onemax :: [Bit] -> Int
onemax bits = foldl (\x y -> x + y) 0 (map convert bits)
    where convert bit 
            | bit == True = 1 
            | bit == False = 0

flips :: Probability -> [Probability] -> [Bit]
flips alpha randoms = map (cut alpha) randoms 
    where cut alpha p 
            | p < alpha = False 
            | otherwise = True

recurse :: [Bit] -> [Float] -> Float -> [[Bit]]
recurse bits rnds alpha  
    | onemax bits == length bits = [bits] 
    | otherwise = bits : continue bits rnds alpha  

mutate :: [Bit] -> [Bit] -> [Bit] 
mutate bits flips = map flipit (zip bits flips)
    where flipit (x,y) = (not x) && y

continue :: [Bit] -> [Float] -> Float -> [[Bit]]
continue bits rnds alpha = recurse mutated rnds' alpha
    where 
        mutated = mutate bits (flips alpha randomfloats)
        rnds' = drop (length bits) rnds
        randomfloats = take (length bits) rnds

main :: IO () 
main = do 
    putStrLn (show (recurse example randomlist alpha))
    where 
        alpha = 0.25
        example = [False, False, False, False] 
        randomlist = ((randoms (mkStdGen 42)) :: [Float])

