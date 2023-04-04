import math
import random
import time
import numpy as np
from samplebase import SampleBase





HEIGHT = 64
WIDTH = 64

class Wave(SampleBase):

    def __init__(self, *args, **kwargs):
        self.grid = self.initializeGrid()
        super(Wave, self).__init__(*args, **kwargs)

    def initializeGrid(self):
        grid = np.zeros((HEIGHT, WIDTH))
        for i in range(HEIGHT):
            for j in range(WIDTH):
                grid[i, j] = 0.1 + 0.1 * random.random()
        return grid

    def update(self):
        lastMap = self.grid.copy()

        for i in range(HEIGHT):
            for j in range(WIDTH):
                lastValue = lastMap[i, j]

                self.grid[i, j] = lastValue * (0.96 + 0.02 * random.random())

                if(lastValue <= (0.18 + 0.04 * random.random())):
                    n = 0

                    for u in range(-1, 2):
                        for v in range(-1, 2):
                            if(u == 0 and u == 0):
                                continue

                            nj = abs((j + u) % WIDTH)
                            ni = abs((i + v) % HEIGHT)

                            nLastValue = lastMap[ni, nj]

                            if nLastValue >= (0.5 + 0.04 * random.random()):
                                n += 1
                                self.grid[i, j] += nLastValue * (0.8 + 0.4 * random.random())

                    if(n > 0):
                        self.grid[i, j] *= 1 / n

                    self.grid[i, j] = min(self.grid[i, j], 1)
            
    def paint(self):
        color_grid = np.zeros((HEIGHT, WIDTH, 3))
        for i in range(HEIGHT):
            for j in range(WIDTH):
                r = 255 * pow(self.grid[i, j], 4 + (self.grid[i, j] * 0.5)) * math.cos(self.grid[i, j])
                g = 255 * pow(self.grid[i, j], 3 + (self.grid[i, j] * 0.5)) * math.sin(self.grid[i, j])
                b = 255 * pow(self.grid[i, j], 2 + (self.grid[i, j] * 0.5))
                color_grid[i, j] = [r, g, b]

        return color_grid
    
    def  generateFrames(self):
        offset_canvas = self.matrix.CreateFrameCanvas()

        while True:
            self.update()
            color_grid = self.paint()
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    r = int(color_grid[i, j, 0])
                    g = int(color_grid[i, j, 1])
                    b = int(color_grid[i, j, 2])
                    offset_canvas.SetPixel(j, i, r, g, b)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
    

wave = Wave()

# offset_canvas = self.matrix.CreateFrameCanvas()


