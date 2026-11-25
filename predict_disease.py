import torch
import torch.nn as nn
from src.severity_estimation import estimate_severity
from src.farmer_advisory import get_farmer_advisory
from torchvision import models, transforms
from PIL import Image

device = torch.device("cpu")

# Load trained model
checkpoint = torch.load(
    "models/tomato_resnet18.pth",
    map_location=device,
    weights_only=False
)

classes = checkpoint["classes"]

model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, len(classes))
model.load_state_dict(checkpoint["model_state_dict"])
model.to(device)
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

# Load test image
image_path = input("Enter image path: ")
image = Image.open(image_path).convert("RGB")
image = transform(image).unsqueeze(0)

# Predict top 3 classes
with torch.no_grad():
    outputs = model(image)
    probabilities = torch.softmax(outputs, dim=1)
    top_probabilities, top_indices = torch.topk(
        probabilities, 3, dim=1
    )

print("\n--- TOMATO DISEASE DETECTION ---")
print("\nTop 3 predictions:")

for i in range(3):
    disease = classes[top_indices[0][i].item()]
    confidence = top_probabilities[0][i].item() * 100

    print(f"{i + 1}. {disease}: {confidence:.2f}%")
predicted_disease = classes[top_indices[0][0].item()]

advisory = get_farmer_advisory(predicted_disease)

if advisory:
    print("\n--- FARMER ADVISORY ---")
    print("Cause:", advisory["cause"])
    print("Symptoms:", advisory["symptoms"])
    print("Precautions:", advisory["precautions"])
else:
    print("No advisory available.")
# Severity estimation
severity_result = estimate_severity(image_path)

if severity_result is not None:
    damage_percentage, severity = severity_result

    print("\n--- SEVERITY ESTIMATION ---")
    print("Estimated visible damage:", round(damage_percentage, 2), "%")
    print("Severity:", severity)
else:
    print("Unable to estimate severity.")