import cv2

# Function to draw bounding boxes around the selected objects and save the image
def draw_bounding_boxes_and_save(image, stone_coords, pithole_coords, output_path="processed_image.jpg"):
    # Draw bounding boxes for stones
    for idx, (start_x, start_y, end_x, end_y) in enumerate(stone_coords, 1):
        # Draw rectangle for each stone
        cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)  # Green for stone

    # Draw bounding boxes for pitholes
    for idx, (start_x, start_y, end_x, end_y) in enumerate(pithole_coords, 1):
        # Draw rectangle for each pithole
        cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)  # Red for pithole

    # Save the processed image with bounding boxes
    cv2.imwrite(output_path, image)
    print(f"Processed image saved at {output_path}")

    # Display the processed image with bounding boxes
    cv2.imshow("Processed Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
# Replace these with the coordinates you picked manually
# stone_coords = [
#     (54, 180, 112, 202),  # Stone 1: top-left (100, 150), bottom-right (200, 250)
#     (115, 239, 173, 266),  # Stone 2: top-left (300, 350), bottom-right (400, 450)
#     (193, 344, 241, 368),
#     (38, 387, 83, 410),
#     (111, 507, 177, 538)
# ]

# pithole_coords = [
#     (468, 279, 717, 333),  # Pithole 1: top-left (500, 550), bottom-right (600, 650)
#     (437, 398, 720, 463)
# ]
stone_coords = [(425, 333, 486, 394), (667, 264, 713, 325), (622, 466, 704, 519), (590, 214, 629, 260), (160, 260, 298, 315), (143, 439, 185, 522), (88, 140, 129, 196), (132, 324, 159, 377)]
pithole_coords = []#[(137, 410, 236, 441), (318, 458, 376, 485), (500, 321, 618, 361)]
# Load the image
image = cv2.imread('background3.png')
image = cv2.resize(image, (800, 600))

# Call the function to draw bounding boxes and save the image
draw_bounding_boxes_and_save(image, stone_coords, pithole_coords, output_path="processed_mars_image_level2.jpg")
