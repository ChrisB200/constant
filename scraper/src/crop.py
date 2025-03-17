import os
from PIL import Image

# Define input and output directories
folder = "triceps"
input_folder = f"old/{folder}"
output_folder = f"imgs/{folder}"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to crop the empty space from an image
def crop_empty_space(image):
    # Convert the image to grayscale
    gray_image = image.convert("L")
    
    # Get the bounding box of the non-empty pixels
    bbox = gray_image.getbbox()
    
    # If there's content to crop
    if bbox:
        return image.crop(bbox)
    else:
        return image  # If no content, return the original image

# Loop through all images in the folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):  # Filter image files
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Crop the empty space
        cropped_img = crop_empty_space(img)

        # Save the cropped image
        output_path = os.path.join(output_folder, filename)
        cropped_img.save(output_path)

        print(f"Cropped and saved: {filename}")

print("Finished cropping all images.")
