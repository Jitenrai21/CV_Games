import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Grid settings
ROWS = 5
COLS = 8
CELL_SIZE = 120
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE

# Set up display
screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
pygame.display.set_caption("The Floor is Lava - Crack and Lava Logic")
clock = pygame.time.Clock()

# Load images
safe_img = pygame.image.load("check.png")
safe_img = pygame.transform.scale(safe_img, (CELL_SIZE, CELL_SIZE))

cracked_img = pygame.image.load("crack.png")
cracked_img = pygame.transform.scale(cracked_img, (CELL_SIZE, CELL_SIZE))

lava_bg = pygame.image.load("lava.png")
lava_bg = pygame.transform.scale(lava_bg, (GRID_WIDTH, GRID_HEIGHT))

# Define grid cell states
# Each cell has: {"state": "safe"/"cracked"/"fallen", "crack_time": timestamp}
grid = [[{"state": "safe", "crack_time": None} for _ in range(COLS)] for _ in range(ROWS)]

# Timing control
CRACK_INTERVAL = 5  # seconds before cracked tiles fall
CYCLE_INTERVAL = 8  # seconds for a full refresh
last_cycle_time = time.time()

def reset_grid():
    for row in range(ROWS):
        for col in range(COLS):
            grid[row][col]["state"] = "safe"
            grid[row][col]["crack_time"] = None

    # Randomly select more tiles to crack
    crack_count = random.randint(33, 35)
    selected = set()
    while len(selected) < crack_count:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)
        if (r, c) not in selected:
            grid[r][c]["state"] = "cracked"
            grid[r][c]["crack_time"] = time.time()
            selected.add((r, c))

def draw_grid():
    # First draw lava background
    screen.blit(lava_bg, (0, 0))

    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            state = grid[row][col]["state"]

            if state == "safe":
                screen.blit(safe_img, (x, y))
            elif state == "cracked":
                screen.blit(cracked_img, (x, y))
            elif state == "fallen":
                # Show lava below (do nothing, lava already drawn)
                continue

            # Draw grid lines
            pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 2)

def update_cracked_tiles():
    current_time = time.time()
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col]["state"] == "cracked":
                elapsed = current_time - grid[row][col]["crack_time"]
                if elapsed > CRACK_INTERVAL:
                    grid[row][col]["state"] = "fallen"

# Initial crack distribution
reset_grid()

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Fill with white first

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update cracked tiles to fallen
    update_cracked_tiles()

    # Restart cycle after defined interval
    if time.time() - last_cycle_time > CYCLE_INTERVAL:
        reset_grid()
        last_cycle_time = time.time()

    draw_grid()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()