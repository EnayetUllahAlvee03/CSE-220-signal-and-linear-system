import numpy as np
import matplotlib.pyplot as plt
# from scipy.integrate import trapz

    

# Load and preprocess the image
image = plt.imread('noisy_image.png')  # Replace with your image file path
# show the image
plt.figure()
plt.title('Original Image')
plt.imshow(image, cmap='gray')
plt.show()

if image.ndim == 3:
    image = np.mean(image, axis=2)  # Convert to grayscale

image = image / 255.0  # Normalize to range [0, 1]
print (image.shape)

sample_rate = 1000 


# plt.imsave('denoised_image.png', denoised_image, cmap='gray')


# plt.figure()
# plt.title('Denoised Image')
# plt.imshow(denoised_image, cmap='gray')
# plt.show()
