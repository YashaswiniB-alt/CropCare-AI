import torch
from torchvision import models
import json
import os

MODEL_PATH = "models/multicrop_mobilenetv3.pth"
OUTPUT_PATH = "models/multicrop_mobilenetv3_torchscript.pt"

with open("models/multicrop_labels.json", "r") as f:
    labels = json.load(f)

num_classes = len(labels)

model = models.mobilenet_v3_small(weights=None)
model.classifier[3] = torch.nn.Linear(
    model.classifier[3].in_features,
    num_classes
)

checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

example_input = torch.randn(1, 3, 224, 224)

traced_model = torch.jit.trace(model, example_input)

traced_model.save(OUTPUT_PATH)

print("TorchScript optimization completed!")
print("Saved to:", OUTPUT_PATH)
print("Classes:", num_classes)
print("Model size:", round(os.path.getsize(OUTPUT_PATH) / (1024 * 1024), 2), "MB")