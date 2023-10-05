### A script for separating malignant images from benign images 
### in dataset to feed them into Stable Diffusion later.

import os
import random
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import shutil
from tqdm import tqdm

# Paths to CSV file, source directory, and destination directory
csv_file_path = "./train.csv"
source_directory = "./train/"
destination_directory = "./malignant_images/"

def display_random_images_in_grid(destination_folder, num_images=4, image_size=(512, 512)):
    # List all image files in the destination folder
    image_files = [f for f in os.listdir(destination_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    # Check if there are any image files in the folder
    if not image_files:
        print("No image files found in the destination folder.")
        return

    # Select 'num_images' random image files
    random_images = random.sample(image_files, num_images)

    # Create a grid for displaying images
    num_rows = int(num_images**0.5)
    num_cols = (num_images + num_rows - 1) // num_rows
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(8, 8))
    axes = axes.ravel()

    for i, ax in enumerate(axes):
        if i < len(random_images):
            image_path = os.path.join(destination_folder, random_images[i])

            # Open and resize the image to the specified size
            img = Image.open(image_path)
            img = img.resize(image_size)

            # Display the resized image
            ax.imshow(img)
            ax.axis('off')

    plt.show()

# Create the destination directory if it doesn't exist
os.makedirs(destination_directory, exist_ok=True)

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Filter rows where the 7th column is "malignant"
malignant_rows = df[df.iloc[:, 6] == "malignant"]

print("Total number of malignant images: \n")
print(len(malignant_rows.index))

with tqdm(total=len(malignant_rows)) as pbar:
    for index, row in malignant_rows.iterrows():
        image_name = row.iloc[0] + ".jpg"  # Get the image name from the 1st column

        source_path = os.path.join(source_directory, image_name)
        destination_path = os.path.join(destination_directory, image_name)

        # Check if the source image file exists
        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
            pbar.update(1)  # Update the progress bar
            #print(f"Copied {image_name} to {destination_directory}")
        else:
            #print(f"Image {image_name} not found in {source_directory}")
            pbar.update(1)  # Update the progress bar even if the image is not found

print("Copying completed.")

display_random_images_in_grid('./malignant_images/', num_images=4, image_size=(256, 256))