'''
parent class to define and mange state.
'''
import numpy as np
from configs import height, width, gifpath
import random
import time
from PIL import Image

class State:
    def __init__(self):
        self.grid = np.zeros((height, width))
        self.color_grid = np.zeros((height, width, 3))
        self.wall = 0
        self.path = 1

        
    def generateFrames(self, duration, numframes):
        pass
    
    # return the directory
    def getOutputFilePath(self, name):
        return gifpath + name + ".gif"

    def toString(self):
        pass

    def update(self):
        pass

    def getGrid(self):
        return self.grid

    def initializeWeightedGrid(self):
        random.seed(time.time())
        for y in range(height):
            for x in range(width):
                self.grid[y, x] = random.random()
    
    def initializeBinaryGrid(self):
        for y in range(height):
            for x in range(width):
                self.grid[y, x] = random.randint(0, 1)

    def saveGrid(self, images, duration, name):
        
        images[0].save(self.getOutputFilePath(name), save_all=True, append_images=images[1:], duration=duration, loop=0)
        return (len(images) * duration, name+".gif")

    
    def paint(self):
        pass



