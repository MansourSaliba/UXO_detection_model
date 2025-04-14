import os
from pathlib import Path
import shutil
import re

def get_number_from_filename(filename):
    # Extract number from filename using regex
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else None

def reorganize_data():
    # Define paths
    interim_dir = Path('data/interim')
    
    # Create new directories for flattened structure
    gopro_dir = interim_dir / 'gopro'
    labels_dir = interim_dir / 'labels'
    sonar_dir = interim_dir / 'aris_polar'
    
    # Create directories if they don't exist
    gopro_dir.mkdir(exist_ok=True)
    labels_dir.mkdir(exist_ok=True)
    sonar_dir.mkdir(exist_ok=True)
    
    # Counter for new file names
    new_counter = 1
    
    # Process each date folder
    for date_folder in sorted(interim_dir.iterdir()):
        if not date_folder.is_dir() or date_folder.name in ['gopro', 'labels', 'aris_polar']:
            continue
            
        print(f"\nProcessing {date_folder.name}:")
        
        # Get source directories
        src_gopro = date_folder / 'gopro'
        src_labels = date_folder / 'labels'
        src_sonar = date_folder / 'aris_polar'
        
        # Get all files and their numbers
        gopro_files = {get_number_from_filename(f.name): f for f in src_gopro.glob('*') if f.is_file()}
        label_files = {get_number_from_filename(f.name): f for f in src_labels.glob('*') if f.is_file()}
        sonar_files = {get_number_from_filename(f.name): f for f in src_sonar.glob('*') if f.is_file()}
        
        # Find common numbers across all three sets
        common_numbers = sorted(set(gopro_files.keys()) & set(label_files.keys()) & set(sonar_files.keys()))
        
        # Process each matching set of files
        for num in common_numbers:
            # Get the files
            gopro_file = gopro_files[num]
            label_file = label_files[num]
            sonar_file = sonar_files[num]
            
            # Create new filenames
            new_gopro = gopro_dir / f"{new_counter}.jpg"  # Assuming jpg for gopro
            new_label = labels_dir / f"{new_counter}.json"  # Assuming json for labels
            new_sonar = sonar_dir / f"{new_counter}.png"  # Assuming png for sonar
            
            # Copy files with new names
            shutil.copy2(gopro_file, new_gopro)
            shutil.copy2(label_file, new_label)
            shutil.copy2(sonar_file, new_sonar)
            
            print(f"Processed set {num} -> {new_counter}")
            new_counter += 1
            
        # Remove the old directories
        if src_gopro.exists():
            shutil.rmtree(src_gopro)
        if src_labels.exists():
            shutil.rmtree(src_labels)
        if src_sonar.exists():
            shutil.rmtree(src_sonar)
            
        # Remove the date folder if it's empty
        if not any(date_folder.iterdir()):
            date_folder.rmdir()
            print(f"Removed empty directory: {date_folder.name}")
    
    print(f"\nReorganization complete. Total processed sets: {new_counter - 1}")

if __name__ == "__main__":
    reorganize_data() 