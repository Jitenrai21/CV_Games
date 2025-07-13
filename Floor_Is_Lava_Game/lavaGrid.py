import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Grid settings
ROWS = 5
COLS = 6
CELL_SIZE = 120
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE

# Colors
SAFE_COLOR = (0, 200, 0)
LAVA_COLOR = (255, 50, 50)
FALLEN_COLOR = (100, 100, 100)
GRID_LINE_COLOR = (0, 0, 0)

# Create window
screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
pygame.display.set_caption("The Floor is Lava - Grid System")

# Create grid with states
# State: "safe", "lava", "fallen"
grid = [["safe" for _ in range(COLS)] for _ in range(ROWS)]

# Timer for lava updates
LAVA_INTERVAL = 2  # seconds
last_lava_time = time.time()

# Game loop
running = True
clock = pygame.time.Clock()

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            # Cell color
            state = grid[row][col]
            if state == "safe":
                color = SAFE_COLOR
            elif state == "lava":
                color = LAVA_COLOR
            elif state == "fallen":
                color = FALLEN_COLOR

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRID_LINE_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 2)

def update_lava_cells():
    # Reset all lava cells back to safe or fallen
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == "lava":
                grid[row][col] = "fallen"

    # Choose new random cells to become lava
    lava_count = random.randint(1, 3)
    for _ in range(lava_count):
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        grid[row][col] = "lava"

while running:
    screen.fill((255, 255, 255))  # Background white

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lava update based on interval
    current_time = time.time()
    if current_time - last_lava_time > LAVA_INTERVAL:
        update_lava_cells()
        last_lava_time = current_time

    draw_grid()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()