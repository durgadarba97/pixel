import numpy as np
from configs import height, width
from pixel.state import State
from PIL import Image
import time

# Game of Life
class GameOfLife(State):

    # def getOutputFilePath(self):
    #     return "/home/spliff/PixelBoard/output/gifs/" + self.toString() + ".gif"

    def update(self):
        new_grid = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                state = self.grid[i, j]
                neighbors = self.countNeighbors(i, j)
                if state == 0 and neighbors == 3:
                    new_grid[i, j] = 1
                elif state == 1 and (neighbors < 2 or neighbors > 3):
                    new_grid[i, j] = 0
                else:
                    new_grid[i, j] = state
        self.grid = new_grid

    def countNeighbors(self, x, y):
        neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + height) % height
                row = (y + j + width) % width
                neighbors += self.grid[col, row]
        neighbors -= self.grid[x, y]
        return neighbors

    # a function to color the grid
    def paint(self, grid):
        # create a new grid with the same dimensions
        new_grid = np.zeros((height, width, 3), dtype=np.uint8)
        color = (100, 149, 237)

        # the color of the cell = color[0] * cell_value, color[1] * cell_value, color[2] * cell_value
        # this is how "blue" the cell will be
        for i in range(height):
            for j in range(width):
                new_grid[i, j] = (color[0] * grid[i, j] , color[1] * grid[i, j], color[2] * grid[i, j])
        
        return new_grid


    def generateFrames(self, numframes=5000, duration=100):
        self.initializeBinaryGrid()

        images = []
        # for each of the generations
        for _ in range(numframes):
            self.update()
            # convert the grid to an image
            color_img = Image.fromarray(self.paint(self.grid))
            images.append(color_img)

        return self.saveGrid(images, duration, self.toString())
    
    def toString(self):
        return "gameoflife"

