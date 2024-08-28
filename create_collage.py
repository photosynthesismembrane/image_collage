import os
import random
from PIL import Image
import numpy as np

# Get all image files from the folder
image_folder = "images"  # Update with your actual folder path
all_images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

# Calculate the number of columns and rows based on image dimensions and desired cell size
image_width = 1920
image_height = 1080
cell_size = 64  # Cell size set to 32x32
cell_size_css = 48
num_columns = image_width // cell_size
num_rows = image_height // cell_size

# Randomly shuffle images
random.shuffle(all_images)

# Function to generate random offset
def generate_random_offset(max_offset=5):
    return random.randint(-max_offset, max_offset)

# Function to generate random rotation
def generate_random_rotation(max_rotation=15):
    return random.uniform(-max_rotation, max_rotation)

# Generate the HTML content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Grid</title>
    <style>
        .grid-container {{
            display: grid;
            grid-template-columns: repeat({num_columns}, {cell_size_css}px);
            grid-template-rows: repeat({num_rows}, {cell_size_css}px);
            grid-gap: 0;
            width: {image_width}px;
            height: {image_height}px;
        }}
        .grid-item {{
            width: {cell_size_css}px;
            height: {cell_size_css}px;
            position: relative;
        }}
        .grid-item img {{
            width: {cell_size}px;
            height: {cell_size}px;
            position: absolute;
        }}
    </style>
</head>
<body>
    <div class="grid-container">
"""

image_counter = 0
for y in range(0, image_height, cell_size):
    for x in range(0, image_width, cell_size):
        offset_x = generate_random_offset()
        offset_y = generate_random_offset()
        rotation = generate_random_rotation()
        img_src = f"{image_folder}/{all_images[image_counter % len(all_images)]}"
        html_content += f'''
            <div class="grid-item" style="left: {offset_x}px; top: {offset_y}px; transform: rotate({rotation}deg);">
                <img src="{img_src}" class="grid-item-img">
            </div>
        '''
        image_counter += 1

html_content += """
    </div>
</body>
</html>
"""

# Define the file path for the output HTML file
output_html_file = "index.html"  # Update with your desired output path

# Write the HTML content to the file
with open(output_html_file, "w") as file:
    file.write(html_content)

print(f"HTML file created: {output_html_file}")
