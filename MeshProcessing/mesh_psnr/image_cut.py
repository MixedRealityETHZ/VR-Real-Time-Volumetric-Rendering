import cv2

def crop_image(input_file, output_file):
  try:
    # Read the image
    img = cv2.imread(input_file)

    # Check if image is loaded properly
    if img is None:
        print("Error in loading the image. Please ensure the file exists and is a valid image.")
        return

    # Crop the image
    # Note: OpenCV handles images in [y:y+h, x:x+w] format
    cropped_img = img[90:220, 500:600]
    # cropped_img = img[90:1000, 380:700]

    # Save the cropped image
    cv2.imwrite(output_file, cropped_img)

    print(f"Cropped image saved as {output_file}")
  except Exception as e:
    print(f"An error occurred: {e}")

# Replace 'input.png' with your input file name
input_file = r'mesh_psnr\basketball\downsample_100x_with_light.png'

# Specify the name for the cropped output file
output_file = r'mesh_psnr\basketball\downsample_100x_with_light_cut.png'

crop_image(input_file, output_file)
