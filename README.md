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

## Data Access

The project data is stored in Google Drive. To access the data:

1. Go to the project's Google Drive folder: [UXO Detection Data](https://drive.google.com/drive/folders/1hJ3EIXnIOz1mGEJpJZVoyiKcS3h6Qlvj)
2. Download the following folders:
   - `raw/`: Original dataset
   - `interim/`: Intermediate processed data
   - `processed/`: Final processed data ready for model training

## Project Structure

```
uxo-detection/
├── data/               # Dataset and data processing scripts
│   ├── raw/           # Original dataset
│   ├── interim/       # Intermediate processed data
│   └── processed/     # Final processed data
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

5. Configure DVC remote:
```bash
dvc remote add -d gdrive gdrive://1hJ3EIXnIOz1mGEJpJZVoyiKcS3h6Qlvj
```

6. Download the data:
   - Manually download from Google Drive (see Data Access section)
   - Place the data in the corresponding directories under `data/`

## Data Versioning

This project uses DVC for data versioning. The data is stored in Google Drive and tracked using DVC metadata files. To update the data:

1. Make changes to the data in the appropriate directory
2. Update DVC tracking:
```bash
dvc add data/raw data/interim data/processed
```
3. Commit the changes:
```bash
git add data/*.dvc
git commit -m "Update data tracking"
```

## Usage

[To be added after implementation]

## Contributing

[To be added]

## License

[To be added]

## Contact

[To be added] 