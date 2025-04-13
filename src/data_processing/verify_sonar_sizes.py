import os
from pathlib import Path
from PIL import Image
import numpy as np

def verify_sonar_sizes():
    # Define path
    processed_dir = Path('data/processed')
    sonar_dir = processed_dir / 'aris_polar'
    
    # Check all sonar images
    print("Verifying sonar image sizes...")
    sizes = {}
    total_files = 0
    
    for img_path in sonar_dir.glob('*.png'):
        total_files += 1
        with Image.open(img_path) as img:
            width, height = img.size
            size_key = f"{width}x{height}"
            if size_key not in sizes:
                sizes[size_key] = []
            sizes[size_key].append(img_path.name)
    
    # Print results
    print(f"\nTotal sonar images checked: {total_files}")
    print("\nSize distribution:")
    for size, files in sizes.items():
        print(f"\nSize {size}: {len(files)} files")
        if len(files) < 10:  # Only show filenames if there are few files
            print("Files:")
            for f in files:
                print(f"  - {f}")
    
    # Check if all files have the same size
    if len(sizes) == 1:
        print("\n✅ All sonar images have the same size!")
    else:
        print("\n⚠️ Warning: Sonar images have different sizes!")
        print("This might cause issues during training.")

if __name__ == "__main__":
    verify_sonar_sizes() 