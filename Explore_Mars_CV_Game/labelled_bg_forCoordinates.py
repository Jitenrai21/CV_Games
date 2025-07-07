import cv2

# Initialize global variables
start_x, start_y, end_x, end_y = -1, -1, -1, -1  # To store coordinates
drawing = False  # To track drawing status
object_type = 'stone'  # Default object type is 'stone'
stone_count = 1  # To track number of stones
pithole_count = 1  # To track number of pitholes

# Lists to store coordinates
stone_coords = []
pithole_coords = []

# Mouse callback function to capture the bounding box coordinates
def draw_rectangle(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, drawing, object_type, stone_count, pithole_count

    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button down
        drawing = True
        start_x, start_y = x, y  # Store the starting point (top-left corner)
    
    elif event == cv2.EVENT_MOUSEMOVE:  # Mouse moving
        if drawing:
            end_x, end_y = x, y  # Update the bottom-right corner coordinates
    
    elif event == cv2.EVENT_LBUTTONUP:  # Left mouse button up
        drawing = False
        end_x, end_y = x, y  # Finalize the bottom-right corner coordinates
        cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)  # Draw rectangle on the image
        cv2.imshow("Image", image)  # Show updated image with rectangle

        # Store coordinates based on object type
        if object_type == 'stone':
            stone_coords.append((start_x, start_y, end_x, end_y))
            print(f"Stone {stone_count}: Top-left ({start_x}, {start_y}), Bottom-right ({end_x}, {end_y})")
            stone_count += 1  # Increment stone count
        elif object_type == 'pithole':
            pithole_coords.append((start_x, start_y, end_x, end_y))
            print(f"Pithole {pithole_count}: Top-left ({start_x}, {start_y}), Bottom-right ({end_x}, {end_y})")
            pithole_count += 1  # Increment pithole count

# Load the image (replace 'mars_background.jpg' with your image path)
image = cv2.imread('explore_mars_background.png')
image = cv2.resize(image, (800, 600))
image_copy = image.copy()

# Set up the mouse callback to allow selecting the bounding box
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_rectangle)

# Instruction for user input
print("Press 's' to select stone and 'p' to select pithole.")
print("Left-click and drag to select the object, and release to finalize the bounding box.")

# Display the image and wait for the user to select a bounding box
while True:
    cv2.imshow("Image", image)
    key = cv2.waitKey(1) & 0xFF  # Wait for key press

    if key == ord('s'):  # Press 's' to select stone
        object_type = 'stone'
        print("Now selecting stone.")
    elif key == ord('p'):  # Press 'p' to select pithole
        object_type = 'pithole'
        print("Now selecting pithole.")
    elif key == ord('q'):  # Press 'q' to quit the program
        break

cv2.destroyAllWindows()

# After the program ends, you can access the coordinates lists
print("Stone Coordinates:", stone_coords)
print("Pithole Coordinates:", pithole_coords)
