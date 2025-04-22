from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io
import os
import logging
import base64 

# Initialize Flask
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# --- Configuration --- #
MODEL_PATH = os.getenv("MODEL_PATH", "uxo_detection_api/YOLO_uxo.pt")

# --- Model Loading --- #
def load_model():
    """Load YOLO model"""
    model = YOLO(MODEL_PATH)
    return model

model = load_model()

# --- API Endpoints --- #
@app.route("/detect", methods=["POST"])
def detect():
    """Detect UXOs and return bounding boxes"""
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"status": "error", "message": "Empty file"}), 400
    
    try:
        # Process image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        results = model.predict(image)
        annotated_img = results[0].plot()  # Image with boxes (numpy array)
        annotated_img = Image.fromarray(annotated_img[..., ::-1])  # BGR → RGB

        # Convert to base64
        img_byte_arr = io.BytesIO()
        annotated_img.save(img_byte_arr, format='JPEG')
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        
        # Get detections
        detections = []
        for r in results:
            for box in r.boxes:
                detections.append({
                    "class": model.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                })

        # Return JSON (matches classification API format)
        return jsonify({
            "status": "success",
            "detections": detections,
            "annotated_image": img_base64,  # Base64 string
            "image_format": "jpg"
        })

    except Exception as e:
        app.logger.error(f"Detection failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "UXO Detection API",
        "model": "YOLOv8"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)  # Different port than classification