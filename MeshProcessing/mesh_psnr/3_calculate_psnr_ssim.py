import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np

def calculate_psnr_and_ssim(image_path_1, image_path_2):
    # Read the images
    img1 = cv2.imread(image_path_1)[90:280, 500:600]
    img2 = cv2.imread(image_path_2)[90:280, 500:600]

    # Convert images to grayscale for SSIM calculation
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculate PSNR
    psnr_value = cv2.PSNR(img1, img2)

    # Calculate SSIM
    ssim_value = ssim(img1_gray, img2_gray)

    return psnr_value, ssim_value

# Function to modify the output path
def modify_output_path(base_path, light_added):
  if light_added:
    path_without_extension = base_path.rsplit('.', 1)[0]
    extension = base_path.split('.')[-1]
    return f"{path_without_extension}_with_light.{extension}"
  else:
    return base_path

# Example usage
with_light = True
image_path_1 = r'mesh_psnr\basketball\raw_nn_out.png'  # Replace with your first image path
config_lst = ['10x','50x','100x','150x','200x']
for config in config_lst:
  # image_path_2 = r'mesh_psnr\basketball\downsample_'+ config +'.png'  # Replace with your second image path
  image_path_2 = r'mesh_psnr\basketball\textured_mesh_'+ config +'.png'  # Replace with your second image path
  psnr, ssim_value = calculate_psnr_and_ssim(modify_output_path(image_path_1, with_light), modify_output_path(image_path_2, with_light))
  print(f"{config}: PSNR: {psnr:.4f} dB, SSIM: {ssim_value:.4f}")
