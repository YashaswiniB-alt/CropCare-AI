import torch
import os

from torchvision import models

MODEL_PATH = "models/multicrop_mobilenetv3.pth"
OUTPUT_PATH = "models/multicrop_mobilenetv3.onnx"

# Load labels
import json
with open("models/multicrop_labels.json", "r") as f:
    labels = json.load(f)

num_classes = len(labels)

# Create MobileNetV3 model
model = models.mobilenet_v3_small(weights=None)
model.classifier[3] = torch.nn.Linear(
    model.classifier[3].in_features,
    num_classes
)

# Load trained weights
checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)

state = checkpoint["model_state_dict"]

model.load_state_dict(state)
model.eval()

# Dummy input
dummy_input = torch.randn(1, 3, 224, 224)

# Export to ONNX
torch.onnx.export(
    model,
    dummy_input,
    OUTPUT_PATH,
    input_names=["input"],
    output_names=["output"],
    opset_version=17,
    dynamo=False
)

print("ONNX export completed!")
print("Saved to:", OUTPUT_PATH)
print("Number of classes:", num_classes)