import os
from screeninfo import get_monitors

# Detect screen size
monitors = get_monitors()
main_screen = monitors[0]
screen_width, screen_height = main_screen.width, main_screen.height

# Get base asset directory
base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(base_dir)  # One level up
assets_dir = os.path.join(base_dir, 'assets')

level_configs = [
    {
        "background": os.path.join(assets_dir, "explore_mars_background.png"),
        "rover": os.path.join(assets_dir, "rover1.png"),
        "logo": os.path.join(assets_dir, "Logo.png"),

        "stone_coords": [
            # (int(54 * screen_width / 800), int(180 * screen_height / 600), int(112 * screen_width / 800), int(202 * screen_height / 600)),
            # (int(115 * screen_width / 800), int(239 * screen_height / 600), int(173 * screen_width / 800), int(266 * screen_height / 600)),
            # (int(193 * screen_width / 800), int(344 * screen_height / 600), int(241 * screen_width / 800), int(368 * screen_height / 600)),
            # (int(38 * screen_width / 800), int(387 * screen_height / 600), int(83 * screen_width / 800), int(410 * screen_height / 600)),
            # (int(111 * screen_width / 800), int(507 * screen_height / 600), int(177 * screen_width / 800), int(538 * screen_height / 600))
        ],

        "pithole_coords": [
            (int(468 * screen_width / 800), int(279 * screen_height / 600), int(717 * screen_width / 800), int(333 * screen_height / 600)),
            # (int(437 * screen_width / 800), int(398 * screen_height / 600), int(720 * screen_width / 800), int(463 * screen_height / 600))
        ],

        "stone_facts": [
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
        ],

        "pithole_facts": [
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
        ],

        "sounds": {
            "bgm": os.path.join(assets_dir, "bgm.mp3"),
            "success": os.path.join(assets_dir, "success.mp3"),
            "miss": os.path.join(assets_dir, "miss.mp3")
        }
    },
]
