import pygame
import cv2
import mediapipe as mp
import numpy as np
import random
import time
from rover_movement_animation import Particle

# Initialize pygame
pygame.init()

# Initialize the Pygame mixer for sound
pygame.mixer.init()

# Screen dimensions and setup
screen_width, screen_height = 1080, 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mars Rover Exploration")

# Colors
WHITE = (255, 255, 255)
CARD_COLOR = (60, 60, 60)  # Dark grey background for card
TEXT_COLOR = (255, 255, 255)  # White for text
TITLE_COLOR = (255, 215, 0)  # Gold color for the title
BUTTON_COLOR_ENABLED = (0, 255, 0)  # Green for enabled
BUTTON_COLOR_DISABLED = (255, 0, 0)  # Red for disabled

# Load and scale images only once at the beginning
background_image = pygame.image.load('explore_mars_background.png').convert()
background_image = pygame.transform.smoothscale(background_image, (screen_width, screen_height))
rover_image = pygame.image.load('rover1.png').convert_alpha()  # Use convert_alpha for images with transparency
rover_image = pygame.transform.smoothscale(rover_image, (100, 100))
logo_img = pygame.image.load("Logo.png").convert_alpha()
logo_img = pygame.transform.smoothscale(logo_img, (60, 60))

# Load sound effects
bgm = pygame.mixer.Sound('bgm.mp3')  # Background music
success_sound = pygame.mixer.Sound('success.mp3')  # Success sound
miss_sound = pygame.mixer.Sound('miss.mp3')  # Miss sound

# Play background music in a loop (once the game starts)
bgm.play(loops=-1, maxtime=0, fade_ms=0)

# Initial rover position
rover_x, rover_y = screen_width // 2, screen_height // 2
rover_speed = 5

# Coordinates for bounding boxes (scaled to screen size)
stone_coords = [
    (int(54 * screen_width / 800), int(180 * screen_height / 600), int(112 * screen_width / 800), int(202 * screen_height / 600)),
    (int(115 * screen_width / 800), int(239 * screen_height / 600), int(173 * screen_width / 800), int(266 * screen_height / 600)),
    (int(193 * screen_width / 800), int(344 * screen_height / 600), int(241 * screen_width / 800), int(368 * screen_height / 600)),
    (int(38 * screen_width / 800), int(387 * screen_height / 600), int(83 * screen_width / 800), int(410 * screen_height / 600)),
    (int(111 * screen_width / 800), int(507 * screen_height / 600), int(177 * screen_width / 800), int(538 * screen_height / 600))
]

pithole_coords = [
    (int(468 * screen_width / 800), int(279 * screen_height / 600), int(717 * screen_width / 800), int(333 * screen_height / 600)),
    (int(437 * screen_width / 800), int(398 * screen_height / 600), int(720 * screen_width / 800), int(463 * screen_height / 600))
]

# Facts about stones and pitholes
stone_facts = [
    "Mars rocks are rich in iron, giving the planet its red color.",
    "Some rocks on Mars were formed billions of years ago.",
    "Mars may have had water long ago, according to some rocks.",
    "Mars' volcanoes are giant, like Olympus Mons, the biggest volcano in the solar system.",
    "Curiosity rover found signs of life in some Martian rocks.",
    "Mars has rocks that look like Earth’s, formed by wind and water.",
    "Mars has huge dust storms that can cover the entire planet.",
    "Some rocks on Mars show signs of past underground water.",
    "NASA’s Perseverance rover is collecting Martian rock samples.",
    "Valles Marineris, a giant canyon on Mars, is the largest in the solar system."
]



pithole_facts = [
    "Pitholes are holes in Mars' surface, made by old volcanic activity.",
    "Some pitholes formed from gas bubbles deep underground.",
    "Pitholes on Mars might have come from collapsing lava tubes.",
    "Martian pitholes show where the planet's volcanoes once erupted.",
    "Gas release from Mars' surface could have caused pitholes.",
    "Pitholes are formed by the low gravity and no atmosphere on Mars.",
    "Some pitholes on Mars may have been caused by meteorite impacts.",
    "Pitholes give scientists clues about Mars’ past weather and atmosphere.",
    "Many pitholes are near old volcanoes, showing Mars’ volcanic history.",
    "Pitholes may help us understand how Mars changed over time."
]


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Variables for hand gesture recognition
fist_held = False
last_fist_time = 0
prev_gestures = []

