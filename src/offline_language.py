# CropCare AI - Offline Language Support
# No internet or translation API required.

LANGUAGES = {
    "English": "en",
    "Kannada": "kn",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
}

# ---------------- INTERFACE TRANSLATIONS ----------------

TRANSLATIONS = {
    "en": {
        "scan": "Scan a Plant",
        "capture": "Capture Image",
        "upload": "Upload Image",
        "language": "Select Language",
        "prediction": "AI Prediction",
        "disease": "Possible Disease",
        "confidence": "Prediction Confidence",
        "top3": "Top 3 Predictions",
        "advisory": "Farmer Advisory",
        "cause": "Possible Cause",
        "symptoms": "Symptoms",
        "precautions": "Precautions",
        "damage": "Estimated Visible Damage",
        "severity": "Severity Level",
        "healthy": "Healthy",
        "no_disease": "No disease detected by the classifier.",
        "low": "Low",
        "moderate": "Moderate",
        "high": "High",
    },

    "kn": {
        "scan": "ಸಸ್ಯವನ್ನು ಪರೀಕ್ಷಿಸಿ",
        "capture": "ಚಿತ್ರ ತೆಗೆಯಿರಿ",
        "upload": "ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "language": "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "prediction": "AI ಮುನ್ಸೂಚನೆ",
        "disease": "ಸಂಭವನೀಯ ರೋಗ",
        "confidence": "ಮುನ್ಸೂಚನೆಯ ವಿಶ್ವಾಸ ಮಟ್ಟ",
        "top3": "ಅಗ್ರ 3 ಮುನ್ಸೂಚನೆಗಳು",
        "advisory": "ರೈತ ಸಲಹೆ",
        "cause": "ಸಂಭವನೀಯ ಕಾರಣ",
        "symptoms": "ಲಕ್ಷಣಗಳು",
        "precautions": "ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು",
        "damage": "ಅಂದಾಜು ಗೋಚರ ಹಾನಿ",
        "severity": "ಹಾನಿಯ ಮಟ್ಟ",
        "healthy": "ಆರೋಗ್ಯಕರ",
        "no_disease": "ಯಾವುದೇ ರೋಗ ಪತ್ತೆಯಾಗಿಲ್ಲ.",
        "low": "ಕಡಿಮೆ",
        "moderate": "ಮಧ್ಯಮ",
        "high": "ಹೆಚ್ಚು",
    },

    "hi": {
        "scan": "पौधे की जाँच करें",
        "capture": "तस्वीर लें",
        "upload": "चित्र अपलोड करें",
        "language": "भाषा चुनें",
        "prediction": "AI अनुमान",
        "disease": "संभावित रोग",
        "confidence": "अनुमान की विश्वसनीयता",
        "top3": "शीर्ष 3 अनुमान",
        "advisory": "किसान सलाह",
        "cause": "संभावित कारण",
        "symptoms": "लक्षण",
        "precautions": "सावधानियाँ",
        "damage": "अनुमानित दिखाई देने वाली क्षति",
        "severity": "क्षति का स्तर",
        "healthy": "स्वस्थ",
        "no_disease": "कोई रोग नहीं पाया गया।",
        "low": "कम",
        "moderate": "मध्यम",
        "high": "अधिक",
    },

    "ta": {
        "scan": "தாவரத்தை ஆய்வு செய்யவும்",
        "capture": "படம் எடுக்கவும்",
        "upload": "படத்தை பதிவேற்றவும்",
        "language": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "prediction": "AI கணிப்பு",
        "disease": "சாத்தியமான நோய்",
        "confidence": "கணிப்பு நம்பகத்தன்மை",
        "top3": "முதல் 3 கணிப்புகள்",
        "advisory": "விவசாயி ஆலோசனை",
        "cause": "சாத்தியமான காரணம்",
        "symptoms": "அறிகுறிகள்",
        "precautions": "முன்னெச்சரிக்கைகள்",
        "damage": "கணிக்கப்பட்ட வெளிப்படையான சேதம்",
        "severity": "சேதத்தின் அளவு",
        "healthy": "ஆரோக்கியமானது",
        "no_disease": "நோய் எதுவும் கண்டறியப்படவில்லை.",
        "low": "குறைவு",
        "moderate": "மிதமான",
        "high": "அதிகம்",
    },

    "te": {
        "scan": "మొక్కను పరిశీలించండి",
        "capture": "చిత్రాన్ని తీయండి",
        "upload": "చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "language": "భాషను ఎంచుకోండి",
        "prediction": "AI అంచనా",
        "disease": "సంభావ్య వ్యాధి",
        "confidence": "అంచనా విశ్వసనీయత",
        "top3": "మొదటి 3 అంచనాలు",
        "advisory": "రైతు సలహా",
        "cause": "సంభావ్య కారణం",
        "symptoms": "లక్షణాలు",
        "precautions": "జాగ్రత్తలు",
        "damage": "అంచనా వేసిన కనిపించే నష్టం",
        "severity": "నష్టం స్థాయి",
        "healthy": "ఆరోగ్యకరమైనది",
        "no_disease": "వ్యాధి ఏదీ గుర్తించబడలేదు.",
        "low": "తక్కువ",
        "moderate": "మధ్యస్థం",
        "high": "ఎక్కువ",
    },

    "ml": {
        "scan": "ചെടി പരിശോധിക്കുക",
        "capture": "ചിത്രം എടുക്കുക",
        "upload": "ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        "language": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "prediction": "AI പ്രവചനം",
        "disease": "സാധ്യമായ രോഗം",
        "confidence": "പ്രവചന വിശ്വാസ്യത",
        "top3": "മികച്ച 3 പ്രവചനങ്ങൾ",
        "advisory": "കർഷക ഉപദേശം",
        "cause": "സാധ്യമായ കാരണം",
        "symptoms": "ലക്ഷണങ്ങൾ",
        "precautions": "മുൻകരുതലുകൾ",
        "damage": "കണക്കാക്കിയ ദൃശ്യനാശം",
        "severity": "നാശത്തിന്റെ നില",
        "healthy": "ആരോഗ്യമുള്ളത്",
        "no_disease": "രോഗമൊന്നും കണ്ടെത്തിയിട്ടില്ല.",
        "low": "കുറവ്",
        "moderate": "മിതമായ",
        "high": "കൂടുതൽ",
    },
}
def get_text(language, key):
    """Get a locally stored translation of an interface label."""
    language_code = LANGUAGES.get(language, "en")
    return TRANSLATIONS.get(language_code, TRANSLATIONS["en"]).get(
        key, TRANSLATIONS["en"].get(key, key)
    )


