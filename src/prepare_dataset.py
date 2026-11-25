from pathlib import Path
import shutil

SOURCE = Path("data/PlantVillage")
DESTINATION = Path("data/tomato_dataset")

for split in ["train", "val"]:
    split_folder = SOURCE / split

    for class_folder in split_folder.iterdir():
        if class_folder.is_dir() and class_folder.name.startswith("Tomato___"):

            destination_folder = DESTINATION / split / class_folder.name
            destination_folder.mkdir(parents=True, exist_ok=True)

            count = 0

            for image in class_folder.iterdir():
                if image.is_file():
                    shutil.copy2(image, destination_folder / image.name)
                    count += 1

            print(f"{split} | {class_folder.name} | {count} images")

print("\nTomato dataset preparation completed!")