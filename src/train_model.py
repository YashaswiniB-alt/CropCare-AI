import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from torchvision.models import ResNet18_Weights
from pathlib import Path

# Select CPU
device = torch.device("cpu")
print("Using device:", device)

# Image transformations
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
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

# Load tomato dataset
train_data = datasets.ImageFolder(
    "data/tomato_dataset/train",
    transform=train_transform
)

val_data = datasets.ImageFolder(
    "data/tomato_dataset/val",
    transform=val_transform
)

train_loader = DataLoader(
    train_data, batch_size=32, shuffle=True, num_workers=0
)

val_loader = DataLoader(
    val_data, batch_size=32, shuffle=False, num_workers=0
)

# Load pretrained ResNet18
model = models.resnet18(weights=ResNet18_Weights.DEFAULT)

# Freeze existing feature extraction layers
for param in model.parameters():
    param.requires_grad = False

# Replace final classification layer
number_of_classes = len(train_data.classes)

model.fc = nn.Linear(model.fc.in_features, number_of_classes)
model = model.to(device)

# Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)

# Training
epochs = 2

for epoch in range(epochs):
    model.train()
    total_loss = 0
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

        total_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    train_accuracy = 100 * correct / total

    # Validation
    model.eval()
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()

    val_accuracy = 100 * val_correct / val_total

    print(
        f"Epoch {epoch + 1}/{epochs} | "
        f"Loss: {total_loss / len(train_loader):.4f} | "
        f"Train accuracy: {train_accuracy:.2f}% | "
        f"Validation accuracy: {val_accuracy:.2f}%"
    )

# Save model
Path("models").mkdir(exist_ok=True)

torch.save({
    "model_state_dict": model.state_dict(),
    "classes": train_data.classes
}, "models/tomato_resnet18.pth")

print("\nTraining completed!")
print("Model saved in models/tomato_resnet18.pth")