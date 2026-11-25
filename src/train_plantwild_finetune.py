import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import os

DATA_DIR = "data/PlantWild"
OUTPUT_PATH = "models/plantwild_mobilenetv3_finetuned.pth"

# Data augmentation
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Read dataset
train_records = []
val_records = []

with open(os.path.join(DATA_DIR, "trainval.txt"), "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        parts = line.split("=")
        image_path = parts[0].strip()
        class_id = int(parts[1].strip())
        split_id = int(parts[2].strip())

        full_path = os.path.join(DATA_DIR, "images", image_path)

        if split_id == 1:
            train_records.append((full_path, class_id))
        elif split_id == 2:
            val_records.append((full_path, class_id))

print("Training images:", len(train_records))
print("Validation images:", len(val_records))

class PlantWildDataset(Dataset):
    def __init__(self, records, transform):
        self.records = records
        self.transform = transform

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        path, label = self.records[idx]
        image = Image.open(path).convert("RGB")
        return self.transform(image), label

train_dataset = PlantWildDataset(train_records, train_transform)
val_dataset = PlantWildDataset(val_records, val_transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=0)

# Load baseline model
checkpoint = torch.load(
    "models/plantwild_mobilenetv3.pth",
    map_location="cpu"
)

class_names = checkpoint["class_names"]

model = models.mobilenet_v3_small(weights=None)
model.classifier[3] = nn.Linear(
    model.classifier[3].in_features,
    len(class_names)
)

model.load_state_dict(checkpoint["model_state_dict"])

# Freeze early layers, train deeper feature layers
for param in model.features.parameters():
    param.requires_grad = False

for param in model.features[-3:].parameters():
    param.requires_grad = True

for param in model.classifier.parameters():
    param.requires_grad = True

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam([
    {"params": model.features[-3:].parameters(), "lr": 0.0001},
    {"params": model.classifier.parameters(), "lr": 0.0005}
])

EPOCHS = 5
best_val_accuracy = 0

for epoch in range(EPOCHS):
    model.train()
    train_correct = 0
    train_total = 0
    train_loss = 0

    for images, labels in train_loader:
        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        predictions = outputs.argmax(dim=1)
        train_correct += (predictions == labels).sum().item()
        train_total += labels.size(0)
        train_loss += loss.item()

    train_accuracy = 100 * train_correct / train_total
    avg_train_loss = train_loss / len(train_loader)

    model.eval()
    val_correct = 0
    val_total = 0
    val_loss = 0

    with torch.no_grad():
        for images, labels in val_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)

            predictions = outputs.argmax(dim=1)
            val_correct += (predictions == labels).sum().item()
            val_total += labels.size(0)
            val_loss += loss.item()

    val_accuracy = 100 * val_correct / val_total
    avg_val_loss = val_loss / len(val_loader)

    print(f"\nEpoch {epoch+1}/{EPOCHS}")
    print(f"Train Accuracy: {train_accuracy:.2f}%")
    print(f"Train Loss: {avg_train_loss:.4f}")
    print(f"Validation Accuracy: {val_accuracy:.2f}%")
    print(f"Validation Loss: {avg_val_loss:.4f}")

    if val_accuracy > best_val_accuracy:
        best_val_accuracy = val_accuracy

        torch.save({
            "model_state_dict": model.state_dict(),
            "class_names": class_names,
            "num_classes": len(class_names),
            "val_accuracy": val_accuracy
        }, OUTPUT_PATH)

        print("Improved model saved!")

print("\nFine-tuning complete!")
print("Best Validation Accuracy:", best_val_accuracy)
print("Saved model:", OUTPUT_PATH)