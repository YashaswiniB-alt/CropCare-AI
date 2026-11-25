import os
import json
import random
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms, models

# ---------------- CONFIGURATION ----------------
DATA_DIR = "data/PlantVillage_38Class"
MODEL_DIR = "models"
OUTPUT_MODEL = os.path.join(MODEL_DIR, "multicrop_mobilenetv3.pth")
OUTPUT_LABELS = os.path.join(MODEL_DIR, "multicrop_labels.json")

IMAGE_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 5
MAX_IMAGES_PER_CLASS = 500
SEED = 42

random.seed(SEED)
torch.manual_seed(SEED)

device = torch.device("cpu")
print("Device:", device)

# ---------------- IMAGE TRANSFORMS ----------------
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

# ---------------- LOAD DATASET ----------------
print("\nLoading PlantVillage dataset...")

base_dataset = datasets.ImageFolder(DATA_DIR)
train_dataset = datasets.ImageFolder(DATA_DIR, transform=train_transform)
val_dataset = datasets.ImageFolder(DATA_DIR, transform=val_transform)

class_names = base_dataset.classes
targets = base_dataset.targets

print("Classes found:", len(class_names))

# ---------------- CREATE TRAIN / VALIDATION SPLIT ----------------
train_indices = []
val_indices = []

for class_id in range(len(class_names)):
    class_indices = [
        i for i, label in enumerate(targets) if label == class_id
    ]

    random.shuffle(class_indices)

    # Limit images for our first experiment
    class_indices = class_indices[:MAX_IMAGES_PER_CLASS]

    split_point = int(len(class_indices) * 0.8)

    train_indices.extend(class_indices[:split_point])
    val_indices.extend(class_indices[split_point:])

print("Training images:", len(train_indices))
print("Validation images:", len(val_indices))

train_subset = Subset(train_dataset, train_indices)
val_subset = Subset(val_dataset, val_indices)

train_loader = DataLoader(
    train_subset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_subset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

# ---------------- CREATE MODEL ----------------
print("\nLoading MobileNetV3-Small pretrained model...")

weights = models.MobileNet_V3_Small_Weights.DEFAULT
model = models.mobilenet_v3_small(weights=weights)

# Freeze feature extraction layers
for parameter in model.features.parameters():
    parameter.requires_grad = False

# Replace the final classifier with our 38 classes
input_features = model.classifier[3].in_features
model.classifier[3] = nn.Linear(input_features, len(class_names))

model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(
    model.classifier.parameters(),
    lr=0.001
)

# ---------------- TRAINING ----------------
print("\nStarting custom model training...\n")

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        predictions = outputs.argmax(dim=1)

        total += labels.size(0)
        correct += (predictions == labels).sum().item()

    train_accuracy = 100 * correct / total
    avg_loss = running_loss / len(train_loader)

    # ---------------- VALIDATION ----------------
    model.eval()
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            predictions = outputs.argmax(dim=1)

            val_total += labels.size(0)
            val_correct += (predictions == labels).sum().item()

    val_accuracy = 100 * val_correct / val_total

    print(f"Epoch {epoch + 1}/{EPOCHS}")
    print(f"Train Loss: {avg_loss:.4f}")
    print(f"Train Accuracy: {train_accuracy:.2f}%")
    print(f"Validation Accuracy: {val_accuracy:.2f}%")
    print("-" * 40)

# ---------------- SAVE MODEL ----------------
os.makedirs(MODEL_DIR, exist_ok=True)

torch.save({
    "model_state_dict": model.state_dict(),
    "class_names": class_names,
    "image_size": IMAGE_SIZE
}, OUTPUT_MODEL)

with open(OUTPUT_LABELS, "w", encoding="utf-8") as f:
    json.dump(class_names, f, indent=4)

print("\nTraining complete!")
print("Model saved to:", OUTPUT_MODEL)
print("Labels saved to:", OUTPUT_LABELS)