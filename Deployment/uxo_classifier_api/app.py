from flask import Flask, request, jsonify
from flask_cors import CORS  
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms, models
import io
import logging
import os

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Enable CORS
logging.basicConfig(level=logging.INFO)

# --- Configuration --- #
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = os.getenv("MODEL_PATH", "resnet18_uxo.pt")  # Environment variable support

# --- Model Loading --- #
def load_model():
    """Centralized model loading function"""
    model = models.resnet18(pretrained=False)
    model.fc = nn.Sequential(
        nn.Linear(512, 256),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(256, 1),
        nn.Sigmoid()
    )
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model = model.to(DEVICE)
    model.eval()
    return model

model = load_model()

# --- Preprocessing --- #
TARGET_SIZE = (224, 414)  
TRAIN_MEAN = [0.485, 0.456, 0.406]
TRAIN_STD = [0.229, 0.224, 0.225]

transform = transforms.Compose([
    transforms.Resize(TARGET_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=TRAIN_MEAN, std=TRAIN_STD)
])

# --- API Endpoints --- #
@app.route("/classify", methods=["POST"])
def classify():
    """Classify UXO vs Non-UXO"""
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"status": "error", "message": "Empty file"}), 400
    
    try:
        # Preprocess
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        input_tensor = transform(image).unsqueeze(0).to(DEVICE)

        # Predict
        with torch.no_grad():
            prob = model(input_tensor).item()
            prediction = 1 if prob > 0.5 else 0

        return jsonify({
            "status": "success",
            "prediction": int(prediction),
            "confidence": float(prob),
            "class": "UXO" if prediction == 1 else "Non-UXO"
        })

    except Exception as e:
        app.logger.error(f"Classification failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "UXO Classification API",
        "device": str(DEVICE)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)