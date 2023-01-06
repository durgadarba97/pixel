import numpy as np
from PIL import Image

def create_mandelbrot(width, height, xmin, xmax, ymin, ymax, max_iter):
  # Create a NumPy array to store the values of the Mandelbrot set
  mandelbrot_set = np.empty((width, height))

  # Set the pixel values of the Mandelbrot set
  for x in range(width):
    for y in range(height):
      # Convert the pixel coordinates to complex numbers
      c = complex(x * (xmax - xmin) / (width - 1) + xmin, y * (ymax - ymin) / (height - 1) + ymin)

      # Iterate the Mandelbrot function to determine the value of the point
      z = 0
      for i in range(max_iter):
        if abs(z) > 2:
          break
        z = z**2 + c
      
      # Store the number of iterations in the Mandelbrot set array
      mandelbrot_set[x, y] = i

  return mandelbrot_set

# Set the dimensions of the Mandelbrot set
width = 500
height = 500

# Set the maximum number of iterations
max_iter = 256

# Set the initial values of the Mandelbrot set
xmin = -2
xmax = 1
ymin = -1
ymax = 1

# Create an image to store the frames of the animation
image = Image.new("RGB", (width, height))

# Create a loop to update the Mandelbrot set at each frame
for i in range(100):
  # Generate the Mandelbrot set
  mandelbrot_set = create_mandelbrot(width, height, xmin, xmax, ymin, ymax, max_iter)

  # Convert the Mandelbrot set to an image
  mandelbrot_image = Image.fromarray(np.uint8(mandelbrot_set))

  # Paste the image into the animation
  image.paste(mandelbrot_image)

  # Update the values of the Mandelbrot set
  xmin += 0.1
  xmax += 0.1
  ymin += 0.1
  ymax += 0.1

# Save
image.save("mandelbrot.png", save_all=True, append_images=[image], duration=100, loop=0)

# '''
# class Mendelbrot():

#     # def getOutputFilePath(self):
#     #   return mendelbrot_path
    
#     def update(self):
#       pass

#     def mendelbrot(self):
#       for i in range(10):
#         print(self.z(i, 1))

      
#     def z(self, n, c):
#       if(not n):
#         return 0
      
#       return self.z(n-1, c) ** 2 + c


# def test():
#   m = Mendelbrot()
#   m.mendelbrot()

# test()
# '''