# Bruteforce Sokoban Solver

### WHY ?

I was blocked at level 11 on my phone. I needed closure...

### HOW TO PLAY THE GAME ?

https://en.wikipedia.org/wiki/Sokoban

### HOW TO USE THE SOLVER ?

Input: Set the Sokoban map in parameters

```
_map_example =  \
                '''
                XXXXXX
                X....X
                X.B.PX
                XXM..X
                X.M.XX
                X.M.XX
                X.M.XX
                X.O.XX
                XXXXXX
                '''
```                
  
Lexique:
```
                X: wall
                .: trail
                O: objective
                P: player
                N: player on objective
                B: block
                M: block on objective
```                
                
Constraints:
                - Surround your map with walls
                - Put as many blocks as objectives
  
Run the python script to solve.

### OUTPUTS           

Prints the steps to the solution if any is found

### HOW DOES IT WORK ?

Bruteforce !! A memory of block position and reachable states is kept, to avoid
cycles. Some pruning heuristics are added to avoid useless computations
