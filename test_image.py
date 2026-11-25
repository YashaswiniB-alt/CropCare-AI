import cv2
import numpy as np
import matplotlib.pyplot as plt

print("OpenCV version:", cv2.__version__)
print("NumPy version:", np.__version__)

# Create a sample image
image = np.zeros((300, 300, 3), dtype=np.uint8)

# Draw a green leaf-like shape
cv2.ellipse(image, (150, 150), (60, 110), 45, 0, 360, (0, 180, 0), -1)

# Convert image format for displaying
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display image
plt.imshow(image_rgb)
plt.title("Crop Image Processing Test")
plt.axis("off")
plt.show()

print("Image processing test successful!")