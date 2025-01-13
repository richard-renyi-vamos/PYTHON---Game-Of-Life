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
GRAY = (50, 50, 50)
BLUE = (0, 120, 215)

# Size of each cell
cell_size = 10

# Number of cells in the grid
cols = width // cell_size
rows = height // cell_size

# Initialize the grid with random 0s and 1s
grid = np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])

# Game state variables
running_simulation = False
speed = 10

def draw_grid(surface, grid):
    for r in range(rows):
        for c in range(cols):
            color = WHITE if grid[r][c] == 1 else BLACK
            pygame.draw.rect(surface, color, (c * cell_size, r * cell_size, cell_size, cell_size))

def update_grid(grid):
    new_grid = np.copy(grid)
    for r in range(rows):
        for c in range(cols):
            neighbors = np.sum(grid[r-1:r+2, c-1:c+2]) - grid[r][c]
            if grid[r][c] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[r][c] = 0
            elif grid[r][c] == 0 and neighbors == 3:
                new_grid[r][c] = 1
    return new_grid

def draw_button(surface, text, rect, color, text_color):
    pygame.draw.rect(surface, color, rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def handle_buttons(mouse_pos, mouse_click, buttons):
    for button in buttons:
        if button["rect"].collidepoint(mouse_pos):
            if mouse_click[0]:  # Left mouse button
                button["action"]()

def reset_grid():
    global grid
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])

# Buttons
start_button = {"rect": pygame.Rect(10, height - 60, 120, 40), "text": "Start", "action": lambda: toggle_simulation(True)}
stop_button = {"rect": pygame.Rect(140, height - 60, 120, 40), "text": "Stop", "action": lambda: toggle_simulation(False)}
reset_button = {"rect": pygame.Rect(270, height - 60, 120, 40), "text": "Reset", "action": reset_grid}
buttons = [start_button, stop_button, reset_button]

def toggle_simulation(state):
    global running_simulation
    running_simulation = state

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if running_simulation:
        grid = update_grid(grid)

    # Draw everything
    screen.fill(GRAY)
    draw_grid(screen, grid)

    # Draw buttons
    for button in buttons:
        draw_button(screen, button["text"], button["rect"], BLUE, WHITE)

    # Handle button actions
    handle_buttons(mouse_pos, mouse_click, buttons)

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(speed)

pygame.quit()
