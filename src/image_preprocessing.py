import cv2
import numpy as np
from PIL import Image


def preprocess_crop_image(image_path, image_size=224):
    """
    Load and preprocess a crop image for AI analysis.
    """

    image = Image.open(image_path).convert("RGB")

    image = image.resize((image_size, image_size))

    image_array = np.array(image, dtype=np.float32)

    image_array = image_array / 255.0

    image_array = np.transpose(image_array, (2, 0, 1))

    return image_array


if __name__ == "__main__":
    print("Crop image preprocessing module is ready.")