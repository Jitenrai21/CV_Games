import pygame
import cv2
import mediapipe as mp
import numpy as np
import random
import time
from modules.configs import *
from modules.rover_movement_animation import Particle
from modules.button import Button
from modules.collision_check import check_for_collision
from modules.text_configs import *

# Initialize pygame
pygame.init()

# Initialize the Pygame mixer for sound
pygame.mixer.init()

# Get the base directory of the project
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory

# Define assets directory
assets_dir = os.path.join(base_dir, 'assets')  # Path to the assets folder

# Function to load and scale images
def load_image(image_name, width, height):
    """Helper function to load and scale images"""
    img_path = os.path.join(assets_dir, image_name)  # Build the full image path
    image = pygame.image.load(img_path).convert_alpha()  # Load the image with transparency support
    return pygame.transform.smoothscale(image, (width, height))  # Resize and return the image

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Variables for hand gesture recognition
fist_held = False
last_fist_time = 0
prev_gestures = []

# Time variables for managing the sound cooldown
last_success_time = 0
last_miss_time = 0

# Cooldown duration for playing sounds (in seconds)
sound_cooldown = 1.0  # Allow sound to play again after 1 second

# Function to play the success sound
def play_success_sound():
    global last_success_time  # Keep track of the last time the success sound was played
    current_time = time.time()
    
    # Only play the sound if the cooldown period has passed
    if current_time - last_success_time >= sound_cooldown:
        success_sound.play()
        last_success_time = current_time  # Update the last play time

# Function to play the miss sound
def play_miss_sound():
    global last_miss_time  # Keep track of the last time the miss sound was played
    current_time = time.time()
    
    # Only play the sound if the cooldown period has passed
    if current_time - last_miss_time >= sound_cooldown:
        miss_sound.play()
        last_miss_time = current_time  # Update the last play time

# Hand gesture detection logic
def detect_hand_gesture(hand_landmarks, prev_gestures, smoothing_window=5, mirror_x=True, mirror_y=True):
    """
    Detect hand gestures (left, right, up, down, fist) using MediaPipe hand landmarks.
    
    Args:
        hand_landmarks: MediaPipe hand landmarks object.
        prev_gestures: List of previous gestures for smoothing.
        smoothing_window: Number of frames to average for smoothing (default: 5).
        mirror_x: If True, flip x-axis for mirrored webcam (default: True).
        mirror_y: If True, flip y-axis for mirrored webcam (default: True).
    
    Returns:
        Gesture ("fist", "left", "right", "up", "down", None) or None if no clear gesture.
    """
    global fist_held, last_fist_time
    
    # Extract key landmarks
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    
    # Fist detection with adaptive threshold
    hand_size = ((wrist.x - index_mcp.x) ** 2 + (wrist.y - index_mcp.y) ** 2) ** 0.5
    fist_threshold = hand_size * 0.3  # Adaptive based on hand size
    distance_thumb_index = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
    if distance_thumb_index < fist_threshold:
        if not fist_held:
            fist_held = True
            last_fist_time = time.time()
        elif time.time() - last_fist_time >= 2:
            return "fist"
        return None
    else:
        if fist_held and time.time() - last_fist_time < 0.2:  # 200ms buffer
            return None
        fist_held = False
    
    # Compute vector from wrist to index finger tip
    wrist_x, wrist_y = wrist.x, wrist.y
    index_x, index_y = index_tip.x, index_tip.y
    
    # Handle mirroring
    if mirror_x:
        wrist_x = 1.0 - wrist_x
        index_x = 1.0 - index_x
    if mirror_y:
        wrist_y = 1.0 - wrist_y
        index_y = 1.0 - index_y
    
    # Calculate direction vector
    dx = index_x - wrist_x
    dy = index_y - wrist_y
    
    # Compute angle and magnitude
    angle = np.arctan2(dy, dx) * 180 / np.pi
    magnitude = (dx ** 2 + dy ** 2) ** 0.5
    
    # Adaptive threshold for direction
    threshold = hand_size * 0.5
    if magnitude < threshold:
        return None  # Ignore small movements
    
    # Define angle ranges for directions (corrected)
    if -45 <= angle < 45:
        gesture = "left"
    elif 45 <= angle < 135:
        gesture = "up"
    elif 135 <= angle or angle < -135:
        gesture = "right"
    elif -135 <= angle < -45:
        gesture = "down"
    else:
        gesture = None
    
    # Temporal smoothing
    prev_gestures.append(gesture)
    if len(prev_gestures) > smoothing_window:
        prev_gestures.pop(0)
    
    valid_gestures = [g for g in prev_gestures if g is not None]
    if not valid_gestures:
        return None
    return max(set(valid_gestures), key=valid_gestures.count, default=None)

