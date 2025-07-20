import pygame

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