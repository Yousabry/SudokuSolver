# SudokuSolver
How it works:
Solver(): Uses three basic patterns to try to solve the grid.
If the grid is solved then great!

if Solver() is no longer making progress, continue to trial and error portion.
the possibilities for each square are stored in a list in the corresponding location in grid
trial() tries a value in the list of possibilities, with three possible outcomes:

1. The grid is solved. Great!
2. There is now a mistake (contradiction) in the grid. Then, we remove the value from the list of possibilities and continue trial()
3. No mistake found and grid is not solved. This is the worst case scenario as we have gained no new informaition. Try next value for trial()

Notes:
The values stored in the grid are actually the opposite of the possibilities. I designed it this way so if when running trial() case 2 occurs, we can add the new value we know the square cannot be. If the true possibilities were stored in the grid, the new info would get lost after the update.

