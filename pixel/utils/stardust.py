import random
import numpy as np
from configs import height, width
from PIL import Image
from pixel.state import State
import math
import time


# create a 2D water ripple effect
# Algorithm from https://github.com/Knifa/matryx-gl/blob/master/src/scenes/WaveScene.cpp
class Stardust(State):
    def __init__(self):
        super().__init__()

        self.radius = 2
        
    
    def toString(self):
        return "stardust"
        

    def setWeights(self):
        '''
        initial weights
        weights = size = radius * radius
            [ 0 , 0 , 0 , 0 , 0 ]
            [ 0 , 0 , 0 , 0 , 0 ]
            [ 0 , 0 , 0 , 0 , 0 ]
            [ 0 , 0 , 0 , 0 , 0 ]
            [ 0 , 0 , 0 , 0 , 0 ]
        
        '''
        size = self.radius * 2 + 1

        # weights of size radius * radius
        weights = np.zeros((size, size))
        
        # in weights array
        for i in range(size):
            for j in range(size):
                distance = (i - self.radius)**2 + (j - self.radius)**2

                # set weight = (1 / distance)^0.1
                if(distance > 0):
                    # weight = 1 / (distance + 1)
                    # weight = abs(float(math.sin(distance) + math.cos(distance)))
                    weight = math.exp(-distance)
                    # weight = distance
                else:
                    weight = 1
                # scale weight to 0 - 1 as a contiunous function
                # weights[i, j] = weight
                weights[i, j] = weight ** 0.1
        
        # return weights
        return weights

    # evolve the cell
    def generateStep(self, x, y, weights, map):
        c = 0
        n = 0

        val = map[x, y]

        # in radius point within map
        for i in range(-self.radius, self.radius+1):
            for j in range(-self.radius, self.radius+1):
                if(i == 0 and j == 0):
                    continue
                

                # normalize the weights with radius
                normalizedx =  abs((i + x) % height)
                normalizedy =  abs((j + y) % width)

                last_neighbor = map[normalizedx, normalizedy]
                
                # if last neighbor greater than threshold
                if(last_neighbor > random.uniform(0.4, 0.6)):
                    # get weight at radius
                    weight = weights[i + self.radius, j + self.radius]

                    '''
                    best ones:
                        c += last_neighbor* random.uniform(0.9, 1.1) * weight

                        c += last_value2 * (0.25 * math.pow(j, 2) + 0.25 * math.pow(i, 2)) * weight
                        c += last_value2 * (math.pow(math.sin(j), 1) + math.pow(math.cos(i), 1)) * weight
                    '''

                    c += last_neighbor* random.uniform(0.9, 1.1) * weight
                    n += weight
                
                # the cell doesn't evolve but doesn't decay.

        
        if(n > 0):
            val = (val + c) / n
        else:
            val = 1
        # print(val, c, n)
        return np.clip(val , 0.0, 1.0)


    def generateFrames(self, numframes = 1000, duration = 50):
        images = []
        weights = self.setWeights()

        self.initializeWeightedGrid()

        new_grid = np.copy(self.grid)

        # in the grid 
        for _ in range(0, numframes):
            for i in range(height):
                for j in range(width):
                    last_value = self.grid[i, j]

                    # if last value greater than threshold
                    if(last_value < random.uniform(0.1, 0.2)):
                        #  evolve the cell
                        new_grid[i, j] = self.generateStep(i, j, weights, self.grid)
                    else:
                        # decay the cell
                        new_grid[i, j] = last_value * (1 - random.uniform(0.2, 0.5) * (1/30))
                    
                    # clip the value
                    new_grid[i, j] = np.clip(new_grid[i, j], 0.0, 1.0)

            self.grid = np.copy(new_grid)

            # add image
            images.append(Image.fromarray(self.paint(new_grid).astype('uint8'), 'RGB'))
        
        return self.saveGrid(images, duration, self.toString())

    def paint(self, grid):
        # create a color grid
        #  grid is a 2d array of values between 0 and 1
        color_grid = np.zeros((height, width, 3), dtype=np.uint8)

        for i in range(height):
            for j in range(width):
                r = 255 * pow(grid[i, j], 4 + (grid[i, j] * 0.5)) * math.cos(grid[i, j])
                g = 255 * pow(grid[i, j], 3 + (grid[i, j] * 0.5)) * math.sin(grid[i, j])
                b = 255 * pow(grid[i, j], 2 + (grid[i, j] * 0.5))

                color_grid[i, j] = [r, g, b]
        
        return color_grid