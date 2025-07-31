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
            (int(54 * screen_width / 800), int(180 * screen_height / 600), int(112 * screen_width / 800), int(202 * screen_height / 600)),
            (int(115 * screen_width / 800), int(239 * screen_height / 600), int(173 * screen_width / 800), int(266 * screen_height / 600)),
            (int(193 * screen_width / 800), int(344 * screen_height / 600), int(241 * screen_width / 800), int(368 * screen_height / 600)),
            (int(38 * screen_width / 800), int(387 * screen_height / 600), int(83 * screen_width / 800), int(410 * screen_height / 600)),
            (int(111 * screen_width / 800), int(507 * screen_height / 600), int(177 * screen_width / 800), int(538 * screen_height / 600))
        ],

        "pithole_coords": [
            (int(468 * screen_width / 800), int(279 * screen_height / 600), int(717 * screen_width / 800), int(333 * screen_height / 600)),
            (int(437 * screen_width / 800), int(398 * screen_height / 600), int(720 * screen_width / 800), int(463 * screen_height / 600))
        ],

        "stone_facts": [
            "Mars' rocks show evidence of volcanic activity, revealing the planet's active past.",
            "Some Martian rocks are rich in silica, indicating potential for ancient microbial life.",
            "Mars' rocks reveal traces of wind erosion, hinting at a once thicker atmosphere.",
            "Clay and sulfate minerals found in rocks suggest past water on Mars.",
            "Mars' basalt rocks formed from ancient lava flows, similar to Earth's oceanic crust.",
            "Martian rocks show signs of radiation exposure, distinct from Earth's geology.",
            "Some Martian stones contain minerals that formed in water, suggesting past habitable conditions.",
            "Perseverance Rover is collecting Martian rock samples for future study on climate history.",
            "Mars' Valles Marineris canyon was likely carved by ancient water flows, revealed by rock analysis.",
            "Mars' surface shows rock formations shaped by wind, similar to Earth’s deserts."
        ],

        "pithole_facts": [
            "Pitholes on Mars are created by volcanic activity and gas pockets beneath the surface.",
            "Martian pitholes might have formed from collapsing lava tubes, creating depressions.",
            "Some pitholes are shaped by ancient underground water erosion beneath Mars' surface.",
            "Mars' pitholes can offer insights into the planet’s volcanic and atmospheric history.",
            "Certain Martian pitholes were likely formed by meteorite impacts millions of years ago.",
            "Mars' low gravity and lack of atmosphere led to unique pithole formations.",
            "Pitholes near volcanoes indicate Mars’ volcanic history and changing surface.",
            "Martian pitholes preserve clues about the planet’s early atmosphere and water.",
            "Gas release from Mars’ surface created pitholes, helping shape the landscape.",
            "Pitholes on Mars help scientists study its past climate and geological activity."
        ],

        "sounds": {
            "bgm": os.path.join(assets_dir, "bgm.mp3"),
            "success": os.path.join(assets_dir, "success.mp3"),
            "miss": os.path.join(assets_dir, "miss.mp3")
        }
    },
    {   
        # level 2 setup
        "background": os.path.join(assets_dir, "background2.png"),
        "rover": os.path.join(assets_dir, "rover3.png"),
        "logo": os.path.join(assets_dir, "Logo.png"),

        "stone_coords": [
            (int(483 * screen_width / 800), int(379 * screen_height / 600), int(582 * screen_width / 800), int(439 * screen_height / 600)),
            (int(63 * screen_width / 800), int(348 * screen_height / 600), int(149 * screen_width / 800), int(427 * screen_height / 600)),
            (int(445 * screen_width / 800), int(203 * screen_height / 600), int(623 * screen_width / 800), int(339 * screen_height / 600)),
            (int(624 * screen_width / 800), int(501 * screen_height / 600), int(706 * screen_width / 800), int(555 * screen_height / 600)),
        ],

        "pithole_coords": [
            (int(97 * screen_width / 800), int(488 * screen_height / 600), int(254 * screen_width / 800), int(545 * screen_height / 600)),
            (int(204 * screen_width / 800), int(426 * screen_height / 600), int(264 * screen_width / 800), int(442 * screen_height / 600))
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
    {   
        # level 3 setup
        "background": os.path.join(assets_dir, "background3.png"),
        "rover": os.path.join(assets_dir, "rover3.png"),
        "logo": os.path.join(assets_dir, "Logo.png"),

        "stone_coords": [
            (int(425 * screen_width / 800), int(333 * screen_height / 600), int(486 * screen_width / 800), int(394 * screen_height / 600)),
            (int(667 * screen_width / 800), int(264 * screen_height / 600), int(713 * screen_width / 800), int(325 * screen_height / 600)),
            (int(622 * screen_width / 800), int(466 * screen_height / 600), int(704 * screen_width / 800), int(519 * screen_height / 600)),
            (int(590 * screen_width / 800), int(214 * screen_height / 600), int(629 * screen_width / 800), int(260 * screen_height / 600)),
            (int(160 * screen_width / 800), int(260 * screen_height / 600), int(298 * screen_width / 800), int(315 * screen_height / 600)),
            (int(143 * screen_width / 800), int(439 * screen_height / 600), int(185 * screen_width / 800), int(522 * screen_height / 600)),
            (int(88 * screen_width / 800), int(140 * screen_height / 600), int(129 * screen_width / 800), int(196 * screen_height / 600)),
            (int(132 * screen_width / 800), int(324 * screen_height / 600), int(159 * screen_width / 800), int(377 * screen_height / 600))
        ],

        "pithole_coords": [],

        "stone_facts": [
            "Olympus Mons is the tallest volcano in the solar system at 13.6 miles high.",
            "Mars' atmosphere is mostly carbon dioxide, making it uninhabitable without protection.",
            "Massive dust storms on Mars can last months and cover the entire planet.",
            "Mars has polar ice caps of carbon dioxide and water ice that change with seasons.",
            "Mars' gravity is 38% of Earth's, making you weigh less there.",
            "Liquid water once flowed on Mars, evidenced by riverbeds and valleys.",
            "Mars has seasons, but they last about twice as long as Earth's.",
            "Temperatures on Mars range from -195°F to 70°F (-125°C to 20°C).",
            "Mars' red color comes from iron oxide (rust) in the soil and rocks.",
            "Mars has two moons, Phobos and Deimos, likely captured asteroids.",
            "Mars once had a magnetic field, but it disappeared long ago.",
            "Mars’ thin atmosphere can’t support life as we know it, but past life is possible.",
            "Underground water may still exist in aquifers on Mars.",
            "Mars’ equator gets more solar radiation, causing extreme temperatures.",
            "Curiosity rover found organic molecules, hinting at ancient life on Mars.",
            "Valles Marineris is the largest canyon in the solar system, 2,500 miles long.",
            "Mars once had a thick atmosphere, but it was stripped by solar winds.",
            "Winds on Mars can reach speeds of over 60 mph, shaping the landscape.",
            "Mars is half the size of Earth, with a surface area similar to Earth's landmass.",
            "A day on Mars is 24.6 hours, similar to Earth’s day."
        ],

        "pithole_facts": [],

        "sounds": {
            "bgm": os.path.join(assets_dir, "bgm.mp3"),
            "success": os.path.join(assets_dir, "success.mp3"),
            "miss": os.path.join(assets_dir, "miss.mp3")
        }
    }
]
