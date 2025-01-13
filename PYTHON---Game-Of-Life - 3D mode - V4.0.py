import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life - 3D Mode")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 120, 215)
LIGHT_BLUE = (100, 180, 255)

# Size of each cell
cell_size = 10

# Number of cells in the grid
cols = width // cell_size
rows = height // cell_size
layers = 10  # Depth for the 3D grid

# Initialize the 3D grid with random 0s and 1s
grid_3d = np.random.choice([0, 1], size=(layers, rows, cols), p=[0.8, 0.2])

# Game state variables
running_simulation = False
speed = 10
show_settings = False
is_3d_mode = False  # Flag for 3D mode
current_layer = 0  # Active layer to view in 3D mode


def draw_grid(surface, grid):
    for r in range(rows):
        for c in range(cols):
            color = WHITE if grid[r][c] == 1 else BLACK
            pygame.draw.rect(surface, color, (c * cell_size, r * cell_size, cell_size, cell_size))


def draw_3d_grid(surface, grid_3d, current_layer):
    for r in range(rows):
        for c in range(cols):
            depth_color = int((current_layer / layers) * 255)
            color = (depth_color, depth_color, 255) if grid_3d[current_layer, r, c] == 1 else BLACK
            pygame.draw.rect(surface, color, (c * cell_size, r * cell_size, cell_size, cell_size))


def update_grid_3d(grid):
    new_grid = np.copy(grid)
    for z in range(layers):
        for r in range(rows):
            for c in range(cols):
                neighbors = np.sum(grid[max(0, z-1):min(layers, z+2), max(0, r-1):min(rows, r+2), max(0, c-1):min(cols, c+2)]) - grid[z, r, c]
                if grid[z, r, c] == 1 and (neighbors < 2 or neighbors > 3):
                    new_grid[z, r, c] = 0
                elif grid[z, r, c] == 0 and neighbors == 3:
                    new_grid[z, r, c] = 1
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


def reset_grid_3d():
    global grid_3d
    grid_3d = np.random.choice([0, 1], size=(layers, rows, cols), p=[0.8, 0.2])


def toggle_simulation(state):
    global running_simulation
    running_simulation = state


def toggle_3d_mode():
    global is_3d_mode
    is_3d_mode = not is_3d_mode


def change_layer(direction):
    global current_layer
    current_layer = (current_layer + direction) % layers

# Buttons
start_button = {"rect": pygame.Rect(10, height - 60, 120, 40), "text": "Start", "action": lambda: toggle_simulation(True)}
stop_button = {"rect": pygame.Rect(140, height - 60, 120, 40), "text": "Stop", "action": lambda: toggle_simulation(False)}
reset_button = {"rect": pygame.Rect(270, height - 60, 120, 40), "text": "Reset", "action": reset_grid_3d}
mode_button = {"rect": pygame.Rect(400, height - 60, 120, 40), "text": "Toggle 3D", "action": toggle_3d_mode}
buttons = [start_button, stop_button, reset_button, mode_button]

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if is_3d_mode:
                if event.key == pygame.K_UP:
                    change_layer(-1)
                elif event.key == pygame.K_DOWN:
                    change_layer(1)

    if running_simulation:
        grid_3d = update_grid_3d(grid_3d)

    # Draw everything
    screen.fill(GRAY)
    if is_3d_mode:
        draw_3d_grid(screen, grid_3d, current_layer)
    else:
        draw_grid(screen, grid_3d[0])

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
