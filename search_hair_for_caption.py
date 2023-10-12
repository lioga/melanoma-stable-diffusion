######################################################################
### Search all the images in a directory for hair and add a caption
### Utilize contour detection to find hair in images
### Add ', hairy' to the caption file associated with this image
### Doesn't work perfectly, but it's better than nothing
######################################################################

import cv2
import os

def process_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and improve contour detection
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Use Canny edge detection to find edges in the image
    edges = cv2.Canny(blurred_image, 50, 250)

    # Find contours in the edge image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Define a minimum contour length threshold to filter out small artifacts
    min_contour_length = 100  

    # Filter out small contours (artifacts)
    filtered_contours = [contour for contour in contours if cv2.arcLength(contour, False) >= min_contour_length]
    total_perimeter = 0

    for contour in filtered_contours:
        perimeter = cv2.arcLength(contour, False)
        total_perimeter += perimeter

    print(f'Total Perimeter: {total_perimeter}')
    name_of_caption = image_path.split(".")
    if total_perimeter > 4000:
        # Add ', hairy' to the caption file associated with this image
        caption_filename = name_of_caption[0] + '.caption'
        with open(caption_filename, 'a') as file:
            text_to_add = ', hairy'
            file.write(text_to_add)

# Directory containing your images
image_directory = './malignant_images/'

# Loop through all image files in the directory
for filename in os.listdir(image_directory):
    if filename.endswith('.jpg'):  # Adjust the file extension as needed
        image_path = os.path.join(image_directory, filename)
        process_image(image_path)
