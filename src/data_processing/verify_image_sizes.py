import os
from pathlib import Path
import json
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

def verify_image_sizes():
    # Define paths
    interim_dir = Path('data/interim')
    gopro_dir = interim_dir / 'gopro'
    labels_dir = interim_dir / 'labels'
    
    # Check all images
    print("Verifying image sizes...")
    incorrect_sizes = []
    total_images = 0
    
    for img_path in gopro_dir.glob('*.jpg'):
        total_images += 1
        with Image.open(img_path) as img:
            width, height = img.size
            if width != 1920 or height != 1080:
                incorrect_sizes.append((img_path.name, width, height))
    
    print(f"\nTotal images checked: {total_images}")
    if incorrect_sizes:
        print("\nImages with incorrect sizes:")
        for name, width, height in incorrect_sizes:
            print(f"{name}: {width}x{height}")
    else:
        print("All images are 1920x1080!")

def visualize_random_samples(num_samples=3):
    # Define paths
    interim_dir = Path('data/interim')
    gopro_dir = interim_dir / 'gopro'
    labels_dir = interim_dir / 'labels'
    
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
        
        # Calculate scaled coordinates
        scale = 3  # 1920/640
        scaled_x_min = x_min * scale
        scaled_y_min = y_min * scale
        scaled_x_max = x_max * scale
        scaled_y_max = y_max * scale
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        
        # Original coordinates
        ax1.imshow(img_np)
        rect1 = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                               linewidth=2, edgecolor='r', facecolor='none')
        ax1.add_patch(rect1)
        ax1.set_title(f'Original Coordinates\nFile: {img_path.name}\nLabel: {label}')
        
        # Scaled coordinates
        ax2.imshow(img_np)
        rect2 = patches.Rectangle((scaled_x_min, scaled_y_min), 
                                scaled_x_max - scaled_x_min, 
                                scaled_y_max - scaled_y_min,
                                linewidth=2, edgecolor='g', facecolor='none')
        ax2.add_patch(rect2)
        ax2.set_title(f'Scaled Coordinates (x{scale})\nFile: {img_path.name}\nLabel: {label}')
        
        # Set limits and legends
        for ax in [ax1, ax2]:
            ax.set_xlim(0, 1920)
            ax.set_ylim(1080, 0)
            ax.legend()
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    verify_image_sizes()
    print("\nVisualizing random samples...")
    visualize_random_samples() 