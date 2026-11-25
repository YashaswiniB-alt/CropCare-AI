import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import os
from collections import defaultdict

DATA_DIR = "data/PlantWild"
MODEL_PATH = "models/plantwild_mobilenetv3_finetuned.pth"

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

records = []

with open(os.path.join(DATA_DIR, "trainval.txt"), "r", encoding="utf-8") as f:
    for line in f:
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

class PlantWildDataset(Dataset):
    def __init__(self, records):
        self.records = records

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        path, label = self.records[idx]
        image = Image.open(path).convert("RGB")
        return transform(image), label

loader = DataLoader(
    PlantWildDataset(records),
    batch_size=32,
    shuffle=False,
    num_workers=0
)

checkpoint = torch.load(MODEL_PATH, map_location="cpu")
class_names = checkpoint["class_names"]

model = models.mobilenet_v3_small(weights=None)
model.classifier[3] = nn.Linear(
    model.classifier[3].in_features,
    len(class_names)
)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

correct_per_class = defaultdict(int)
total_per_class = defaultdict(int)

with torch.no_grad():
    for images, labels in loader:
        outputs = model(images)
        predictions = outputs.argmax(dim=1)

        for label, prediction in zip(labels, predictions):
            total_per_class[label.item()] += 1

            if label.item() == prediction.item():
                correct_per_class[label.item()] += 1

results = []

for class_id in range(len(class_names)):
    total = total_per_class[class_id]
    correct = correct_per_class[class_id]

    if total > 0:
        accuracy = 100 * correct / total
        results.append((accuracy, class_names[class_id], correct, total))

results.sort()

print("\n======= FINE-TUNED CLASS-WISE REPORT =======")

print("\nLOWEST ACCURACY CLASSES:")
for accuracy, name, correct, total in results[:15]:
    print(f"{name}: {accuracy:.2f}% ({correct}/{total})")

print("\nHIGHEST ACCURACY CLASSES:")
for accuracy, name, correct, total in results[-15:][::-1]:
    print(f"{name}: {accuracy:.2f}% ({correct}/{total})")

print("===========================================")