# Disease name translations for tested predictions
DISEASE_TRANSLATIONS = {
    "Bacterial spot": {
        "kn": "ಬ್ಯಾಕ್ಟೀರಿಯಾ ಎಲೆ ಚುಕ್ಕೆ ರೋಗ",
        "hi": "बैक्टीरियल धब्बा रोग",
        "ta": "பாக்டீரியா புள்ளி நோய்",
        "te": "బ్యాక్టీరియా మచ్చ వ్యాధి",
        "ml": "ബാക്ടീരിയൽ പുള്ളി രോഗം",
    },
    "Early blight": {
        "kn": "ಆರಂಭಿಕ ಎಲೆ ಅಂಗಮಾರಿ",
        "hi": "अर्ली ब्लाइट रोग",
        "ta": "ஆரம்ப இலை கருகல் நோய்",
        "te": "ప్రారంభ ఆకుమచ్చ తెగులు",
        "ml": "ആദ്യകാല ഇലപ്പുള്ളി രോഗം",
    },
    "Tomato Yellow Leaf Curl Virus": {
        "kn": "ಟೊಮೇಟೊ ಹಳದಿ ಎಲೆ ಮುರುಕು ವೈರಸ್",
        "hi": "टमाटर पीली पत्ती मुड़ने वाला वायरस",
        "ta": "தக்காளி மஞ்சள் இலை சுருள் வைரஸ்",
        "te": "టమాటా పసుపు ఆకు ముడత వైరస్",
        "ml": "തക്കാളി മഞ്ഞ ഇല ചുരുളൽ വൈറസ്",
    },
    "Leaf Mold": {
        "kn": "ಎಲೆ ಅಚ್ಚು ರೋಗ",
        "hi": "पत्ती फफूंदी रोग",
        "ta": "இலை பூஞ்சை நோய்",
        "te": "ఆకు బూజు వ్యాధి",
        "ml": "ഇല പൂപ്പൽ രോഗം",
    },
    "Healthy": {
        "kn": "ಆರೋಗ್ಯಕರ",
        "hi": "स्वस्थ",
        "ta": "ஆரோக்கியமானது",
        "te": "ఆరోగ్యకరమైనది",
        "ml": "ആരോഗ്യമുള്ളത്",
    },
}


