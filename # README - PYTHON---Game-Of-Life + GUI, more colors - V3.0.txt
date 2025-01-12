CHATGPT CONVERSATION

*********


You said:
make this game more colorful with GUI added settings

*********

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
ChatGPT said:
ChatGPT
Here’s a revised and enhanced version of your game that adds more colorful GUI elements and a settings menu for adjusting parameters like speed, cell size, and grid reset options. The settings are accessible via a button and displayed in a user-friendly overlay.

python
Copy code
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
LIGHT_BLUE = (100, 180, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

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
show_settings = False


def draw_grid(surface, grid):
    for r in range(rows):
        for c in range(cols):
            color = WHITE if grid[r][c] == 1 else BLACK
            pygame.draw.rect(surface, color, (c * cell_size, r * cell_size, cell_size, cell_size))


def update_grid(grid):
    new_grid = np.copy(grid)
    for r in range(rows):
        for c in range(cols):
            neighbors = np.sum(grid[r - 1:r + 2, c - 1:c + 2]) - grid[r][c]
            if grid[r][c] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[r][c] = 0
            elif grid[r][c] == 0 and neighbors == 3:
                new_grid[r][c] = 1
    return new_grid


def draw_button(surface, text, rect, color, text_color):
    pygame.draw.rect(surface, color, rect, border_radius=5)
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


def toggle_simulation(state):
    global running_simulation
    running_simulation = state


def toggle_settings():
    global show_settings
    show_settings = not show_settings


def draw_settings_overlay():
    overlay_rect = pygame.Rect(50, 50, 700, 400)
    pygame.draw.rect(screen, LIGHT_BLUE, overlay_rect, border_radius=10)
    font = pygame.font.Font(None, 36)
    settings_text = font.render("Settings", True, BLACK)
    screen.blit(settings_text, (overlay_rect.x + 300, overlay_rect.y + 20))

    # Speed adjustment
    speed_text = font.render(f"Speed: {speed} FPS", True, BLACK)
    screen.blit(speed_text, (overlay_rect.x + 50, overlay_rect.y + 100))
    draw_button(screen, "+", pygame.Rect(overlay_rect.x + 200, overlay_rect.y + 95, 50, 40), GREEN, WHITE)
    draw_button(screen, "-", pygame.Rect(overlay_rect.x + 260, overlay_rect.y + 95, 50, 40), RED, WHITE)

    # Cell size adjustment
    size_text = font.render(f"Cell Size: {cell_size}", True, BLACK)
    screen.blit(size_text, (overlay_rect.x + 50, overlay_rect.y + 200))
    draw_button(screen, "+", pygame.Rect(overlay_rect.x + 200, overlay_rect.y + 195, 50, 40), GREEN, WHITE)
    draw_button(screen, "-", pygame.Rect(overlay_rect.x + 260, overlay_rect.y + 195, 50, 40), RED, WHITE)


def adjust_speed(increase):
    global speed
    speed = max(1, speed + (1 if increase else -1))


def adjust_cell_size(increase):
    global cell_size, cols, rows, grid
    cell_size = max(5, cell_size + (1 if increase else -1))
    cols = width // cell_size
    rows = height // cell_size
    reset_grid()


# Buttons
start_button = {"rect": pygame.Rect(10, height - 60, 120, 40), "text": "Start", "action": lambda: toggle_simulation(True)}
stop_button = {"rect": pygame.Rect(140, height - 60, 120, 40), "text": "Stop", "action": lambda: toggle_simulation(False)}
reset_button = {"rect": pygame.Rect(270, height - 60, 120, 40), "text": "Reset", "action": reset_grid}
settings_button = {"rect": pygame.Rect(400, height - 60, 120, 40), "text": "Settings", "action": toggle_settings}
buttons = [start_button, stop_button, reset_button, settings_button]

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

    # Draw settings overlay
    if show_settings:
        draw_settings_overlay()
        # Handle speed adjustments
        if pygame.Rect(250, 145, 50, 40).collidepoint(mouse_pos) and mouse_click[0]:
            adjust_speed(True)
        elif pygame.Rect(310, 145, 50, 40).collidepoint(mouse_pos) and mouse_click[0]:
            adjust_speed(False)

        # Handle cell size adjustments
        if pygame.Rect(250, 245, 50, 40).collidepoint(mouse_pos) and mouse_click[0]:
            adjust_cell_size(True)
        elif pygame.Rect(310, 245, 50, 40).collidepoint(mouse_pos) and mouse_click[0]:
            adjust_cell_size(False)

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(speed)

pygame.quit()
Features Added:
Settings Menu: Access via the "Settings" button to adjust game speed and cell size dynamically.
Colorful GUI: Enhanced buttons and an attractive settings overlay.
Interactive Controls: Increment and decrement buttons for speed and cell size adjustments.
This version makes the game more visually engaging and interactive while providing customization options for the user.
