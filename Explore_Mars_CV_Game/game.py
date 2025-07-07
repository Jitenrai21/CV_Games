import pygame
import cv2
import numpy as np
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions and setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mars Rover Exploration")

# Colors
WHITE = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)  # White for text

# Load the background image and rover image (your processed image and rover PNG)
background_image = pygame.image.load('explore_mars_background.png')  # Make sure to put your image path here
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Resize to fit the screen

rover_image = pygame.image.load('rover.png')  # Rover PNG image path
rover_image = pygame.transform.scale(rover_image, (100, 100))  # Resize rover to appropriate size

# Initial rover position
rover_x, rover_y = screen_width // 2, screen_height // 2
rover_speed = 5

# Coordinates for bounding boxes (stones and pitholes) from your previous input
stone_coords = [
    (54, 180, 112, 202),
    (115, 239, 173, 266),
    (193, 344, 241, 368),
    (38, 387, 83, 410),
    (111, 507, 177, 538)
]

pithole_coords = [
    (468, 279, 717, 333),
    (437, 398, 720, 463)
]

# Facts about the stones and pitholes
stone_facts = [
    "Mars rocks are rich in iron oxide, giving Mars its red color.",
    "Mars rocks are believed to have formed billions of years ago.",
    "Some rocks on Mars are believed to have been formed by ancient water.",
    "Mars has a history of volcanic activity, and some rocks are remnants of volcanic lava.",
    "Some Martian rocks show evidence of past impact events from meteorites."
]

pithole_facts = [
    "Pitholes on Mars are likely remnants of ancient volcanic activity.",
    "These pits may have formed from gas bubbles in volcanic rocks.",
    "Some pitholes could be the result of Martian seismic activity.",
    "Pitholes can help scientists understand Mars' geologic history.",
    "The formation of pitholes may provide clues about the ancient atmosphere on Mars."
]

# Function to check if the rover is inside any bounding box
def check_for_collision(rover_rect, object_coords):
    for (start_x, start_y, end_x, end_y) in object_coords:
        object_rect = pygame.Rect(start_x, start_y, end_x - start_x, end_y - start_y)
        if rover_rect.colliderect(object_rect):
            return True
    return False

# Function to display text on the screen
def display_text(text, x, y, font_size=30):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (x, y))

# Variables to handle display duration and randomization
last_display_time = 0
display_duration = 3000  # Time to display facts (in milliseconds)
current_fact = ""
fact_displayed = False

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)  # Fill the screen with white before drawing the background

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the rover image at its current position
    screen.blit(rover_image, (rover_x, rover_y))

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses for movement
    keys = pygame.key.get_pressed()

    # Rover movement control (up, down, left, right)
    if keys[pygame.K_UP]:
        rover_y -= rover_speed
    if keys[pygame.K_DOWN]:
        rover_y += rover_speed
    if keys[pygame.K_LEFT]:
        rover_x -= rover_speed
    if keys[pygame.K_RIGHT]:
        rover_x += rover_speed

    # Make sure the rover doesn't go out of bounds
    rover_x = max(0, min(rover_x, screen_width - rover_image.get_width()))
    rover_y = max(0, min(rover_y, screen_height - rover_image.get_height()))

    # Handle spacebar press to trigger analysis
    if keys[pygame.K_SPACE]:
        rover_rect = pygame.Rect(rover_x, rover_y, rover_image.get_width(), rover_image.get_height())

        # Check for collision with stones or pitholes and display the relevant facts
        if check_for_collision(rover_rect, stone_coords):
            index = stone_coords.index(next(coord for coord in stone_coords if pygame.Rect(coord).colliderect(rover_rect)))
            current_fact = random.choice(stone_facts)
            fact_displayed = True
            last_display_time = pygame.time.get_ticks()
        elif check_for_collision(rover_rect, pithole_coords):
            index = pithole_coords.index(next(coord for coord in pithole_coords if pygame.Rect(coord).colliderect(rover_rect)))
            current_fact = random.choice(pithole_facts)
            fact_displayed = True
            last_display_time = pygame.time.get_ticks()
        else:
            current_fact = "Keep exploring for more beneficial results!"
            fact_displayed = True
            last_display_time = pygame.time.get_ticks()

    # Display the fact if it's within the display time limit
    if fact_displayed:
        elapsed_time = pygame.time.get_ticks() - display_duration
        display_text(current_fact, 20, 500)
        if pygame.time.get_ticks() - last_display_time > display_duration:
            fact_displayed = False

    # Update the screen
    pygame.display.flip()

    # Limit the frames per second
    clock.tick(60)

# Quit pygame
pygame.quit()
