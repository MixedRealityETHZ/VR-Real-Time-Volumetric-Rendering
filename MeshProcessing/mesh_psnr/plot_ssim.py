import matplotlib.pyplot as plt
from my_plot_utils import use_my_rcparam

use_my_rcparam()

# Data for the two methods
x = [10, 50, 100, 150, 200]  # Magnifications

# SSIM for each method
ssim_method_2 = [0.9753, 0.8945, 0.8318, 0.8038, 0.7789]
ssim_method_1 = [0.9677, 0.9693, 0.9614, 0.9560, 0.9405]

# Creating the plot
plt.plot(x, ssim_method_1, label='Texture Baking', marker='o')
plt.plot(x, ssim_method_2, label='Vertex Color', marker='o')

# Adding title and labels
plt.title('SSIM Comparison between Texture Baking and Vertex Color')
plt.xlabel('Mesh Down Sampling Ratio', fontsize = 8)
plt.ylabel('SSIM', fontsize = 8)
plt.grid(True)
legend = plt.legend()
legend.get_frame().set_linewidth(0.5)

# Show the plot
plt.grid(True)
# plt.show()
plt.savefig('mesh_psnr\plots\ssim.png')
