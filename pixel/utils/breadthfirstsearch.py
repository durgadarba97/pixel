import random
import numpy as np
from pixel.configs import height, width
from PIL import Image

# implements the breadth first search algorithm
class BreadthFirstSearch():
    def __init__(self):
        # initialize the grid. where height and width are defined in config.py
        # each pixel is a tuple size 3 (r, g, b)
        self.grid = np.zeros((height, width, 3))
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.walls = []
    
    # randomly set the starting point, the end point, and the walls
    def random_grid(self):
        # set the starting point to green and set it to be in the top left qudrant of the grid
        self.start_point = (random.randint(0, height // 2), random.randint(0, width // 2))
        self.grid[self.start_point[0], self.start_point[1]] = (0, 255, 0)

        # set the end point to red and set it to be in the bottom right quadrant of the grid
        self.end_point = (random.randint(height // 2, height - 1), random.randint(width // 2, width - 1))
        self.grid[self.end_point[0], self.end_point[1]] = (255, 0, 0)

        #  set wall to be white
        for i in range(height):
            for j in range(width):
                # there is a 10% chance that a pixel will be a wall
                if random.randint(0, 10) == 0:
                    self.grid[i, j] = (255, 255, 255)
                    self.walls.append((i, j))
    
    # get neighbors of a point
    def get_neighbors(self, point):
        neighbors = []
        # for each of the 8 neighbors
        for i in range(-1, 2):
            for j in range(-1, 2):
                # get the coordinates of the neighbor
                col = point[0] + i
                row = point[1] + j

                # if the neighbor is not out of bounds and is not a wall
                if 0 <= col < height and 0 <= row < width and (col, row) not in self.walls:
                    # add the neighbor to the list of neighbors
                    neighbors.append((col, row))
        return neighbors
        
    # update the grid, solve the maze using breadth first search
    def generateframes(self, numframes=0):
        self.random_grid()

        visited = set()
        images = []
        # # for each of the generations
        # for _ in range(numframes):
            
        #     # convert the grid to an image
        #     images.append(Image.fromarray(self.grid, 'RGB'))

        # # return list of images
        # return images

        # add the starting point to the queue
        queue = [self.start_point]
        visited.add(self.start_point)

        # while the queue is not empty
        while queue:
            # get the next point in the queue
            point = queue.pop(0)

            # if we have reached the end point, we are done
            if(point == self.end_point):
                break

            # get the neighbors of the current point
            neighbors = self.get_neighbors(point)

            # for each neighbor
            for neighbor in neighbors:
                # if the neighbor has not been visited
                if(neighbor not in visited):
                    # add the neighbor to the queue
                    queue.append(neighbor)
                    # mark the neighbor as visited
                    visited.add(neighbor)
                    # set the neighbor to be blue
                    self.grid[neighbor[0], neighbor[1]] = (0, 0, 255)
                


            # convert the grid to an image
            images.append(Image.fromarray(self.grid.astype('uint8'), 'RGB'))

        print(len(images))
        images[0].save("../output/bfs.gif", save_all=True, append_images=images[1:], duration=25, loop=0)
        # 3727 frames x 100 ms = 6 minutes and 12.7 seconds
        return "../output/bfs.gif"


def test():
    bfs = BreadthFirstSearch()
    bfs.generateframes()
    # bfs.random_grid()
    # image = Image.fromarray(bfs.grid.astype('uint8'), 'RGB')
    # image.save("../output/bfs.gif")

# test()