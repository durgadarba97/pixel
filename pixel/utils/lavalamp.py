import curses
import random
import time

# Initialize the screen
screen = curses.initscr()

# Set the screen size
screen.resize(64, 64)

# Set the cursor to be invisible
curses.curs_set(0)

# Create an empty list to store the "lava"
lava = []

# get screen height and width
screen_height = screen.getmaxyx()[0]
screen_width = screen.getmaxyx()[1]

# Fill the screen with spaces
for y in range(screen_height):
    lava.append([" "] * screen_width)

# Generate some random "lava"
for i in range(50):
    x = random.randint(0, screen_width - 1)
    y = random.randint(0, screen_height - 1)
    lava[y][x] = "X"

# Animate the "lava"
while True:
    # Clear the screen
    screen.clear()

    # Draw the "lava"
    for y in range(screen_height):
        for x in range(screen_width):
            screen.put(lava[y][x], x, y)

    # Update the screen
    screen.refresh()

    # Shift the "lava" down by one
    lava.pop(0)
    lava.append([" "] * screen.width)

    # Generate some random "lava"
    for i in range(5):
        x = random.randint(0, screen.width - 1)
        lava[-1][x] = "X"

    # Wait for a bit
    time.sleep(0.1)
