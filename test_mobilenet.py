import torch
import torchvision.models as models
import json
from PIL import Image
from torchvision import transforms

# Load labels
with open("models/labels.json", "r") as f:
    labels = json.load(f)

# Create MobileNetV2 architecture
model = models.mobilenet_v2(weights=None)

# Adjust final layer for 38 classes
model.classifier[1] = torch.nn.Sequential(
    torch.nn.Dropout(0.2),
    torch.nn.Linear(1280, 38)
)

# Load trained weights
checkpoint = torch.load(
    "models/mobilenetv2_plant.pth",
    map_location="cpu",
    weights_only=False
)

model.load_state_dict(checkpoint)
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

# Test image
image_path = "data/test_images/healthy_leaf.jpg"
image = Image.open(image_path).convert("RGB")
image = transform(image).unsqueeze(0)

# Prediction
with torch.no_grad():
    output = model(image)
    probabilities = torch.softmax(output, dim=1)
    top3 = torch.topk(probabilities, 3)

print("\n🌿 CropCare AI - MobileNetV2 Test")
print("--------------------------------")

for i in range(3):
    index = top3.indices[0][i].item()
    confidence = top3.values[0][i].item() * 100

    label = labels[str(index)] if isinstance(labels, dict) else labels[index]
print(f"{i+1}. {label} - {confidence:.2f}%")