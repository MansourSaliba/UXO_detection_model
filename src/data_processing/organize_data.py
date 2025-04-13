import os
import shutil
from pathlib import Path

def organize_data():
    # Define paths
    raw_dir = Path('data/raw')
    interim_dir = Path('data/interim')
    
    # Folders to keep
    keep_folders = ['gopro', 'labels', 'aris_polar']
    
    # Create interim directory if it doesn't exist
    interim_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each date folder
    for date_folder in raw_dir.iterdir():
        if date_folder.is_dir():
            # Create corresponding folder in interim
            interim_date_dir = interim_dir / date_folder.name
            interim_date_dir.mkdir(exist_ok=True)
            
            # Copy only the folders we want to keep
            for folder in keep_folders:
                source_folder = date_folder / folder
                if source_folder.exists():
                    dest_folder = interim_date_dir / folder
                    if dest_folder.exists():
                        shutil.rmtree(dest_folder)  # Remove if exists
                    shutil.copytree(source_folder, dest_folder)
                    print(f"Copied {folder} from {date_folder.name}")

if __name__ == "__main__":
    organize_data() 