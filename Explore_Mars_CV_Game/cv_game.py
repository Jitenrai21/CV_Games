import pygame
import cv2
import mediapipe as mp
import numpy as np
import random
import time
from rover_movement_animation import Particle

# Initialize pygame
pygame.init()

# Screen dimensions and setup
screen_width, screen_height = 1080, 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mars Rover Exploration")

# Colors
WHITE = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)  # White for text

# Load and scale images
background_image = pygame.image.load('explore_mars_background.png')  # Ensure this file exists
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
rover_image = pygame.image.load('rover1.png')  # Ensure this file exists
rover_image = pygame.transform.scale(rover_image, (100, 100))

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
fact_display_duration = 3000  # 5 seconds
analyzing_duration = 2000  # 3 seconds

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

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw game visuals
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    if not is_moving:
        time_ms = pygame.time.get_ticks()
        hover_offset = 8 * np.sin(time_ms / 500)  # 6 pixels vertical oscillation
    else:
        hover_offset = 0  # No hovering while moving
    screen.blit(rover_image, (rover_x, rover_y + hover_offset))

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
                elif collision_type == "pithole":
                    current_fact = random.choice(pithole_facts)
                    state = "analyzing"
                    analyzing_start_time = pygame.time.get_ticks()
                else:
                    current_fact = "Keep exploring for more beneficial results!"
                    state = "analyzing"
                    analyzing_start_time = pygame.time.get_ticks()
            
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

    # Display webcam feed
    frame_surface = pygame.surfarray.make_surface(frame_rgb)
    frame_surface = pygame.transform.scale(frame_surface, (200, 150))
    screen.blit(frame_surface, (0, 0))

    # Display text
    if state == "analyzing":
        elapsed_time = pygame.time.get_ticks() - analyzing_start_time
        if elapsed_time < analyzing_duration:
            display_text("Analyzing...", 20, 500)
        else:
            state = "showing_fact"
            fact_display_time = pygame.time.get_ticks()
    elif state == "showing_fact":
        if pygame.time.get_ticks() - fact_display_time <= fact_display_duration:
            display_text(current_fact, 20, 500)
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