# Create a button at the bottom right of the screen
button_width, button_height = 250, 50
button_x = screen_width - button_width - 20  # 20px padding from right edge
button_y = screen_height - button_height - 20  # 20px padding from bottom edge

# Function to toggle webcam feed (or any other action)
def toggle_webcam():
    global webcam_enabled, webcam_button
    webcam_enabled = not webcam_enabled  # Toggle webcam status
    if webcam_enabled:
        webcam_button.color = BUTTON_COLOR_DISABLED  # Change button color to red
        webcam_button.text = "Disable Webcam Feed"  # Change text to 'Disable Camera'
        print("Webcam enabled")
    else:
        webcam_button.color = BUTTON_COLOR_ENABLED  # Change button color to green
        webcam_button.text = "Enable Webcam Feed"  # Change text to 'Enable Camera'
        print("Webcam disabled")

# Define some kid-friendly colors
TUTORIAL_BG_COLOR = (0, 0, 0, 100)  # Semi-transparent black for background overlay
COLOR_TEXT = (255, 176, 0)  # Gold for titles
COLOR_SUBTEXT = (0, 194, 203)   
COLOR_EMOJI = (241, 213, 128) 

# Initialize font
font_main = pygame.font.SysFont("Impact", 60)  # Larger and bold for main title
font_sub = pygame.font.SysFont("Impact", 40)  # Smaller for subtext
font_instructions = pygame.font.SysFont("Impact", 35)  # Standard for instructions and gestures

