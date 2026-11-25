import streamlit as st
import torch
import sys
import torch.nn as nn
import cv2
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.local_ai_assistant import ask_farmer_ai
from offline_language import get_text, translate_disease, get_advisory_translation
from torchvision import models, transforms
from PIL import Image
from src.farmer_advisory import get_farmer_advisory
from src.severity_estimation import analyze_leaf

# ==================================================
# 1. APP CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="CropCare AI",
    page_icon="🌿",
    layout="centered"
)

# ==================================================
# 2. DARK GREEN UI THEME
# ==================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071b12, #0b2b1b, #102f20);
    color: #ffffff;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    color: #b6ffb0 !important;
}

.stMarkdown p {
    color: #e2f3e5;
}

[data-testid="stFileUploader"] {
    background: #143b28;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #2d7148;
}

[data-testid="stCameraInput"] {
    background: #143b28;
    border-radius: 12px;
    padding: 10px;
}

.stButton > button {
    background-color: #39b86a;
    color: #ffffff !important;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #55d982;
    color: #062513 !important;
    border: 1px solid #a4ffbf;
}

div[data-testid="stMetric"] {
    background-color: #143b28;
    border: 1px solid #2d7148;
    padding: 15px;
    border-radius: 12px;
}

.stProgress > div > div > div > div {
    background-color: #55d982;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 3. HEADER
# ==================================================

st.title("🌿 CropCare AI")
st.subheader("Smart Plant Health Scanner")

st.write(
    "Capture an image using your camera or upload a plant image "
    "to analyze it, estimate visible damage, and receive precautions."
)

st.info(
    "Prototype limitation: Our AI model analyzes the image to identify "
    "possible plant diseases, estimate visible damage severity, and "
    "provide preventive measures and recommendations."
)

st.divider()

language = st.selectbox(
    "🌐 Select Language",
    ["English", "Kannada", "Hindi", "Tamil", "Telugu", "Malayalam"]
)

st.caption(
    "Language selection is currently a prototype. "
    "Results and advisory are displayed in English."
)

# ==================================================
# 4. LOAD TRAINED MULTICROP MODEL
# ==================================================

@st.cache_resource
def load_model():

    device = torch.device("cpu")

    with open("models/multicrop_labels.json", "r") as f:
        classes = json.load(f)

    model = models.mobilenet_v3_small(weights=None)

    model.classifier[3] = nn.Linear(
        model.classifier[3].in_features,
        len(classes)
    )

    checkpoint = torch.load(
        "models/multicrop_mobilenetv3.pth",
        map_location=device,
        weights_only=False
    )

    model.load_state_dict(checkpoint["model_state_dict"])

    model.to(device)
    model.eval()

    return model, classes, device


model, classes, device = load_model()

# ==================================================
# 5. IMAGE PREPROCESSING
# ==================================================

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ==================================================
# 6. CAMERA OR UPLOAD
# ==================================================

st.header("📷 Scan a Plant")

image_mode = st.radio(
    "Choose image source",
    ["📸 Capture with Camera", "🖼️ Upload Image"]
)

image = None

if image_mode == "📸 Capture with Camera":

    camera_image = st.camera_input(
        "Take a photograph of the plant leaf"
    )

    if camera_image is not None:
        image = Image.open(camera_image).convert("RGB")

else:

    uploaded_image = st.file_uploader(
        "Upload a leaf image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image is not None:
        image = Image.open(uploaded_image).convert("RGB")

# ==================================================
# 7. ANALYZE IMAGE
# ==================================================

if image is not None:

    st.image(
        image,
        caption="Selected Plant Image",
        use_container_width=True
    )

    # IMAGE PREPROCESSING
    input_tensor = transform(image).unsqueeze(0)

    # PREDICTION
    with torch.no_grad():

        outputs = model(input_tensor)

        probabilities = torch.softmax(outputs, dim=1)

        top_count = min(3, len(classes))

        top_probabilities, top_indices = torch.topk(
            probabilities,
            top_count,
            dim=1
        )

    predicted_disease = classes[
        top_indices[0][0].item()
    ]

    confidence = (
        top_probabilities[0][0].item() * 100
    )

    if "___" in predicted_disease:

        crop_name, disease_name = predicted_disease.split("___", 1)

        display_name = (
            crop_name + " - " + disease_name.replace("_", " ")
        )

    else:

        display_name = predicted_disease.replace("_", " ")

    # ==================================================
    # 8. DISEASE DETECTION RESULTS
    # ==================================================

    st.divider()
    st.header("🔬 Disease Detection Results")

    if "healthy" in predicted_disease.lower():

        st.success(
            f"🌱 Predicted Condition: {display_name}"
        )

    else:

        st.warning(
            f"Possible Disease: {display_name}"
        )

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    if confidence < 50:

        st.warning(
            "The model has low confidence in this result. "
            "Try a clearer leaf photograph with better lighting. "
            "The prediction may be incorrect."
        )

    # ==================================================
    # 9. TOP 3 PREDICTIONS
    # ==================================================

    st.subheader("Top 3 Possible Conditions")

    for i in range(top_count):

        disease = classes[
            top_indices[0][i].item()
        ]

        score = top_probabilities[0, i].item()

        percentage = score * 100

        if "___" in disease:

            crop_name, condition_name = disease.split("___", 1)

            disease_name = (
                crop_name + " - " + condition_name.replace("_", " ")
            )

        else:

            disease_name = disease.replace("_", " ")

        st.write(
            f"**{i + 1}. {disease_name}**"
        )

        st.progress(float(score))

        st.caption(
            f"Confidence: {percentage:.2f}%"
        )

    # ==================================================
    # 10. FARMER ADVISORY
    # ==================================================

    advisory = get_farmer_advisory(predicted_disease)

    st.divider()
    st.header("🌱 Farmer Advisory")

    if advisory:

        st.write("**Cause:**")
        st.write(advisory["cause"])

        st.write("**Symptoms:**")
        st.write(advisory["symptoms"])

        st.write("**Precautions:**")
        st.write(advisory["precautions"])

    else:

        st.info("No advisory is available for this prediction.")

    # ==================================================
    # 11. VISIBLE DAMAGE ESTIMATION
    # ==================================================

    st.divider()
    st.header("📊 Visible Damage Estimation")

    os.makedirs("outputs", exist_ok=True)

    image_path = "outputs/streamlit_leaf.jpg"

    image.save(image_path)

    severity_result = analyze_leaf(image_path)

    damage_percentage = None
    severity = None

    if severity_result is not None:

        damage_percentage, severity = severity_result

        st.metric(
            "Estimated Visible Damage",
            f"{damage_percentage:.2f}%"
        )

        if "healthy" in predicted_disease.lower():

            st.write(
                "**Estimated Severity Level:** "
                "Healthy / No significant visible damage"
            )

        else:

            st.write(
                f"**Estimated Severity Level:** {severity}"
            )

        # DAMAGE VISUALIZATION
        visual_path = "outputs/severity_visual.png"

        if os.path.exists(visual_path):

            visual = cv2.imread(visual_path)

            if visual is not None:

                visual = cv2.cvtColor(
                    visual,
                    cv2.COLOR_BGR2RGB
                )

                st.image(
                    visual,
                    caption="Visualized Leaf Damage",
                    use_container_width=True
                )

    else:

        st.warning(
            "Unable to estimate visible damage for this image."
        )

    # ==================================================
    # 12. PREPARE SCAN CONTEXT FOR THE LLM
    # ==================================================

    scan_context = (
        f"Predicted crop/disease: {display_name}\n"
        f"Prediction confidence: {confidence:.2f}%\n"
    )

    if damage_percentage is not None:

        scan_context += (
            f"Estimated visible damage: {damage_percentage:.2f}%\n"
            f"Estimated severity: {severity}\n"
        )

    else:

        scan_context += (
            "Visible damage estimation was unavailable.\n"
        )

    if advisory:

        scan_context += (
            f"Cause: {advisory.get('cause', 'Not available')}\n"
            f"Symptoms: {advisory.get('symptoms', 'Not available')}\n"
            f"Precautions: {advisory.get('precautions', 'Not available')}\n"
        )

    # Store the latest scan results for the chatbot
    st.session_state.latest_scan_context = scan_context

    # ==================================================
    # 13. DISCLAIMER
    # ==================================================

    st.divider()

    st.caption(
        "CropCare AI is an experimental prototype. "
        "Disease predictions and visible damage estimates may be inaccurate. "
        "Verify results before taking crop treatment decisions."
    )

# ==================================================
# 14. FARMER AI ASSISTANT
# ==================================================

st.divider()
st.header("🤖 CropCare AI - Farmer Assistant")
st.caption("Ask farming questions. Powered by local AI.")

# Initialize chat history
if "farmer_chat_history" not in st.session_state:

    st.session_state.farmer_chat_history = []

# Initialize scan context if not available
if "latest_scan_context" not in st.session_state:

    st.session_state.latest_scan_context = None

# Display previous conversation
for chat in st.session_state.farmer_chat_history:

    with st.chat_message(chat["role"]):

        st.markdown(chat["content"])

user_question = st.chat_input(
    "Ask about crop diseases, watering, or prevention..."
)

if user_question:

    st.session_state.farmer_chat_history.append(
        {"role": "user", "content": user_question}
    )

    with st.chat_message("user"):

        st.markdown(user_question)

    with st.chat_message("assistant"):

        with st.spinner("CropCare AI is thinking..."):

            answer = ask_farmer_ai(
                user_question,
                st.session_state.latest_scan_context
            )

            st.markdown(answer)

    st.session_state.farmer_chat_history.append(
        {"role": "assistant", "content": answer}
    )