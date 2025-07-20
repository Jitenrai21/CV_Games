import pygame, time

# Initialize pygame
pygame.init()

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