import cv2
import numpy as np
import os


def analyze_leaf(image_path):

    image = cv2.imread(image_path)

    if image is None:
        print("Image not found!")
        return None

    image = cv2.resize(image, (224, 224))
    height, width = image.shape[:2]

    # Step 1: Separate leaf from background using GrabCut
    mask = np.zeros((height, width), np.uint8)

    margin = 10
    rectangle = (
        margin,
        margin,
        width - 2 * margin,
        height - 2 * margin
    )

    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)

    try:
        cv2.grabCut(
            image,
            mask,
            rectangle,
            background_model,
            foreground_model,
            5,
            cv2.GC_INIT_WITH_RECT
        )
    except cv2.error:
        print("Leaf segmentation failed.")
        return None

    leaf_mask = np.where(
        (mask == cv2.GC_FGD) |
        (mask == cv2.GC_PR_FGD),
        255,
        0
    ).astype(np.uint8)

    # Step 2: Detect yellow and brown coloured regions
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    damage_mask = cv2.inRange(
        hsv,
        np.array([5, 40, 20]),
        np.array([35, 255, 255])
    )

    # Step 3: Count damaged pixels only inside segmented leaf
    damage_region = cv2.bitwise_and(
        damage_mask,
        leaf_mask
    )

    leaf_pixels = np.count_nonzero(leaf_mask)
    damage_pixels = np.count_nonzero(damage_region)

    if leaf_pixels == 0:
        print("Unable to identify leaf.")
        return None

    damage_percentage = (
        damage_pixels / leaf_pixels
    ) * 100

    if damage_percentage < 10:
        severity = "Mild"
    elif damage_percentage < 25:
        severity = "Moderate"
    else:
        severity = "Severe"

    # Step 4: Create visual output
    overlay = image.copy()
    overlay[damage_region > 0] = (0, 0, 255)

    visual = cv2.addWeighted(
        image, 0.65, overlay, 0.35, 0
    )

    os.makedirs("outputs", exist_ok=True)

    cv2.imwrite("outputs/leaf_mask.png", leaf_mask)
    cv2.imwrite("outputs/severity_visual.png", visual)

    return damage_percentage, severity


def estimate_severity(image_path):
    result = analyze_leaf(image_path)

    if result is None:
        return None

    return result


if __name__ == "__main__":

    print("LEAF SEVERITY ESTIMATION")

    image_path = input("Enter image path: ")

    result = analyze_leaf(image_path)

    if result is not None:

        percentage, severity = result

        print(
            "Estimated visible damage:",
            round(percentage, 2),
            "%"
        )

        print("Severity:", severity)

        print("Leaf mask saved: outputs/leaf_mask.png")
        print("Visual result saved: outputs/severity_visual.png")