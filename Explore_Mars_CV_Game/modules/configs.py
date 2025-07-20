import pygame
import sys,os
from screeninfo import get_monitors

pygame.mixer.init()

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(base_dir)  # Go one level up
assets_dir = os.path.join(base_dir, 'assets')

# Screen dimensions and setup
monitors = get_monitors()
main_screen = monitors[0]
screen_width, screen_height = main_screen.width, main_screen.height
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
background_image_path = os.path.join(assets_dir, 'explore_mars_background.png')
background_image = pygame.image.load(background_image_path).convert()
background_image = pygame.transform.smoothscale(background_image, (screen_width, screen_height))
rover_image_path = os.path.join(assets_dir, 'rover1.png')
rover_image = pygame.image.load(rover_image_path).convert_alpha()
rover_image = pygame.transform.smoothscale(rover_image, (120, 120))
logo_img_path = os.path.join(assets_dir, 'Logo.png')
logo_img = pygame.image.load(logo_img_path).convert_alpha()
logo_img = pygame.transform.smoothscale(logo_img, (120, 120))

# Load sound effects
bgm_path = os.path.join(assets_dir, 'bgm.mp3')
bgm = pygame.mixer.Sound(bgm_path)
success_sound_path = os.path.join(assets_dir, 'success.mp3')
success_sound = pygame.mixer.Sound(success_sound_path)
miss_sound_path = os.path.join(assets_dir, 'miss.mp3')
miss_sound = pygame.mixer.Sound(miss_sound_path)

# Play background music in a loop (once the game starts)
bgm.play(loops=-1, maxtime=0, fade_ms=0)

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