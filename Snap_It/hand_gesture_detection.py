import cv2
import mediapipe as mp
import pyautogui  # Import PyAutoGUI for mouse control

# Define the screen dimensions (must match the game window)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize MediaPipe Hands and OpenCV
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Function to detect hand gestures based on the landmark positions
def detect_gesture(landmarks, image_shape):
    """Detect hand gestures based on landmark positions."""
    h, w, _ = image_shape
    thumb_tip = landmarks[4]   # Thumb tip
    index_tip = landmarks[8]   # Index finger tip
    middle_tip = landmarks[12] # Middle finger tip
    ring_tip = landmarks[16]   # Ring finger tip
    pinky_tip = landmarks[20]  # Pinky finger tip
    wrist = landmarks[0]       # Wrist

    # Helper: Check if finger is extended (higher than its base)
    def is_finger_extended(tip, base_idx):
        base = landmarks[base_idx]
        return tip.y < base.y - 0.05  # y-coordinate check (inverted)

    # Thumbs up: Thumb extended up, other fingers folded
    if (thumb_tip.y < wrist.y - 0.1 and
        not is_finger_extended(index_tip, 5) and
        not is_finger_extended(middle_tip, 9)):
        return "thumbs_up"

    # Thumbs down: Thumb extended down, other fingers folded
    if (thumb_tip.y > wrist.y + 0.1 and
        not is_finger_extended(index_tip, 5) and
        not is_finger_extended(middle_tip, 9)):
        return "thumbs_down"

    # Peace sign: Index and middle fingers extended, others folded
    if (is_finger_extended(index_tip, 5) and
        is_finger_extended(middle_tip, 9) and
        not is_finger_extended(ring_tip, 13) and
        not is_finger_extended(pinky_tip, 17)):
        return "peace_sign"

    return None

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)  # Set webcam resolution
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame for better display and convert to RGB
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe
        results = hands.process(frame)

        # Convert the frame back to BGR for OpenCV display
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                # Detect gestures
                gesture = detect_gesture(landmarks.landmark, frame.shape)

                # Display detected gesture
                if gesture:
                    cv2.putText(frame, f"Gesture: {gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Use index finger tip to control the mouse cursor
                index_tip = landmarks.landmark[8]  # Index finger tip
                x = int(index_tip.x * SCREEN_WIDTH)  # Map x to screen width
                y = int(index_tip.y * SCREEN_HEIGHT)  # Map y to screen height

                pyautogui.moveTo(x, y)  # Move the cursor to the detected index tip position

        # Show the frame with the detected gestures
        cv2.imshow('Hand Gesture Detection', frame)

        # Quit condition: Press 'q' to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
