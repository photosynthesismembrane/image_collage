import os
import random
from PIL import Image
import numpy as np

# Load image 
image_path = "title_page_offset_3.png"
image = Image.open(image_path)

# Get all image files from the folder
image_folder = "abstract"  # Update with your actual folder path
all_images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

# Calculate the number of columns and rows based on image dimensions and desired cell size
image_width = 612
image_height = 792
cell_size = 6  # Cell size set to 6x6 pixels
num_columns = image_width // cell_size
num_rows = image_height // cell_size

# Randomly shuffle images
random.shuffle(all_images)

# Function to check the number of black pixels in an image, in a given region, with certain rotation
def count_black_pixels(x, y, size, rotation):
    # Crop the region of interest first
    cropped_image = image.crop((x-size, y-size, x + size*2, y + size*2))

    # Rotate the cropped region
    rotated_cropped_image = cropped_image.rotate(rotation, resample=Image.BICUBIC, expand=False, center=(size, size))

    # Crop the rotated image to the original size
    rotated_cropped_image = rotated_cropped_image.crop((size, size, size*2, size*2))

    # Convert the rotated cropped image to a NumPy array
    cropped_array = np.array(rotated_cropped_image)

    # Count the number of black pixels (pixels with RGB values of 0,0,0)
    black_pixel_count = np.sum(cropped_array[:, :, 3] != 0)

    return black_pixel_count

# Function to generate random offset
def generate_random_offset(max_offset=5):
    return random.randint(-max_offset, max_offset)

# Function to generate random rotation
def generate_random_rotation(max_rotation=45):
    return random.uniform(-max_rotation, max_rotation)

# Function to generate random size
def generate_random_size(min_size=2, max_size=128):
    return random.randint(min_size, max_size)

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
            grid-template-columns: repeat({num_columns}, {cell_size}px);
            grid-template-rows: repeat({num_rows}, {cell_size}px);
            grid-gap: 0;
            width: {image_width}px;
            height: {image_height}px;
            margin: 100px;
        }}
        .grid-item {{
            width: {cell_size}px;
            height: {cell_size}px;
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
        img_src = f"{image_folder}/{all_images[image_counter % len(all_images)]}"
        for i in range(0, 300):
            offset_x = generate_random_offset()
            offset_y = generate_random_offset()
            rotation = generate_random_rotation()
            size = generate_random_size()
            z_index = size
            black_pixel_count = count_black_pixels(x + offset_x, y + offset_y, size, rotation)
            if black_pixel_count == 0:
                break
            if i == 299:
                img_src = f"white.png"
                offset_x = 0
                offset_y = 0
                rotation = 0
                size = 6
                z_index = 0
        
        html_content += f'''
            <div class="grid-item" style="left: {offset_x}px; top: {offset_y}px; transform: rotate({rotation}deg); z-index: {z_index};">
                <img src="{img_src}" class="grid-item-img" style="width: {size}px; height: {size}px;">
            </div>
        '''
        image_counter += 1
        if image_counter % 25 == 0:
            print(f"Processed {image_counter} images")
        # print(f"Processed cell ({x // cell_size}, {y // cell_size})")

html_content += """
    </div>
</body>
</html>
"""

# Define the file path for the output HTML file
output_html_file = "index_3.html"  # Update with your desired output path

# Write the HTML content to the file
with open(output_html_file, "w") as file:
    file.write(html_content)

print(f"HTML file created: {output_html_file}")
