from PIL import Image, ImageDraw, ImageFilter
import random
import os

# Configuration
output_dir = "break_frames"
frame_count = 6
image_size = (256, 256)
line_color = (30, 30, 30, 255)
line_width_range = (2, 5)
crack_per_frame = [3, 5, 8, 11, 14, 17]  # progressively more cracks per frame

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Base transparent image
base_img = Image.new("RGBA", image_size, (0, 0, 0, 0))
center = (image_size[0] // 2, image_size[1] // 2)

# Generate frames with increasing cracks
for i in range(frame_count):
    img = base_img.copy()
    draw = ImageDraw.Draw(img)

    num_cracks = crack_per_frame[i]
    for _ in range(num_cracks):
        angle = random.uniform(0, 360)
        length = random.randint(40, 120)
        offset_x = int(length * random.uniform(0.6, 1.0) * random.choice([-1, 1]))
        offset_y = int(length * random.uniform(0.6, 1.0) * random.choice([-1, 1]))
        end = (center[0] + offset_x, center[1] + offset_y)

        width = random.randint(*line_width_range)
        draw.line([center, end], fill=line_color, width=width)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))  # minor blur
    img.save(os.path.join(output_dir, f"break_{i+1}.png"))

import os
os.listdir(output_dir)