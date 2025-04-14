import os
from pathlib import Path
import json
import shutil

def scale_labels():
    # Define paths
    interim_dir = Path('data/interim')
    processed_dir = Path('data/processed')
    
    # Create processed directories
    gopro_dir = processed_dir / 'gopro'
    labels_dir = processed_dir / 'labels'
    sonar_dir = processed_dir / 'aris_polar'
    
    # Create directories if they don't exist
    gopro_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    sonar_dir.mkdir(parents=True, exist_ok=True)
    
    # Scale factor
    scale = 3  # 1920/640
    
    # Process all files
    print("Processing files...")
    total_files = 0
    
    # Get all JSON files
    json_files = list((interim_dir / 'labels').glob('*.json'))
    total_files = len(json_files)
    
    for json_path in json_files:
        # Get corresponding image and sonar files
        img_path = interim_dir / 'gopro' / f"{json_path.stem}.jpg"
        sonar_path = interim_dir / 'aris_polar' / f"{json_path.stem}.png"
        
        # Load and scale JSON
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Scale coordinates
        data['x_min'] = int(data['x_min'] * scale)
        data['y_min'] = int(data['y_min'] * scale)
        data['x_max'] = int(data['x_max'] * scale)
        data['y_max'] = int(data['y_max'] * scale)
        
        # Save scaled JSON
        new_json_path = labels_dir / json_path.name
        with open(new_json_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        # Copy image and sonar files
        shutil.copy2(img_path, gopro_dir / img_path.name)
        shutil.copy2(sonar_path, sonar_dir / sonar_path.name)
        
        print(f"Processed {json_path.name}")
    
    print(f"\nProcessing complete!")
    print(f"Total files processed: {total_files}")
    print(f"Files moved to processed directory:")
    print(f"- GoPro images: {len(list(gopro_dir.glob('*.jpg')))}")
    print(f"- Scaled labels: {len(list(labels_dir.glob('*.json')))}")
    print(f"- Sonar data: {len(list(sonar_dir.glob('*.png')))}")

if __name__ == "__main__":
    scale_labels() 