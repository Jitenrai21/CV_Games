import pygame
import os

# Initialize pygame just for image handling
pygame.init()

# Dummy video mode for convert_alpha
pygame.display.set_mode((1, 1))

# Settings
FRAME_COUNT = 6
OUTPUT_DIR = "break_frames"

# Load crack image
crack_img = pygame.image.load("crack.png").convert_alpha()
WIDTH, HEIGHT = crack_img.get_size()

# Create output dir if needed
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate frames
for i in range(FRAME_COUNT):
    alpha = int(255 * (1 - (i + 1) / FRAME_COUNT))  # Fade out

    # Copy the original
    frame = crack_img.copy()
    frame.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)

    # Save the frame
    pygame.image.save(frame, os.path.join(OUTPUT_DIR, f"break_{i+1}.png"))

print(f"Saved {FRAME_COUNT} frames in '{OUTPUT_DIR}'")
pygame.quit()