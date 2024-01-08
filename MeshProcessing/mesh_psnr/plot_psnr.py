import matplotlib.pyplot as plt
from my_plot_utils import use_my_rcparam

use_my_rcparam()

# Data for "Meshod 1" and "Meshod 2"
x = [10, 50, 100, 150, 200]  # magnifications
psnr_meshod2 = [40.7478, 33.2837, 29.7508, 28.2577, 27.4776]
psnr_meshod1 = [40.3015, 40.0787, 39.0313, 37.7878, 35.5774]

# Plotting
# plt.figure(figsize=(10, 6))
plt.plot(x, psnr_meshod1, label='Texture Baking', marker='o')
plt.plot(x, psnr_meshod2, label='Vertex Color', marker='x')

# Adding titles and labels
plt.title('PSNR Comparison Between Texture Baking and Vertex Color')
plt.xlabel('Mesh Down Sampling Ratio', fontsize = 8)
plt.ylabel('PSNR (dB)', fontsize = 8)
legend = plt.legend()
legend.get_frame().set_linewidth(0.5)

# Show the plot
plt.grid(True)
# plt.show()
plt.savefig('mesh_psnr\plots\psnr.png')
