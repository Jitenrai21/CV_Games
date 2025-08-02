import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Define screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snap It - Eclipse Observation")

# Load assets for the objects
asteroid_image = pygame.image.load('asteroid.png')  # Replace with the path to your asteroid image
satellite_image = pygame.image.load('satellite.png')  # Replace with the path to your satellite image
planet_image = pygame.image.load('planet.png')  # Replace with the path to your planet image
moon_image = pygame.image.load('moon.png')  # Replace with the path to your moon image

# Load assets for sun and lens overlay
background_image = pygame.image.load('sun.png')  # Replace with the path to your sun background
lens_overlay = pygame.image.load('overlay.png')  # Replace with the path to your camera lens overlay

# Resize the lens overlay to match the lens size
lens_overlay = pygame.transform.smoothscale(lens_overlay, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to match radius

# Set initial zoom level (scale factor)
zoom_level = 1.0

# Set initial lens position (centered in the screen initially)
lens_radius = 240
lens_x = (SCREEN_WIDTH - lens_radius * 2) // 2
lens_y = (SCREEN_HEIGHT - lens_radius * 2) // 2

# Animation variables for rotation
angle = 0  # Initial angle for rotation
rotation_speed = 1  # Speed of the rotation

# Define the object class with movement and scaling logic
class EclipseObject:
    def __init__(self, image, size, speed, x, y, name=None):
        self.image = image
        self.original_size = size  # Store the original size for scaling
        self.speed = speed
        self.x = x
        self.y = y
        self.name = name  # Optional name (for planet)
        self.angle = random.uniform(0, 2 * math.pi)  # Random angle in radians (0 to 2π)
        self.speed_x = self.speed * math.cos(self.angle)  # X component of speed (calculated from angle)
        self.speed_y = self.speed * math.sin(self.angle)  # Y component of speed (calculated from angle)

        # Set initial size based on zoom level
        self.size = int(self.original_size * zoom_level)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def move(self):
        # Move the object in the direction of its velocity components (speed_x, speed_y)
        self.x += self.speed_x
        self.y += self.speed_y

        # Wrap the object around the screen when it goes out of bounds
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

    def draw(self):
        # Draw the object on the screen
        screen.blit(self.image, (self.x, self.y))

    def update_size(self, new_size):
        self.size = new_size
        self.image = pygame.transform.scale(self.image, (new_size, new_size))

    def randomize(self):
        """Randomize the object’s properties."""
        # Randomize speed and direction
        self.speed = random.randint(1, 6)  # Random speed
        self.angle = random.uniform(0, 2 * math.pi)  # Random direction
        self.speed_x = self.speed * math.cos(self.angle)  # Update X speed component
        self.speed_y = self.speed * math.sin(self.angle)  # Update Y speed component

        # Randomize position within screen boundaries
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)

        # Scale the object relative to the zoom level
        self.size = int(self.original_size * zoom_level)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))


# Create eclipse objects: asteroid, satellite, planet, and moon
objects = [
    EclipseObject(asteroid_image, 50, random.randint(1, 3), random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
    EclipseObject(satellite_image, 40, random.randint(2, 5), random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
    EclipseObject(planet_image, 60, random.randint(1, 2), random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), name="Venus"),
    EclipseObject(moon_image, 100, random.randint(3, 6), random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
]

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

    # Ensure lens_rect is within bounds of the zoomed background
    lens_rect.width = min(lens_rect.width, zoomed_background.get_width() - lens_rect.x)
    lens_rect.height = min(lens_rect.height, zoomed_background.get_height() - lens_rect.y)

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
    lens_x = max(0, min(lens_x, zoomed_background.get_width() - SCREEN_WIDTH))
    lens_y = max(0, min(lens_y, zoomed_background.get_height() - SCREEN_HEIGHT))

    # Move and draw each object
    for obj in objects:
        obj.move()  # Move the object
        obj.draw()  # Draw the object

        # Logic for the moon to sometimes cover the sun completely (simulate full eclipse)
        if obj.name is None and random.random() < 0.01:  # Random chance for moon to cover the sun
            if obj.image == moon_image:
                obj.update_size(200)  # Make the moon large enough to cover the sun

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
