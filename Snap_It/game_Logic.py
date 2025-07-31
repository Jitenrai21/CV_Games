import pygame
import sys

# Initialize Pygame
pygame.init()

# Define screen size (this is determined by the lens overlay size)
lens_radius = 240  # Set the radius of the lens overlay
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snap It - Eclipse Observation")

# Load assets
background_image = pygame.image.load('sun.png')  # Replace with the path to your sun background
lens_overlay = pygame.image.load('overlay.png')  # Replace with the path to your camera lens overlay

# Resize the background image to simulate zoomed-in view (adjust as needed)
background_width, background_height = background_image.get_size()

# Resize the lens overlay to match the lens size
lens_overlay = pygame.transform.smoothscale(lens_overlay, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to match radius

# Set initial lens position (centered in the screen initially)
lens_x = (SCREEN_WIDTH - lens_radius * 2) // 2
lens_y = (SCREEN_HEIGHT - lens_radius * 2) // 2

# Initialize clock for controlling frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Calculate the portion of the background visible inside the lens (zoomed-in view)
    lens_view = background_image.subsurface(pygame.Rect(lens_x, lens_y, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Draw the cropped portion of the background inside the lens (zoomed-in area)
    screen.blit(lens_view, (0, 0))  # Draw only the area visible through the lens overlay

    # Draw the lens overlay (boundary view) on top of the background view
    screen.blit(lens_overlay, (0, 0))  # Lens stays fixed at the center, showing the zoomed-in area of the background

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move the lens based on cursor position at the screen edges
    # Set movement speed
    speed = 5  # Controls how fast the lens moves

    # Left edge
    if mouse_x <= 200:  # Cursor on the left side of the screen
        lens_x -= speed
    # Right edge
    elif mouse_x >= SCREEN_WIDTH - 200:  # Cursor on the right side of the screen
        lens_x += speed

    # Top edge
    if mouse_y <= 200:  # Cursor on the top of the screen
        lens_y -= speed
    # Bottom edge
    elif mouse_y >= SCREEN_HEIGHT - 200:  # Cursor on the bottom of the screen
        lens_y += speed

    # Keep the lens inside the bounds of the background image
    lens_x = max(0, min(lens_x, background_width - lens_radius * 2))
    lens_y = max(0, min(lens_y, background_height - lens_radius * 2))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
