from PIL import Image, ImageDraw, ImageFilter
import random
import os

# Configuration
output_folder = "crack_frames"
frame_count = 5
image_size = (256, 256)
line_color = (30, 30, 30)
line_width_range = (2, 5)
crack_count_range = (4, 10)

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

def generate_crack_image(intensity):
    img = Image.new("RGBA", image_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = (image_size[0] // 2, image_size[1] // 2)
    crack_count = random.randint(*crack_count_range)

    for _ in range(crack_count):
        angle = random.uniform(0, 360)
        length = intensity * random.randint(30, 120)
        x_offset = length * random.uniform(0.7, 1.0) * random.choice([-1, 1])
        y_offset = length * random.uniform(0.7, 1.0) * random.choice([-1, 1])
        end = (center[0] + x_offset, center[1] + y_offset)

        width = random.randint(*line_width_range)
        draw.line([center, end], fill=line_color, width=width)

    # Optional blur to simulate depth
    img = img.filter(ImageFilter.GaussianBlur(radius=intensity * 0.3))
    return img

# Generate frames with increasing crack intensity
for i in range(1, frame_count + 1):
    crack_img = generate_crack_image(i)
    crack_img.save(os.path.join(output_folder, f"crack{i}.png"))

import os
os.listdir(output_folder)