def translate_disease(disease_name, language):
    """Translate known disease names offline."""
    language_code = LANGUAGES.get(language, "en")

    if language_code == "en":
        return disease_name

    translations = DISEASE_TRANSLATIONS.get(disease_name)

    if translations:
        return translations.get(language_code, disease_name)

    # Unknown disease: preserve the original model label.
    return disease_name

    ADVISORY_TRANSLATIONS = {
    "Kannada": {
        "Bacterial spot": {
            "cause": "ಬ್ಯಾಕ್ಟೀರಿಯಾದ ಸೋಂಕಿನಿಂದ ಉಂಟಾಗುತ್ತದೆ.",
            "symptoms": "ಎಲೆಗಳ ಮೇಲೆ ಸಣ್ಣ ಕಪ್ಪು ಅಥವಾ ಕಂದು ಬಣ್ಣದ ಚುಕ್ಕೆಗಳು ಕಾಣಿಸಿಕೊಳ್ಳುತ್ತವೆ.",
            "precautions": "ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆದುಹಾಕಿ. ಎಲೆಗಳ ಮೇಲೆ ನೇರವಾಗಿ ನೀರು ಹಾಕಬೇಡಿ."
        },
        "Early blight": {
            "cause": "ಶಿಲೀಂಧ್ರದ ಸೋಂಕಿನಿಂದ ಉಂಟಾಗುತ್ತದೆ.",
            "symptoms": "ಹಳೆಯ ಎಲೆಗಳ ಮೇಲೆ ಕಂದು ಚುಕ್ಕೆಗಳು ಮತ್ತು ವೃತ್ತಾಕಾರದ ಗುರುತುಗಳು ಕಾಣಿಸಿಕೊಳ್ಳುತ್ತವೆ.",
            "precautions": "ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಎಲೆಗಳು ಒದ್ದೆಯಾಗುವುದನ್ನು ತಪ್ಪಿಸಿ."
        },
        "Healthy": {
            "cause": "ಯಾವುದೇ ಪ್ರಮುಖ ರೋಗದ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿಲ್ಲ.",
            "symptoms": "ಎಲೆ ಆರೋಗ್ಯಕರವಾಗಿ ಕಾಣುತ್ತದೆ.",
            "precautions": "ನಿಯಮಿತವಾಗಿ ನೀರು ಹಾಕಿ ಮತ್ತು ಸಸ್ಯದ ಆರೋಗ್ಯವನ್ನು ಗಮನಿಸಿ."
        }
    },

    "Hindi": {
        "Bacterial spot": {
            "cause": "यह बैक्टीरिया के संक्रमण के कारण होता है।",
            "symptoms": "पत्तियों पर छोटे काले या भूरे धब्बे दिखाई देते हैं।",
            "precautions": "संक्रमित पत्तियों को हटा दें और पत्तियों पर सीधे पानी न डालें।"
        },
        "Early blight": {
            "cause": "यह फफूंद के संक्रमण के कारण होता है।",
            "symptoms": "पुरानी पत्तियों पर भूरे धब्बे और गोलाकार निशान दिखाई देते हैं।",
            "precautions": "संक्रमित पत्तियों को हटा दें और पत्तियों को गीला होने से बचाएँ।"
        },
        "Healthy": {
            "cause": "कोई प्रमुख रोग लक्षण दिखाई नहीं दे रहे हैं।",
            "symptoms": "पत्ती स्वस्थ दिखाई देती है।",
            "precautions": "नियमित रूप से पानी दें और पौधे के स्वास्थ्य पर ध्यान दें।"
        }
    },

    "Tamil": {
        "Bacterial spot": {
            "cause": "பாக்டீரியா தொற்றால் ஏற்படுகிறது.",
            "symptoms": "இலைகளில் சிறிய கருப்பு அல்லது பழுப்பு நிற புள்ளிகள் தோன்றும்.",
            "precautions": "பாதிக்கப்பட்ட இலைகளை அகற்றவும். இலைகளின் மீது நேரடியாக நீர் ஊற்ற வேண்டாம்."
        },
        "Early blight": {
            "cause": "பூஞ்சை தொற்றால் ஏற்படுகிறது.",
            "symptoms": "பழைய இலைகளில் பழுப்பு நிற புள்ளிகளும் வட்ட வடிவ அடையாளங்களும் தோன்றும்.",
            "precautions": "பாதிக்கப்பட்ட இலைகளை அகற்றி இலைகள் ஈரமாகாமல் பார்த்துக்கொள்ளவும்."
        },
        "Healthy": {
            "cause": "குறிப்பிடத்தக்க நோய் அறிகுறிகள் காணப்படவில்லை.",
            "symptoms": "இலை ஆரோக்கியமாகத் தெரிகிறது.",
            "precautions": "தொடர்ந்து தண்ணீர் ஊற்றி செடியின் ஆரோக்கியத்தை கண்காணிக்கவும்."
        }
    },

    "Telugu": {
        "Bacterial spot": {
            "cause": "బాక్టీరియా సంక్రమణ వల్ల వస్తుంది.",
            "symptoms": "ఆకులపై చిన్న నల్లటి లేదా గోధుమ రంగు మచ్చలు కనిపిస్తాయి.",
            "precautions": "సోకిన ఆకులను తొలగించండి. ఆకులపై నేరుగా నీరు పోయవద్దు."
        },
        "Early blight": {
            "cause": "శిలీంధ్ర సంక్రమణ వల్ల వస్తుంది.",
            "symptoms": "పాత ఆకులపై గోధుమ రంగు మచ్చలు మరియు వలయాకార గుర్తులు కనిపిస్తాయి.",
            "precautions": "సోకిన ఆకులను తొలగించి ఆకులు తడవకుండా జాగ్రత్తపడండి."
        },
        "Healthy": {
            "cause": "ప్రధాన వ్యాధి లక్షణాలు కనిపించడం లేదు.",
            "symptoms": "ఆకు ఆరోగ్యంగా కనిపిస్తోంది.",
            "precautions": "క్రమం తప్పకుండా నీరు పోసి మొక్క ఆరోగ్యాన్ని గమనించండి."
        }
    },

    "Malayalam": {
        "Bacterial spot": {
            "cause": "ബാക്ടീരിയ അണുബാധ മൂലമാണ് ഉണ്ടാകുന്നത്.",
            "symptoms": "ഇലകളിൽ ചെറിയ കറുത്ത അല്ലെങ്കിൽ തവിട്ട് പാടുകൾ കാണപ്പെടുന്നു.",
            "precautions": "രോഗബാധിതമായ ഇലകൾ നീക്കം ചെയ്യുക. ഇലകളിൽ നേരിട്ട് വെള്ളം ഒഴിക്കരുത്."
        },
        "Early blight": {
            "cause": "ഫംഗസ് അണുബാധ മൂലമാണ് ഉണ്ടാകുന്നത്.",
            "symptoms": "പഴയ ഇലകളിൽ തവിട്ട് പാടുകളും വൃത്താകൃതിയിലുള്ള അടയാളങ്ങളും കാണപ്പെടുന്നു.",
            "precautions": "രോഗബാധിതമായ ഇലകൾ നീക്കം ചെയ്യുകയും ഇലകൾ നനയുന്നത് ഒഴിവാക്കുകയും ചെയ്യുക."
        },
        "Healthy": {
            "cause": "പ്രധാന രോഗലക്ഷണങ്ങൾ കണ്ടെത്തിയിട്ടില്ല.",
            "symptoms": "ഇല ആരോഗ്യകരമായി കാണപ്പെടുന്നു.",
            "precautions": "ക്രമമായി വെള്ളം നൽകുകയും ചെടിയുടെ ആരോഗ്യം ശ്രദ്ധിക്കുകയും ചെയ്യുക."
        }
    }
}


def get_advisory_translation(disease_name, language, section):
    disease_name = disease_name.replace("_", " ").strip()

    if language == "English":
        return None

    return (
        ADVISORY_TRANSLATIONS
        .get(language, {})
        .get(disease_name, {})
        .get(section)
    )