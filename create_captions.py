######################################################################
### Create captions for images by using the csv file.
### The csv file contains image_names, patient_id, sex, 
### age_approx, anatom_site_general_challenge, diagnosis,
### benign_malignant, target.
### Just the malignant images will be used to create captions.
###  
### Created captions will be in the format of:
### 
### photo of a {sex} skin, me1anoma on {anatom_site_general_challenge}, at age {age_approx}
###
### Every caption will be saved in a .caption file with the image name.
######################################################################

import pandas as pd
import os
from tqdm import tqdm

# Define a function to create captions

def create_caption(row):
    """Create a caption for an image."""
    sex = row[2]
    anatom_site = row[4]
    age = row[3]

    # Check if the diagnosis is malignant
    benign_malignant = row[6]
    if benign_malignant.lower() == 'malignant':
        caption = f"photo of a {sex} skin, me1anoma on {anatom_site}, at age {int(age)}"
        return caption
    else:
        return None

# Read the CSV file with pandas
csv_file = 'train.csv'  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Create the 'captions' folder if it doesn't exist
os.makedirs('captions', exist_ok=True)

# Initialize tqdm to track progress
progress_bar = tqdm(total=len(df))

# Create captions and save them for malignant images in the 'captions' folder
for index, row in df.iterrows():
    caption = create_caption(row)
    
    if caption:
        # Save the caption in a .caption file inside the 'captions' folder
        image_name = row[0]
        caption_file_path = os.path.join('captions', f'{image_name}.caption')
        with open(caption_file_path, mode='w') as caption_file:
            caption_file.write(caption)
    
    # Update the progress bar
    progress_bar.update(1)

# Close the progress bar
progress_bar.close()

print("Captions created for malignant images in the 'captions' folder.")

    