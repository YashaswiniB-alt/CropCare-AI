import os
from collections import Counter

DATASET_DIR = "data/PlantWild"
SPLIT_FILE = os.path.join(DATASET_DIR, "trainval.txt")

with open(SPLIT_FILE, "r", encoding="utf-8") as f:
    entries = [line.strip() for line in f if line.strip()]

split_counts = Counter()
class_counts = Counter()
invalid_entries = 0

for entry in entries:
    parts = entry.split("=")

    if len(parts) != 3:
        invalid_entries += 1
        continue

    image_path = parts[0].strip()
    class_id = parts[1].strip()
    split_id = parts[2].strip()

    if class_id.isdigit() and split_id.isdigit():
        class_counts_id = int(class_id)
        split_counts_id = int(split_id)

        class_counts[class_counts_id] += 1
        split_counts[split_counts_id] += 1
    else:
        invalid_entries += 1

print("=== PlantWild Split Analysis ===")
print("Total entries:", len(entries))
print("Invalid entries:", invalid_entries)

print("\nImages per split:")
for split_id in sorted(split_counts):
    print("Split ID =", split_id, "| Images =", split_counts[split_id])