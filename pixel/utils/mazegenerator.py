import numpy as np
# from config import height, width

from PIL import Image
import random
from pixel.state import State
import time

# maze_generator_path = "./output/maze_generator.gif"
height = 61
width = 61

#  Generate a maze using the recursive backtracker algorithm and Kruskal's algorithm
class MazeGenerator(State):
    # def __init__(self, path = None) -> None:
        # # initialize the grid. where height and width are defined in config.py
        # self.grid = np.zeros((height, width))
        # self.wall = 0
        # self.path = 1

    # return the output file path

    # setup the grid
    def setupGrid(self):
        # set every other cell to the path
        for i in range(0, height):
            for j in range(0, width):
                if(not (i % 2 == 0 or j % 2 == 0)):
                    self.grid[i, j] = self.path

    # generate maze using Kruskal's algorithm. TBH I just let Copilot do this one lol.
    def kruskals(self):
        pass
    
    # generate the maze using the recursive backtracker algorithm. Iterative version
    def recursiveBacktracker(self, duration = 30):
        images = []
        output_array = np.zeros((height, width, 3), dtype=np.uint8)
        # stack to keep track of the cells to unvisited
        stack = []
        # set of visited cells
        visited = set()
        # start at a random cell
        x = random.randint(0, height - 1)
        y = random.randint(0, width - 1)
        # make sure the cell is odd. to make sure it is a path
        if(x % 2 == 0):
            x += 1
        if(y % 2 == 0):
            y += 1
        # push the cell to the stack
        stack.append((x, y))
        # mark the cell as visited
        visited.add((x, y))

        # while the stack is not empty
        while(len(stack) > 0):
            # pop the top cell
            x, y = stack.pop()
            # get the neighbors of the cell with a horizontal bias
            neighbors = self.getNeighbors(x, y, visited)
            # if the cell has any neighbors
            if(len(neighbors) > 0):
                # push the cell to the stack
                stack.append((x, y))
                # choose a random neighbor but weight it horizontally. naive implementation
                if(random.randint(0, 1) <= 0.95):
                    x2, y2 = neighbors[random.randint(0, len(neighbors)//2)]
                else:
                    x2, y2 = neighbors[random.randint(len(neighbors)//2, len(neighbors)-1)]

                x2, y2 = random.choice(neighbors)
                # remove the wall between the cell and the neighbor
                self.grid[(x + x2) // 2, (y + y2) // 2] = self.path
                
                
                output_array[(x + x2) // 2, (y + y2) // 2] = (100, 149, 237)
                output_array[x, y] = (100, 149, 237)
                output_array[x2, y2] = (100, 149, 237)

                # push the neighbor to the stack
                stack.append((x2, y2))
                # mark the neighbor as visited
                visited.add((x2, y2))

                # pad the output array to sive 64x64 with (0, 0 ,0) (black)
                padded_output_array = np.zeros((64, 64, 3), dtype=np.uint8)
                padded_output_array[1:height+1, 1:width+1] = output_array

                images.append(Image.fromarray(padded_output_array.astype('uint8'), 'RGB'))

        # duplicate the last frame for 30 frames
        for _ in range(0, 30):
            images.append(images[-1])

        return self.saveGrid(images, duration, self.toString())
    
    # get the neighbors of a cell that's not a wall and is not in visited
    def getNeighbors(self, x, y, visited):
        neighbors = []
        # check the cell to the right
        if(x + 2 < height and self.grid[x + 2, y] == self.path and (x + 2, y) not in visited):
            neighbors.append((x + 2, y))
        # check the cell to the left
        if(x - 2 > 0 and self.grid[x - 2, y] == self.path and (x - 2, y) not in visited):
            neighbors.append((x - 2, y))
        # check the cell above
        if(y - 2 > 0 and self.grid[x, y - 2] == self.path and (x, y - 2) not in visited):
            neighbors.append((x, y - 2))
        # check the cell below
        if(y + 2 < width and self.grid[x, y + 2] == self.path and (x, y + 2) not in visited):
            neighbors.append((x, y + 2))
        return neighbors
    
    def generateFrames(self, duration=50, numframes=100):
        self.setupGrid()
        return self.recursiveBacktracker(duration=duration)

    def toString(self):
        return "Maze Generator"
