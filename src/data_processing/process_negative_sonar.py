import os
import shutil
from pathlib import Path
from PIL import Image
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define target size to match UXO sonar dimensions
TARGET_SIZE = (1636, 3025)

def process_negative_sonar():
    # Define paths
    raw_dir = Path('data/raw/Negative')
    processed_dir = Path('data/processed/negative_sonar')
    
    # Create processed directory if it doesn't exist
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Process and copy images
    logger.info("Processing and copying images...")
    counter = 1
    for img_path in sorted(raw_dir.glob('*.png')):
        try:
            # Open and resize image
            with Image.open(img_path) as img:
                # Resize to target size
                img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
                
                # Save to processed directory with new name
                new_name = f"{counter}.png"
                new_path = processed_dir / new_name
                img.save(new_path)
                
                logger.info(f"Processed {img_path.name} -> {new_name}")
                counter += 1
                
        except Exception as e:
            logger.error(f"Error processing {img_path.name}: {str(e)}")
    
    # Remove annotations file if it exists
    annotations_path = raw_dir / 'annotations.json'
    if annotations_path.exists():
        annotations_path.unlink()
        logger.info("Removed annotations.json file")
    
    logger.info(f"Processing complete! Processed {counter-1} images")
    logger.info(f"Processed images saved to: {processed_dir}")
    logger.info(f"All images resized to: {TARGET_SIZE}")

if __name__ == "__main__":
    process_negative_sonar() 