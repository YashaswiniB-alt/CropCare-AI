def get_farmer_advisory(disease):

    advisories = {

        "Tomato___Bacterial_spot": {
            "cause": "Bacterial infection.",
            "symptoms": "Small dark, water-soaked spots on leaves.",
            "precautions": "Avoid overhead watering and remove infected plant debris."
        },

        "Tomato___Early_blight": {
            "cause": "Fungal infection.",
            "symptoms": "Brown spots with concentric ring patterns on older leaves.",
            "precautions": "Remove infected leaves and avoid wetting foliage."
        },

        "Tomato___Late_blight": {
            "cause": "Disease caused by a fungus-like organism.",
            "symptoms": "Water-soaked dark patches that can spread rapidly.",
            "precautions": "Remove affected plant material and avoid overhead irrigation."
        },

        "Tomato___Leaf_Mold": {
            "cause": "Fungal infection.",
            "symptoms": "Yellow patches on upper leaf surfaces and mold growth underneath.",
            "precautions": "Improve air circulation and reduce excess humidity."
        },

        "Tomato___Septoria_leaf_spot": {
            "cause": "Fungal infection.",
            "symptoms": "Small circular spots with pale centers and dark edges.",
            "precautions": "Remove infected lower leaves and avoid splashing water."
        },

        "Tomato___Spider_mites Two-spotted_spider_mite": {
            "cause": "Spider mite infestation.",
            "symptoms": "Tiny pale spots, yellowing and fine webbing on leaves.",
            "precautions": "Inspect leaf undersides and seek locally appropriate pest-control advice."
        },

        "Tomato___Target_Spot": {
            "cause": "Fungal infection.",
            "symptoms": "Brown circular spots with target-like rings.",
            "precautions": "Remove infected leaves and maintain good plant spacing."
        },

        "Tomato___Tomato_YellowLeaf__Curl_Virus": {
            "cause": "Viral infection.",
            "symptoms": "Yellowing, upward leaf curling and stunted growth.",
            "precautions": "Remove severely affected plants as locally advised and monitor whiteflies."
        },

        "Tomato___Tomato_mosaic_virus": {
            "cause": "Viral infection.",
            "symptoms": "Mosaic-like light and dark green leaf patterns.",
            "precautions": "Remove infected plants as locally advised and clean tools."
        },

        "Tomato___healthy": {
            "cause": "No disease detected by the classifier.",
            "symptoms": "The image appears consistent with a healthy tomato leaf.",
            "precautions": "Continue regular monitoring and good crop management."
        }
    }

    if disease not in advisories:
        return None

    return advisories[disease]


if __name__ == "__main__":

    print("OFFLINE TOMATO FARMER ADVISORY")

    disease = input("Enter predicted disease class: ")

    advisory = get_farmer_advisory(disease)

    if advisory:
        print("\nCause:", advisory["cause"])
        print("Symptoms:", advisory["symptoms"])
        print("Precautions:", advisory["precautions"])
    else:
        print("No advisory available for this disease.")