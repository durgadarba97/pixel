import math
import random
import time
import numpy as np
from PIL import Image
from configs import height, width
from pixel.state import State

class Wave(State):

    def update(self):
        lastMap = self.grid.copy()

        for i in range(height):
            for j in range(width):
                lastValue = lastMap[i, j]

                self.grid[i, j] = lastValue * (0.96 + 0.02 * random.random())

                if(lastValue <= (0.18 + 0.04 * random.random())):
                    n = 0

                    for u in range(-1, 2):
                        for v in range(-1, 2):
                            if(u == 0 and u == 0):
                                continue

                            nj = abs((j + u) % width)
                            ni = abs((i + v) % height)

                            nLastValue = lastMap[ni, nj]

                            if nLastValue >= (0.5 + 0.04 * random.random()):
                                n += 1
                                self.grid[i, j] += nLastValue * (0.8 + 0.4 * random.random())

                    if(n > 0):
                        self.grid[i, j] *= 1 / n

                    self.grid[i, j] = min(self.grid[i, j], 1)
        
    def generateFrames(self, numframes = 5000, duration = 50):
        self.initializeWeightedGrid()

        images = []
        for _ in range(numframes):
            self.update()
            # save the image
            img = Image.fromarray(self.paint().astype('uint8'), 'RGB')
            images.append(img)

        return self.saveGrid(images, duration, self.toString())
        
    def toString(self):
        return "wave"
            
    def paint(self):
        color_grid = np.zeros((height, width, 3))
        for i in range(height):
            for j in range(width):
                r = 255 * pow(self.grid[i, j], 4 + (self.grid[i, j] * 0.5)) * math.cos(self.grid[i, j])
                g = 255 * pow(self.grid[i, j], 3 + (self.grid[i, j] * 0.5)) * math.sin(self.grid[i, j])
                b = 255 * pow(self.grid[i, j], 2 + (self.grid[i, j] * 0.5))
                color_grid[i, j] = [r, g, b]

        return color_grid
