from src.image_preprocessing import preprocess_crop_image

image_path = "data/test_images/tomato_leaf.jpg"

processed_image = preprocess_crop_image(image_path)

print("Image loaded successfully!")
print("Processed image shape:", processed_image.shape)
print("Minimum pixel value:", processed_image.min())
print("Maximum pixel value:", processed_image.max())