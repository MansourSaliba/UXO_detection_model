import os
from PIL import Image
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def standardize_images(input_dir: str, output_dir: str, target_size: tuple = (1636, 3025)):
    """
    Standardize all images in the input directory to the target size.
    
    Args:
        input_dir (str): Path to input directory containing images
        output_dir (str): Path to output directory for standardized images
        target_size (tuple): Target size (width, height)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all image files
    image_extensions = ('.png', '.jpg', '.jpeg')
    image_files = [f for f in os.listdir(input_dir) 
                  if f.lower().endswith(image_extensions)]
    
    logger.info(f"Found {len(image_files)} images to process")
    
    # Process each image
    for filename in image_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        try:
            with Image.open(input_path) as img:
                # Resize image
                img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                # Save resized image
                img_resized.save(output_path)
                logger.info(f"Processed {filename}")
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    # Define paths
    base_dir = Path("data/processed")
    input_dir = base_dir / "aris_polar"
    output_dir = base_dir / "aris_polar_standardized"
    
    # Standardize images
    standardize_images(str(input_dir), str(output_dir))
    logger.info("Image standardization complete") 