# UXO Detection System

A machine learning-based system for detecting and classifying Unexploded Ordnance (UXO) using computer vision techniques.

## Project Overview

This project implements a deep learning solution for detecting and classifying UXO in images. The system uses state-of-the-art object detection models (YOLOv8/Faster R-CNN) to identify and classify different types of UXO with high accuracy and real-time processing capabilities.

## Features

- Multi-class UXO detection
- Real-time processing and visualization
- Confidence scoring
- Interactive web interface
- Model performance tracking with MLflow
- Data versioning with DVC
- RESTful API with FastAPI
- Docker containerization

## Project Structure

```
uxo-detection/
├── data/               # Dataset and data processing scripts
├── models/            # Trained models and model definitions
├── src/               # Source code
│   ├── api/          # FastAPI backend
│   ├── frontend/     # React/Streamlit frontend
│   ├── ml/           # ML training and inference code
│   └── utils/        # Utility functions
├── tests/            # Test suite
├── notebooks/        # Jupyter notebooks for analysis
├── docs/            # Documentation
└── docker/          # Docker configuration
```

## Setup Instructions

1. Clone the repository:
```bash
git clone [repository-url]
cd uxo-detection
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize DVC:
```bash
dvc init
```

## Usage

[To be added after implementation]

## Contributing

[To be added]

## License

[To be added]

## Contact

[To be added] 