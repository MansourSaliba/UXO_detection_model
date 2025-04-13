import os
from pathlib import Path
import json
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

def verify_scaled_labels(num_samples=3):
    # Define paths
    processed_dir = Path('data/processed')
    gopro_dir = processed_dir / 'gopro'
    labels_dir = processed_dir / 'labels'
    
    # Get all matching pairs
    image_files = list(gopro_dir.glob('*.jpg'))
    random.shuffle(image_files)
    
    # Process random samples
    for img_path in image_files[:num_samples]:
        # Get corresponding label file
        label_path = labels_dir / f"{img_path.stem}.json"
        if not label_path.exists():
            print(f"No matching label for {img_path.name}")
            continue
            
        # Load image
        img = Image.open(img_path)
        img_np = np.array(img)
        
        # Load JSON
        with open(label_path, 'r') as f:
            data = json.load(f)
        
        # Get coordinates
        x_min = data['x_min']
        y_min = data['y_min']
        x_max = data['x_max']
        y_max = data['y_max']
        label = data['class']
        
        # Create visualization
        plt.figure(figsize=(15, 10))
        plt.imshow(img_np)
        
        # Draw bounding box
        rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                               linewidth=2, edgecolor='g', facecolor='none')
        plt.gca().add_patch(rect)
        
        plt.title(f'Scaled Label Verification\nFile: {img_path.name}\nLabel: {label}\n'
                 f'Coordinates: ({x_min}, {y_min}) to ({x_max}, {y_max})')
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    verify_scaled_labels() 