# UXO Detection System UI

A simple Streamlit-based UI for the UXO Detection System that allows users to:
1. Upload sonar data for UXO classification using a RESNET18 model
2. Upload images for UXO detection with bounding boxes using a YOLO model

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Running with Docker

1. Build the Docker image:
```bash
docker build -t uxo-ui .
```

2. Run the container:
```bash
docker run -p 8501:8501 uxo-ui
```

3. Access the application at http://localhost:8501

## Note
This UI is designed to work with the existing UXO classification and detection APIs. Make sure the APIs are running and accessible before using the UI. 