# Function to check for collision with bounding boxes
def check_for_collision(rover_rect, stone_coords, pithole_coords):
    for (start_x, start_y, end_x, end_y) in stone_coords:
        object_rect = pygame.Rect(start_x, start_y, end_x - start_x, end_y - start_y)
        if rover_rect.colliderect(object_rect):
            return "stone"
    for (start_x, start_y, end_x, end_y) in pithole_coords:
        object_rect = pygame.Rect(start_x, start_y, end_x - start_x, end_y - start_y)
        if rover_rect.colliderect(object_rect):
            return "pithole"
    return None

# Function to display text on the screen
def display_text(text, x, y, font_size=30):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (x, y))

# Function to draw the logo in the top-right corner
def draw_logo(surface, logo_img):
    logo_width, logo_height = logo_img.get_size()  # Get the dimensions of the logo
    logo_x = screen_width - logo_width - 10        # Position 10px from the right edge
    logo_y = 10                                    # Position 10px from the top edge

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

# Function to play the success sound
def play_success_sound():
    global sound_played  # Ensure sound is played only once
    if not sound_played:
        success_sound.play()
        sound_played = True

# Function to play the miss sound
def play_miss_sound():
    global sound_played  # Ensure sound is played only once
    if not sound_played:
        miss_sound.play()
        sound_played = True

# Function to display guideline text with a curved background and optional image
def display_text_with_image(surface, text, image, font_size=30):
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

# Variables for display timing and state
state = "idle"  # idle, analyzing, showing_fact
analyzing_start_time = 0
fact_display_time = 0
current_fact = ""
fact_display_duration = 5000  # 5 seconds
analyzing_duration = 1000  # 1 seconds

# Font for the button text
font = pygame.font.SysFont(None, 30)

# Button class to create customized buttons
class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)  # Button position and size
        self.text = text  # Button text
        self.color = color  # Button color
        self.text_color = text_color  # Text color
        self.action = action  # Action to be triggered on click
        self.last_click_time = 0  # Last time the button was clicked
        self.click_cooldown = 0.3  # Cooldown between clicks (seconds)

    def draw(self, surface):
        # Draw the button (color and text)
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)  # Draw text centered on the button

    def check_click(self, mouse_pos, mouse_click):
        # Check if the mouse is inside the button and if it was clicked
        current_time = time.time()
        if self.rect.collidepoint(mouse_pos) and mouse_click[0]:
            # Check if enough time has passed since the last click
            if current_time - self.last_click_time > self.click_cooldown:
                self.last_click_time = current_time  # Update last click time
                if self.action:
                    self.action()  # Trigger the action (if any)

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
is_moving = False
particles = []
hover_offset = 0

# Game loop
running = True
clock = pygame.time.Clock()
last_gesture_time = 0
gesture_cooldown = 0.1  # seconds

sound_played = False  # Flag to track whether sound has been played

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
    image = pygame.image.load("chimpu.png").convert_alpha()  # Load the image
    image = pygame.transform.smoothscale(image, (60, 60))  # Resize image if needed
    display_text_with_image(screen, "Explore and analyze all the distinct objects.", image, font_size=25)
    
    if is_moving:
        hover_offset = 0  # Prevent hovering when moving
    else:
        time_ms = pygame.time.get_ticks()
        hover_offset = 6 * np.sin(time_ms / 300)  # Smooth hover while idle
    screen.blit(rover_image, (rover_x, rover_y + hover_offset))

    # Draw the logo
    draw_logo(screen, logo_img)

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
            display_text_with_background(screen, "Analyzing...", 30)
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
            display_text_with_background(screen, current_fact, 30)
        else:
            state = "idle"
        

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()
pygame.quit()