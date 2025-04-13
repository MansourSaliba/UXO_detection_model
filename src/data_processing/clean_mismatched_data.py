import os
from pathlib import Path
import re

def get_number_from_filename(filename):
    # Extract number from filename using regex
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else None

def clean_mismatched_data():
    # Define paths
    interim_dir = Path('data/interim')
    
    # Process each date folder
    for date_folder in interim_dir.iterdir():
        if not date_folder.is_dir():
            continue
            
        print(f"\nProcessing {date_folder.name}:")
        
        # Get paths for each data type
        gopro_dir = date_folder / 'gopro'
        labels_dir = date_folder / 'labels'
        sonar_dir = date_folder / 'aris_polar'
        
        # Get all files and their numbers
        gopro_files = {get_number_from_filename(f.name): f for f in gopro_dir.glob('*') if f.is_file()}
        label_files = {get_number_from_filename(f.name): f for f in labels_dir.glob('*') if f.is_file()}
        sonar_files = {get_number_from_filename(f.name): f for f in sonar_dir.glob('*') if f.is_file()}
        
        # Print initial counts
        print(f"Initial counts:")
        print(f"GoPro images: {len(gopro_files)}")
        print(f"Labels: {len(label_files)}")
        print(f"Sonar data: {len(sonar_files)}")
        
        # Find common numbers across all three sets
        common_numbers = set(gopro_files.keys()) & set(label_files.keys()) & set(sonar_files.keys())
        
        # Remove files that don't have matches in all three folders
        for num in set(gopro_files.keys()) - common_numbers:
            gopro_files[num].unlink()
            print(f"Removed unmatched GoPro file: {gopro_files[num].name}")
            
        for num in set(label_files.keys()) - common_numbers:
            label_files[num].unlink()
            print(f"Removed unmatched label file: {label_files[num].name}")
            
        for num in set(sonar_files.keys()) - common_numbers:
            sonar_files[num].unlink()
            print(f"Removed unmatched sonar file: {sonar_files[num].name}")
        
        # Print final counts
        print(f"\nFinal counts after cleaning:")
        print(f"GoPro images: {len(list(gopro_dir.glob('*')))}")
        print(f"Labels: {len(list(labels_dir.glob('*')))}")
        print(f"Sonar data: {len(list(sonar_dir.glob('*')))}")

if __name__ == "__main__":
    clean_mismatched_data() 