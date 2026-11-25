def get_farmer_advisory(disease):

    disease_name = disease.replace("___", " - ").replace("_", " ")

    advisories = {

        "Tomato___Early_blight": {
            "cause": "Fungal infection.",
            "symptoms": "Brown spots with concentric rings on older leaves.",
            "precautions": "Remove infected leaves and avoid wetting foliage."
        },

        "Tomato___Late_blight": {
            "cause": "Disease caused by a fungus-like organism.",
            "symptoms": "Dark water-soaked patches that may spread rapidly.",
            "precautions": "Remove affected plant material and avoid overhead irrigation."
        },

        "Tomato___Bacterial_spot": {
            "cause": "Bacterial infection.",
            "symptoms": "Small dark spots on leaves.",
            "precautions": "Remove infected plant debris and avoid overhead watering."
        },

        "Tomato___healthy": {
            "cause": "No disease detected by the classifier.",
            "symptoms": "The leaf appears healthy.",
            "precautions": "Continue regular monitoring and proper crop management."
        }
    }

    if disease in advisories:
        return advisories[disease]

    if "healthy" in disease.lower():
        return {
            "cause": "The AI model classified this leaf as healthy.",
            "symptoms": "No major disease symptoms were detected in the uploaded image.",
            "precautions": "Maintain proper watering, nutrition and regular crop monitoring."
        }

    return {
        "cause": f"Possible plant health issue detected: {disease_name}.",
        "symptoms": "Look for leaf spots, yellowing, curling, wilting or unusual growth. AI predictions are not confirmed diagnoses.",
        "precautions": "Remove severely affected leaves where appropriate, maintain good airflow, avoid excess moisture and consult a local agricultural expert before applying pesticides."
    }