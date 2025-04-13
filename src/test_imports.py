# Test imports for UXO Detection Project
print("Testing package imports...")

# Data Processing
print("\nTesting data processing packages:")
import numpy as np
print("✓ NumPy version:", np.__version__)
import pandas as pd
print("✓ Pandas version:", pd.__version__)
import sklearn
print("✓ Scikit-learn version:", sklearn.__version__)

# Deep Learning
print("\nTesting deep learning packages:")
import torch
print("✓ PyTorch version:", torch.__version__)
import torchvision
print("✓ Torchvision version:", torchvision.__version__)
from ultralytics import YOLO
print("✓ Ultralytics (YOLO) imported successfully")

# Web Development
print("\nTesting web development packages:")
import fastapi
print("✓ FastAPI version:", fastapi.__version__)
import uvicorn
print("✓ Uvicorn version:", uvicorn.__version__)
import streamlit
print("✓ Streamlit version:", streamlit.__version__)

# MLOps
print("\nTesting MLOps packages:")
import dvc
print("✓ DVC version:", dvc.__version__)
import mlflow
print("✓ MLflow version:", mlflow.__version__)

# Development Tools
print("\nTesting development tools:")
import pytest
print("✓ Pytest version:", pytest.__version__)
import black
print("✓ Black version:", black.__version__)
import flake8
print("✓ Flake8 version:", flake8.__version__)
import isort
print("✓ Isort version:", isort.__version__)

# Documentation
print("\nTesting documentation tools:")
import mkdocs
print("✓ MkDocs version:", mkdocs.__version__)

print("\nAll packages imported successfully!") 