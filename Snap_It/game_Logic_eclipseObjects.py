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
asteroid_image = pygame.image.load('asteroid.png')  
satellite_image = pygame.image.load('satellite.png')
planet_image = pygame.image.load('planet.png') 
moon_image = pygame.image.load('moon.png') 

# Load assets for sun and lens overlay
background_image = pygame.image.load('sun.png') 
lens_overlay = pygame.image.load('overlay.png')  

# Resize the lens overlay to match the lens size
lens_overlay = pygame.transform.smoothscale(lens_overlay, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to match radius

# Set initial zoom level (scale factor)
zoom_level = 1.0

# Set initial lens position (centered in the screen initially)
lens_radius = 240
lens_x = (SCREEN_WIDTH - lens_radius * 2) // 2
lens_y = (SCREEN_HEIGHT - lens_radius * 2) // 2

# Define the object class with enhanced movement and scaling logic
class EclipseObject:
    def __init__(self, image, size, speed, x, y, name=None):
        self.image = image
        self.original_size = size  # Store the original size for scaling
        self.speed = speed
        self.x = x
        self.y = y
        self.name = name  # Optional name (for planet)
        
        # Randomize initial angle for orbital movement
        self.angle = random.uniform(0, 2 * math.pi)  # Random angle in radians (0 to 2π)
        
        # Set initial speed based on the angle (speed_x, speed_y)
        self.speed_x = self.speed * math.cos(self.angle)
        self.speed_y = self.speed * math.sin(self.angle)
        
        # Orbiting behavior: Move objects in a more realistic, circular/elliptical motion
        self.orbit_radius = random.randint(150, 300)  # Simulating orbital distance from the center
        self.orbit_angle = random.uniform(0, 2 * math.pi)  # Random starting angle for the orbit
        
        # Set initial size based on zoom level
        self.size = int(self.original_size * 1.0)  # Assume zoom level is 1.0 for now
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        
        # Set orbit speed
        self.orbit_speed = random.uniform(0.5, 2.5)  # Different orbital speeds for each object
        
        # Optional: Add rotation speed for realistic rotation of objects (e.g., moon)
        self.rotation_speed = random.uniform(0.1, 0.5)  # Speed of object rotation
        self.rotation_angle = 0  # Initial rotation angle

    def move(self):
        """Move the object in a circular or elliptical orbit and rotate it."""
        # Update orbit position (circular motion)
        self.orbit_angle += self.orbit_speed  # Increment the orbit angle
        
        # Calculate the new position using polar-to-cartesian conversion
        self.x = SCREEN_WIDTH // 2 + int(self.orbit_radius * math.cos(self.orbit_angle))
        self.y = SCREEN_HEIGHT // 2 + int(self.orbit_radius * math.sin(self.orbit_angle))

        # Update the rotation angle of the object for realistic spinning
        self.rotation_angle += self.rotation_speed
        
        # Keep the object within bounds, but allow it to move freely on the screen
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.reset()  # Reset the position if it moves out of bounds

    def draw(self):
        """Draw the object on the screen with its current rotation."""
        rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)  # Rotate the object
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))  # Get the rotated image's rect
        screen.blit(rotated_image, rotated_rect.topleft)  # Draw the rotated image at the calculated position

    def update_size(self, new_size):
        """Update the size of the object and resize its image accordingly."""
        self.size = new_size
        self.image = pygame.transform.scale(self.image, (new_size, new_size))

    def reset(self):
        """Reset the object's position, speed, and properties randomly."""
        # Randomize speed and direction for more dynamic behavior
        self.speed = random.randint(1, 6)
        self.angle = random.uniform(0, 2 * math.pi)  # Random angle for direction
        self.speed_x = self.speed * math.cos(self.angle)
        self.speed_y = self.speed * math.sin(self.angle)
        
        # Reset the orbit to random parameters
        self.orbit_radius = random.randint(150, 300)
        self.orbit_angle = random.uniform(0, 2 * math.pi)
        self.orbit_speed = random.uniform(0.5, 2.5)  # Varying orbital speed
        
        # Randomize size and position off-screen
        self.x = random.randint(-100, SCREEN_WIDTH + 100)  # Off-screen position
        self.y = random.randint(-100, SCREEN_HEIGHT + 100)
        
        # Update size based on zoom level or reset
        self.size = int(self.original_size * 1.0)  # Reset size
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

# Create eclipse objects: asteroid, satellite, planet, and moon
objects = [
    EclipseObject(asteroid_image, 50, random.randint(1, 3), 0, 0, name="Asteroid"),
    EclipseObject(satellite_image, 40, random.randint(2, 5), 0, 0, name="Satellite"),
    EclipseObject(planet_image, 60, random.randint(1, 2), 0, 0, name="Venus"),
    EclipseObject(moon_image, 100, random.randint(3, 6), 0, 0, name="Moon")
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

    # Draw the full background image (without clipping based on the lens)
    # The background moves regardless of the zoom or lens area
    screen.blit(zoomed_background, (0, 0))  # Draw the zoomed background

    for obj in objects:
        obj.move()  # Move the object
        obj.draw()  # Draw the object
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

     # Move and draw each object
    for obj in objects:
        obj.move()  # Move the object
        obj.draw()  # Draw the object

        # Logic for the moon to sometimes cover the sun completely (simulate full eclipse)
        if obj.name is None and random.random() < 0.01:  # Random chance for moon to cover the sun
            if obj.image == moon_image:
                obj.update_size(200)  # Make the moon large enough to cover the sun

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

            # Handle mouse click for screenshot (left click)
            if event.button == 1:  # Left-click to take a screenshot
                # Save the screen as a PNG file
                pygame.image.save(screen, "screenshot.png")
                print("Screenshot saved as 'screenshot.png'.")

    # Get the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move the lens based on cursor position at the screen edges
    # Set movement speed
    speed = 3  # Controls how fast the lens moves

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

    # Keep the lens inside the bounds of the zoomed background
    lens_x = max(0, min(lens_x, zoomed_background.get_width() - SCREEN_WIDTH))
    lens_y = max(0, min(lens_y, zoomed_background.get_height() - SCREEN_HEIGHT))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
