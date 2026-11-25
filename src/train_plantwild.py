import os
import re
import time
from collections import Counter

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from PIL import Image

# =========================
# 1. SETTINGS
# =========================

DATA_DIR = "data/PlantWild"
IMAGE_DIR = os.path.join(DATA_DIR, "images")
CLASSES_FILE = os.path.join(DATA_DIR, "classes.txt")
SPLIT_FILE = os.path.join(DATA_DIR, "trainval.txt")

MODEL_PATH = "models/plantwild_mobilenetv3.pth"
LABELS_PATH = "models/plantwild_labels.json"

EPOCHS = 3
BATCH_SIZE = 32
IMAGE_SIZE = 224

DEVICE = torch.device("cpu")

# =========================
# 2. LOAD CLASS NAMES
# =========================

import json

class_names = []

with open(CLASSES_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        # Format: class_id class_name
        match = re.match(r"^(\d+)[,\s]+(.+)$", line)

        if match:
            class_id = int(match.group(1))
            class_name = match.group(2).strip()
            class_names.append((class_id, class_name))

class_names.sort(key=lambda x: x[0])

class_ids = [item[0] for item in class_names]
class_labels = [item[1] for item in class_names]

print("PlantWild classes:", len(class_labels))

# =========================
# 3. READ DATA SPLITS
# =========================

train_records = []
val_records = []
test_records = []

with open(SPLIT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        parts = line.split("=")

        if len(parts) != 3:
            continue

        image_path = parts[0].strip().replace("\\", "/")
        class_id = int(parts[1].strip())
        split_id = int(parts[2].strip())

        full_path = os.path.join(
            IMAGE_DIR,
            image_path.replace("/", os.sep)
        )

        record = (full_path, class_id)

        if split_id == 1:
            train_records.append(record)
        elif split_id == 2:
            val_records.append(record)
        elif split_id == 0:
            test_records.append(record)

print("Training images:", len(train_records))
print("Validation images:", len(val_records))
print("Test images (reserved):", len(test_records))

# =========================
# 4. IMAGE TRANSFORMS
# =========================

train_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

val_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# =========================
# 5. DATASET
# =========================

class PlantWildDataset(Dataset):
    def __init__(self, records, transform=None):
        self.records = records
        self.transform = transform

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        image_path, class_id = self.records[index]

        image = Image.open(image_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, class_id

train_dataset = PlantWildDataset(train_records, train_transform)
val_dataset = PlantWildDataset(val_records, val_transform)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

# =========================
# 6. LOAD MOBILENET
# =========================

print("\nLoading MobileNetV3-Small pretrained model...")

weights = models.MobileNet_V3_Small_Weights.DEFAULT
model = models.mobilenet_v3_small(weights=weights)

# Freeze feature extractor
for param in model.features.parameters():
    param.requires_grad = False

# Replace classifier for PlantWild's 89 classes
model.classifier[3] = nn.Linear(
    model.classifier[3].in_features,
    len(class_labels)
)

model = model.to(DEVICE)

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.classifier.parameters(),
    lr=0.001
)

# =========================
# 7. TRAINING
# =========================

best_val_accuracy = 0.0

print("\n=== PlantWild Training Started ===")

for epoch in range(EPOCHS):

    model.train()
    train_correct = 0
    train_total = 0
    train_loss_total = 0.0

    start_time = time.time()

    for batch_index, (images, labels) in enumerate(train_loader):

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        train_loss_total += loss.item()
        predictions = outputs.argmax(dim=1)

        train_correct += (predictions == labels).sum().item()
        train_total += labels.size(0)

        if (batch_index + 1) % 100 == 0:
            print(
                f"Epoch {epoch + 1}/{EPOCHS} | "
                f"Batch {batch_index + 1}/{len(train_loader)}"
            )

    train_accuracy = 100 * train_correct / train_total
    average_train_loss = train_loss_total / len(train_loader)

    # =========================
    # VALIDATION
    # =========================

    model.eval()

    val_correct = 0
    val_total = 0
    val_loss_total = 0.0

    with torch.no_grad():
        for images, labels in val_loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)
            loss = criterion(outputs, labels)

            val_loss_total += loss.item()

            predictions = outputs.argmax(dim=1)
            val_correct += (predictions == labels).sum().item()
            val_total += labels.size(0)

    val_accuracy = 100 * val_correct / val_total
    average_val_loss = val_loss_total / len(val_loader)

    elapsed = time.time() - start_time

    print(f"\nEpoch {epoch + 1}/{EPOCHS} completed")
    print(f"Training Loss: {average_train_loss:.4f}")
    print(f"Training Accuracy: {train_accuracy:.2f}%")
    print(f"Validation Loss: {average_val_loss:.4f}")
    print(f"Validation Accuracy: {val_accuracy:.2f}%")
    print(f"Time: {elapsed / 60:.2f} minutes")

    # Save best model
    if val_accuracy > best_val_accuracy:
        best_val_accuracy = val_accuracy

        torch.save({
            "model_state_dict": model.state_dict(),
            "class_names": class_labels,
            "num_classes": len(class_labels),
            "val_accuracy": val_accuracy
        }, MODEL_PATH)

        with open(LABELS_PATH, "w", encoding="utf-8") as f:
            json.dump(class_labels, f, indent=2, ensure_ascii=False)

        print("Best PlantWild model saved!")

print("\n=== Training Completed ===")
print(f"Best Validation Accuracy: {best_val_accuracy:.2f}%")
print("Model:", MODEL_PATH)