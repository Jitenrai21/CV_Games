import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Variables for hand gesture recognition
fist_held = False
last_fist_time = 0
prev_gestures = []

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
    
    # Define angle ranges for directions
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

# OpenCV video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Get webcam dimensions
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    # Resize frame for performance
    frame = cv2.resize(frame, (800, 600))
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    # Convert back to BGR for OpenCV display
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
    
    detected_gesture = None
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Detect hand gesture
            detected_gesture = detect_hand_gesture(landmarks, prev_gestures, mirror_x=True, mirror_y=True)
            
            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Display gesture on frame
            if detected_gesture:
                cv2.putText(frame, f"Gesture: {detected_gesture}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Display the frame
    cv2.imshow("Hand Gesture Detection", frame)
    
    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()