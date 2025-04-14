import os
import shutil
from pathlib import Path

def cleanup_aris_polar():
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # Path to the aris_polar folder in processed
    aris_polar_path = project_root / 'data' / 'processed' / 'aris_polar'
    
    # Check if the folder exists
    if aris_polar_path.exists():
        print(f"Removing {aris_polar_path}")
        shutil.rmtree(aris_polar_path)
        print("aris_polar folder removed successfully")
    else:
        print("aris_polar folder not found")

if __name__ == "__main__":
    cleanup_aris_polar() 