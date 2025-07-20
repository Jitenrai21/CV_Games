import pygame, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.configs import *
pygame.init()

# Function to display text on the screen
def display_text(text, x, y, font_size=30):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (x, y))

# Function to draw the logo in the top-right corner
def draw_logo(surface, logo_img):
    logo_width, logo_height = logo_img.get_size()  # Get the dimensions of the logo
    logo_x = screen_width - logo_width - 20        # Position 20px from the right edge
    logo_y = 20                                    # Position 20px from the top edge

    # Create a glow effect around the logo (optional)
    glow = pygame.Surface((logo_width + 10, logo_height + 10), pygame.SRCALPHA)
    glow.fill((255, 255, 255, 0))  # Semi-transparent white glow
    surface.blit(glow, (logo_x - 5, logo_y - 5))  # Draw glow behind the logo
    surface.blit(logo_img, (logo_x, logo_y))  # Draw the actual logo

# Function to display text with a semi-transparent background at the center of the screen
def display_text_with_background(surface, text, font_size=30):
    # Set up the font and text
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, TEXT_COLOR)
    
    # Get the width and height of the text
    text_width, text_height = text_surface.get_size()

    # Calculate the position to center the text
    text_x = (screen_width - text_width) // 2
    text_y = (screen_height - text_height) // 1.2

    # Create a semi-transparent background for the text
    background_color = (0, 0, 0, 50)  # Black with some transparency (0-255)
    background = pygame.Surface((text_width + 20, text_height + 20), pygame.SRCALPHA)  # Extra space for padding
    background.fill(background_color)

    # Draw the background and then the text
    surface.blit(background, (text_x - 10, text_y - 10))  # Offset the background for padding
    surface.blit(text_surface, (text_x, text_y))  # Place text on top of the background

# Function to display guideline text with a curved background and optional image
def display_text_with_logo_image(surface, text, image, font_size=60):
    # Set up the font and text
    font = pygame.font.SysFont("Impact", font_size)
    text_surface = font.render(text, True, TEXT_COLOR)
    
    # Get the width and height of the text
    text_width, text_height = text_surface.get_size()

    # Get the size of the image
    image_width, image_height = image.get_size()

    # Set padding between the text and the image
    padding = 10

    # Calculate the background size (text width + image width + padding)
    background_width = text_width + image_width + padding
    background_height = max(text_height, image_height) + 10  # Ensure enough space for both text and image

    # Calculate the position of the background to center it on the screen
    background_x = (screen_width - background_width) // 2
    background_y = 20

    # Create the semi-transparent background
    background_color = (0, 0, 0, 50)  # Black with transparency
    background = pygame.Surface((background_width + 10, background_height), pygame.SRCALPHA)
    background.fill(background_color)

    # Draw the background
    surface.blit(background, (background_x, background_y))

    # Position the image inside the rectangle
    image_x = background_x + text_width + padding  # Position image next to the text
    image_y = background_y + (background_height - image_height) // 2  # Center the image vertically within the background
    surface.blit(image, (image_x, image_y))

    # Position the text inside the rectangle
    text_x = background_x + 20  # Shift text by padding_left
    text_y = background_y + (background_height - text_height) // 2  # Center text vertically within the background
    surface.blit(text_surface, (text_x, text_y))
