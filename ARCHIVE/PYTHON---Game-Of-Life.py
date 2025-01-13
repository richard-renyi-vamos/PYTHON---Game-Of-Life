import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Size of each cell
cell_size = 10

# Number of cells in the grid
cols = width // cell_size
rows = height // cell_size

# Initialize the grid with random 0s and 1s
grid = np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])

def draw_grid(surface, grid):
    for r in range(rows):
        for c in range(cols):
            color = WHITE if grid[r][c] == 1 else BLACK
            pygame.draw.rect(surface, color, (c * cell_size, r * cell_size, cell_size, cell_size))

def update_grid(grid):
    # Copy the current grid to calculate the next state
    new_grid = np.copy(grid)
    
    for r in range(rows):
        for c in range(cols):
            # Get the sum of the 8 neighbors
            neighbors = np.sum(grid[r-1:r+2, c-1:c+2]) - grid[r][c]
            
            # Apply the rules of the game
            if grid[r][c] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[r][c] = 0  # Cell dies
            elif grid[r][c] == 0 and neighbors == 3:
                new_grid[r][c] = 1  # Cell becomes alive
    return new_grid

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the grid
    screen.fill(BLACK)
    draw_grid(screen, grid)
    
    # Update the grid to the next generation
    grid = update_grid(grid)
    
    # Update the display
    pygame.display.flip()
    
    # Control the game speed
    clock.tick(10)

pygame.quit()
