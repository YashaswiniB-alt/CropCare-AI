CropCare AI 🌱

An AI-powered crop disease detection and farmer assistance system that helps identify plant diseases from leaf images and provides preliminary recommendations for disease management.

Overview

CropCare AI uses deep learning-based image classification to identify crop diseases from uploaded leaf images. It supports multiple crop categories and provides disease predictions, severity assessment, and farmer-friendly guidance.

Features

- Multi-crop disease classification
- AI-based plant disease prediction
- MobileNet-based deep learning models
- Disease severity estimation
- Farmer advisory and precautionary recommendations
- Image-based disease analysis
- Mobile access through an Android application

Technology Stack

- Python
- Streamlit
- PyTorch
- MobileNetV2
- MobileNetV3
- OpenCV
- NumPy
- PIL (Pillow)

Project Structure

CropCare-AI/
├── app.py
├── models/
├── src/
├── data/
├── outputs/
├── predict disease.py
├── predict multicrop.py
├── test image.py
├── test mobilenet.py
└── test preprocessing.py

How It Works

1. The user uploads an image of a crop leaf.
2. The application preprocesses the image.
3. A trained deep learning model analyzes the image.
4. The system predicts the possible crop disease.
5. The application displays the prediction and related farmer advisory.

Installation

Clone the repository:

git clone https://github.com/YOUR-USERNAME/CropCare-AI.git
cd CropCare-AI

Install the required Python packages:

pip install -r requirements.txt

Run the application:

streamlit run app.py

Project Goal

The goal of CropCare AI is to make crop disease identification more accessible to farmers using artificial intelligence, helping them recognize potential plant health problems and take informed action.

Disclaimer

CropCare AI provides AI-based preliminary predictions and advisory. It should not replace professional agricultural guidance.

Project Status

Developed as a student AI project for crop disease identification and farmer assistance.
