import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import os

# Paths
DATA_DIR = "data/PlantWild"
MODEL_PATH = "models/plantwild_mobilenetv3.pth"

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Load test images
class PlantWildTestDataset(Dataset):
    def __init__(self, records):
        self.records = records

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        image_path, label = self.records[idx]

        image = Image.open(image_path).convert("RGB")
        image = transform(image)

        return image, label

# Read test records
records = []

split_file = os.path.join(DATA_DIR, "trainval.txt")

with open(split_file, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        parts = line.split("=")

        image_path = parts[0].strip()
        class_id = int(parts[1].strip())
        split_id = int(parts[2].strip())

        if split_id == 0:
            full_path = os.path.join(DATA_DIR, "images", image_path)
            records.append((full_path, class_id))

print("Total test images:", len(records))

# DataLoader
test_dataset = PlantWildTestDataset(records)
test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False,
    num_workers=0
)

# Load trained model
checkpoint = torch.load(MODEL_PATH, map_location="cpu")
class_names = checkpoint["class_names"]

model = models.mobilenet_v3_small(weights=None)
model.classifier[3] = nn.Linear(
    model.classifier[3].in_features,
    len(class_names)
)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

# Evaluate
correct = 0
total = 0
total_loss = 0

criterion = nn.CrossEntropyLoss()

with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        loss = criterion(outputs, labels)

        predictions = torch.argmax(outputs, dim=1)

        correct += (predictions == labels).sum().item()
        total += labels.size(0)
        total_loss += loss.item()

test_accuracy = 100 * correct / total
average_loss = total_loss / len(test_loader)

print("\n========== PLANTWILD TEST RESULTS ==========")
print(f"Test Accuracy: {test_accuracy:.2f}%")
print(f"Test Loss: {average_loss:.4f}")
print(f"Correct Predictions: {correct}/{total}")
print("========================================")