def display_text_with_image(surface, text, image, x, y, font, color):
    # Render the text
    text_surface = font.render(text, True, color)
    text_width, text_height = text_surface.get_size()
    image_width, image_height = image.get_size()
    
    # Calculate total width of image + text + spacing
    total_width = image_width + 10 + text_width  # 10px spacing between image and text
    start_x = x - (total_width // 2)  # Adjust x to center the combined image and text
    
    # Draw image and text
    surface.blit(image, (start_x, y))
    surface.blit(text_surface, (start_x + image_width + 10, y))  # Text to the right of image

# Load gesture images using the function
gesture_fist_img = load_image("fist.png", 50, 50)  # Fist gesture image
gesture_left_img = load_image("left.png", 50, 50)  # Left arrow image
gesture_right_img = load_image("right.png", 50, 50)  # Right arrow image
gesture_up_img = load_image("up.png", 50, 50)  # Up arrow image
gesture_down_img = load_image("down.png", 50, 50)  # Down arrow image

# Modified tutorial_text to split the complex gesture line into separate entries
tutorial_text = [
    ("Welcome to Mars Rover Exploration!", COLOR_TEXT, font_main),  # Main title
    ("Explore the Martian landscape and uncover educational facts.", COLOR_TEXT, font_sub),
    ("Use hand gestures to control the rover.", COLOR_EMOJI, font_instructions),
    (gesture_fist_img, "Fist gesture to analyze in certain zones.", WHITE, font_instructions),
    # Split the complex gesture line into individual entries for clarity
    (gesture_left_img, "Left: Move left", WHITE, font_instructions),
    (gesture_right_img, "Right: Move right", WHITE, font_instructions),
    (gesture_up_img, "Up: Move up", WHITE, font_instructions),
    (gesture_down_img, "Down: Move down", WHITE, font_instructions),
    ("Press Space or Enter to start the game.", COLOR_EMOJI, font_sub)
]

def start_screen():
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Fill screen with the background
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        # Create overlay with semi-transparent black background
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill(TUTORIAL_BG_COLOR)  # Semi-transparent black overlay
        screen.blit(overlay, (0, 0))

        # Display tutorial text with colors and different font sizes
        y_position = screen_height // 10  # Start closer to the top for title
        gesture_section_height = 0  # To calculate total height of the hand gesture part

        # First calculate total height of gesture section
        for item in tutorial_text[2:8]:  # Hand gesture part (now indices 2 to 7)
            if isinstance(item[0], pygame.Surface):  # Check if it's an image
                text_surface = font_instructions.render(item[1], True, item[2])
                gesture_section_height += text_surface.get_height() + 10  # Add spacing
            else:
                text_surface = item[2].render(item[0], True, item[1])
                gesture_section_height += text_surface.get_height() + 10  # Add spacing

        # Now place the tutorial text
        for item in tutorial_text:
            if isinstance(item[0], pygame.Surface):  # Check if it's an image (gesture lines)
                image = item[0]
                text = item[1]
                color = item[2]
                font = item[3]
                text_surface = font.render(text, True, color)
                text_width, text_height = text_surface.get_size()
                display_text_with_image(screen, text, image, screen_width // 2, y_position, font, color)
                y_position += text_height + 10  # Add space between lines
            else:  # Text-only (title, subtext, or start prompt)
                line, color, font = item
                text_surface = font.render(line, True, color)
                text_width, text_height = text_surface.get_size()

                x_position = (screen_width // 2) - (text_width // 2)
                if line == tutorial_text[0][0]:  # Main title
                    y_position = 50  # Slight padding from the top
                elif line == tutorial_text[1][0]:  # Subtext below the title
                    y_position += text_height + 20  # Line spacing after title
                elif line == tutorial_text[-1][0]:  # Press space or enter at the bottom
                    y_position = screen_height - 70  # Place near bottom
                elif line in [item[0] for item in tutorial_text[2:8]]:  # Gesture instructions, center vertically
                    if line == tutorial_text[2][0]:  # First line of gesture tutorial
                        y_position = (screen_height - gesture_section_height) // 2
                    y_position += text_height + 10  # Line spacing between gesture tutorial lines

                # Display the text
                screen.blit(text_surface, (x_position, y_position))
                if line != tutorial_text[-1][0]:  # Don't increment y_position after the last text
                    y_position += text_height + 10  # Move to next line for subsequent text
        
        # Draw the logo
        draw_logo(screen, logo_img)

        # Update the screen
        pygame.display.flip()

        # Wait for player to press space or enter
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            running = False  # Exit the start screen to begin the game

        time.sleep(0.1)

# Initialize webcam toggle state
webcam_enabled = False  # Initially, the webcam is disabled

# Create a button instance
webcam_button = Button(button_x, button_y, button_width, button_height, "Enable Webcam Feed", BUTTON_COLOR_ENABLED, TEXT_COLOR, toggle_webcam)

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    pygame.quit()
    exit()

# Rover Animation Variable
particles = []
hover_offset = 0

# Game loop
def main_game():
    running = True
    clock = pygame.time.Clock()
    last_gesture_time = 0
    gesture_cooldown = 0.1  # seconds

    # Variables for display timing and state
    state = "idle"  # idle, analyzing, showing_fact
    analyzing_start_time = 0
    fact_display_time = 0
    current_fact = ""
    fact_display_duration = 5000  # 5 seconds
    analyzing_duration = 1000  # 1 seconds

    # Initial rover position
    rover_x, rover_y = screen_width // 2, screen_height // 2
    rover_speed = 5

    is_moving = False
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw game visuals
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        # Get mouse position and click state
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Draw and handle button click
        webcam_button.draw(screen)
        webcam_button.check_click(mouse_pos, mouse_click)

        # Display guideline text at the top
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, 'assets')
        img_path = os.path.join(assets_dir, 'chimpu.png')
        image = pygame.image.load(img_path).convert_alpha()  # Load the image
        image = pygame.transform.smoothscale(image, (100, 100))  # Resize image if needed
        display_text_with_logo_image(screen, "Explore and analyze all the distinct objects.", image, font_size=40)
        
        if is_moving:
            hover_offset = 0  # Prevent hovering when moving
        else:
            time_ms = pygame.time.get_ticks()
            hover_offset = 6 * np.sin(time_ms / 300)  # Smooth hover while idle
        screen.blit(rover_image, (rover_x, rover_y + hover_offset))

        # Draw the logo
        draw_logo(screen, logo_img)

        # **New Section**: Display the exit tutorial message
        exit_message = "Press ESC or Q to exit the game."
        exit_message_surface = font_sub.render(exit_message, True, WHITE)
        exit_message_width, exit_message_height = exit_message_surface.get_size()

        exit_message_x = (screen_width - exit_message_width) // 2
        exit_message_y = screen_height - exit_message_height - 20

        screen.blit(exit_message_surface, (exit_message_x, exit_message_y))

        # Process webcam frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        frame = cv2.resize(frame, (320, 240))  # Resize for performance
        frame = cv2.flip(frame, 1)  # Flip horizontally for mirroring
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Fix 90-degree rotation
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Draw landmarks and process gestures
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame_rgb, landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = detect_hand_gesture(landmarks, prev_gestures, mirror_x=True, mirror_y=True)
                
                if gesture == "fist":
                    rover_rect = pygame.Rect(rover_x, rover_y, rover_image.get_width(), rover_image.get_height())
                    collision_type = check_for_collision(rover_rect, stone_coords, pithole_coords)
                    if collision_type == "stone":
                        current_fact = random.choice(stone_facts)
                        state = "analyzing"
                        analyzing_start_time = pygame.time.get_ticks()
                        sound_played = False  # Reset the flag to play sound after analysis
                    elif collision_type == "pithole":
                        current_fact = random.choice(pithole_facts)
                        state = "analyzing"
                        analyzing_start_time = pygame.time.get_ticks()
                        sound_played = False  # Reset the flag to play sound after analysis
                    else:
                        current_fact = "Keep exploring for more beneficial results!"
                        state = "analyzing"
                        analyzing_start_time = pygame.time.get_ticks()
                        sound_played = False  # Reset the flag to play sound after analysis
                
                if gesture in ["left", "right", "up", "down"]:
                    now = time.time()
                    is_moving = True
                    if now - last_gesture_time > gesture_cooldown:
                        if gesture == "right":
                            rover_y += rover_speed
                        elif gesture == "left":
                            rover_y -= rover_speed
                        elif gesture == "down":
                            rover_x -= rover_speed
                        elif gesture == "up":
                            rover_x += rover_speed
                        last_gesture_time = now
                    # Boundary check
                    rover_x = max(0, min(rover_x, screen_width - rover_image.get_width()))
                    rover_y = max(0, min(rover_y, screen_height - rover_image.get_height()))
                else:
                    is_moving = False
                if is_moving:
                    for _ in range(5):  # Spawn 3 particles per frame
                        particles.append(Particle(rover_x + 40, rover_y + 90))  # behind the rover

                for p in particles[:]:
                    p.update()
                    p.draw(screen)
                    if p.life <= 0:
                        particles.remove(p)

        # If webcam is enabled, display the webcam feed
        if webcam_enabled:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)  # Flip horizontally for mirroring
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_surface = pygame.surfarray.make_surface(frame_rgb)
                frame_surface = pygame.transform.scale(frame_surface, (200, 150))
                screen.blit(frame_surface, (0, 0))  # Display the webcam feed


        # Handle text display logic (analyzing, showing_fact)
        if state == "analyzing":
            elapsed_time = pygame.time.get_ticks() - analyzing_start_time
            if elapsed_time < analyzing_duration:
                display_text_with_background(screen, "Analyzing...", 40)
            else:
                state = "showing_fact"
                fact_display_time = pygame.time.get_ticks()
                if collision_type == "stone" or collision_type == "pithole":
                    if not sound_played:
                        play_success_sound()  # Play success sound after analyzing
                        sound_played = True  # Ensure it's only played once
                else:
                    if not sound_played:
                        play_miss_sound()  # Play miss sound after analyzing
                        sound_played = True  # Ensure it's only played once
        elif state == "showing_fact":
            if pygame.time.get_ticks() - fact_display_time <= fact_display_duration:
                display_text_with_background(screen, current_fact, 40)
            else:
                state = "idle"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
            pygame.quit()  # Exit the game if ESC or Q is pressed
            exit()

        # Update display
        pygame.display.flip()
        clock.tick(60)

start_screen()

main_game()

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()
pygame.quit()