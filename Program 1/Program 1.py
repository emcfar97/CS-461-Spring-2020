##############################################################################
##
## CS 461
## Program #1
## Ethan McFarland
## Em463@mail.umkc.edu
##
##############################################################################

from scipy.spatial.distance import cityblock

class Pathfinder():
    """Implementation of A* pathfinding"""

    def __init__(self):

        self.goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def setup(self, start):

        self.path = []
        self.unvisited = {start}
        self.visited = set()

    def astar(self, limit): 
        """Returns path from start state to goal state as list of tuples
        unless a solution cannot be found by the time the limit is reached"""
        
        while self.unvisited and len(self.path) < limit:

            best = min(
                self.unvisited, key=lambda state: self.get_distance(state)
                )
            self.path.append(best)
            self.unvisited.remove(best)
            self.visited.add(best)
            
            for child in self.options(best):

                if self.get_distance(child) == 0: 
                    
                    return self.path + [child]
                
                if not (child in self.visited or child in self.unvisited): 

                    self.unvisited.add(child)
        
        else: return self.path[0], 'No solution'

    def get_distance(self, state):
        """Returns city-block distance for given state or parent if not given"""

        return cityblock(state, self.goal)
    
    def options(self, state, width=3):
        """Returns up-to four possible moves for self"""
        
        k = []
        zero = state.index(0)

        if zero >= width: # move up
            k.append(
                self.move([zero - width, zero], state)
                )

        if (zero + width) < len(state): # move down
            k.append(
                self.move([zero + width, zero], state)
                )

        if zero % width: # move left
            k.append(
                self.move([zero - 1, zero], state)
                )

        if (zero + 1) % width: # move right
            k.append(
                self.move([zero + 1, zero], state)
                )
        
        return k

    def move(self, swap, state):
        
        a, b = swap[::-1] if (swap[0] > swap[1]) else swap

        parent = list(state)
        parent[a], parent[b] = parent[b], parent[a]

        return tuple(parent)

with open(r'Program 1\sample puzzles.txt') as file:
    
    # Split file input into separate puzzles
    puzzles = ''.join(file.readlines()).split('\n\n')

pathfinder = Pathfinder()

for num, puzzle in enumerate(puzzles):

    if puzzle and num in (2, 3, 4, 6):
        puzzle = tuple( # flatten puzzle and convert to integers
            int(num) for row in puzzle.split('\n') for num in row.split()
            )
        pathfinder.setup(puzzle)
        with open(rf'Program 1\puzzle{num}.txt', 'w') as file:
            solution = pathfinder.astar(5000)
            for state in solution:
                file.write(f'{state}\n')