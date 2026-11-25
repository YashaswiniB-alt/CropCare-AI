import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json

# Load labels
with open("models/multicrop_labels.json", "r") as f:
    class_names = json.load(f)

# Load model
weights = models.MobileNet_V3_Small_Weights.DEFAULT
model = models.mobilenet_v3_small(weights=None)

model.classifier[3] = nn.Linear(
    model.classifier[3].in_features,
    len(class_names)
)

checkpoint = torch.load(
    "models/multicrop_mobilenetv3.pth",
    map_location="cpu"
)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Prediction function
def predict_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)

    top_probs, top_indices = torch.topk(probabilities, 3)

    print("\n--- CropCare AI Prediction ---")

    for i in range(3):
        class_name = class_names[top_indices[0][i].item()]
        confidence = top_probs[0][i].item() * 100

        print(f"{i+1}. {class_name}: {confidence:.2f}%")

# Enter image path
image_path = input("Enter leaf image path: ")
predict_image(image_path)