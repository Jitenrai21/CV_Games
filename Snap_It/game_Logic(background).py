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

# Resize the lens overlay to match the lens size
lens_overlay = pygame.transform.smoothscale(lens_overlay, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to match radius

# Set initial lens position (centered in the screen initially)
lens_x = (SCREEN_WIDTH - lens_radius * 2) // 2
lens_y = (SCREEN_HEIGHT - lens_radius * 2) // 2

# Initial zoom level (scale factor)
zoom_level = 1.0

# Initialize clock for controlling frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Calculate the new zoomed background size and maintain the aspect ratio
    width, height = background_image.get_size()
    new_width = int(width * zoom_level)
    new_height = int(height * zoom_level)
    
    # Resize the background image, preserving the aspect ratio
    zoomed_background = pygame.transform.scale(background_image, (new_width, new_height))

    # Ensure lens position stays within bounds of the zoomed background
    lens_x = max(0, min(lens_x, new_width - SCREEN_WIDTH))
    lens_y = max(0, min(lens_y, new_height - SCREEN_HEIGHT))

    # Calculate the portion of the zoomed-in background visible inside the lens (zoomed-in view)
    lens_rect = pygame.Rect(lens_x, lens_y, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Create the lens view from the zoomed background (subsurface)
    lens_view = zoomed_background.subsurface(lens_rect)

    # Draw the cropped portion of the zoomed-in background inside the lens (zoomed-in area)
    screen.blit(lens_view, (0, 0))  # Draw only the area visible through the lens overlay

    # Draw the lens overlay (boundary view) on top of the background view
    screen.blit(lens_overlay, (0, 0))  # Lens stays fixed at the center, showing the zoomed-in area of the background

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle zooming with mouse scroll
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll Up (zoom in)
                zoom_level = min(3.0, zoom_level + 0.1)  # Zoom in, but don't exceed 3x zoom
            elif event.button == 5:  # Scroll Down (zoom out)
                zoom_level = max(0.5, zoom_level - 0.1)  # Zoom out, but don't go below 0.5x zoom

    # Get the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move the lens based on cursor position at the screen edges
    # Set movement speed
    speed = 5  # Controls how fast the lens moves

    # Left edge
    if mouse_x <= 100:  # Cursor on the left side of the screen
        lens_x -= speed
    # Right edge
    elif mouse_x >= SCREEN_WIDTH - 100:  # Cursor on the right side of the screen
        lens_x += speed

    # Top edge
    if mouse_y <= 100:  # Cursor on the top of the screen
        lens_y -= speed
    # Bottom edge
    elif mouse_y >= SCREEN_HEIGHT - 100:  # Cursor on the bottom of the screen
        lens_y += speed

    # Keep the lens inside the bounds of the zoomed background
    lens_x = max(0, min(lens_x, new_width - SCREEN_WIDTH))
    lens_y = max(0, min(lens_y, new_height - SCREEN_HEIGHT))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
