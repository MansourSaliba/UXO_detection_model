import json
import os
from pathlib import Path
import time

def update_labels():
    # Path to the labels directory
    labels_dir = Path('data/processed/labels')
    
    # Create a log file to track progress
    log_file = Path('label_update_progress.log')
    processed_files = set()
    
    # Load previously processed files if log exists
    if log_file.exists():
        with open(log_file, 'r') as f:
            processed_files = set(f.read().splitlines())
    
    # Get all JSON files
    all_json_files = list(labels_dir.glob('*.json'))
    total_files = len(all_json_files)
    
    print(f"Total files to process: {total_files}")
    print(f"Already processed: {len(processed_files)}")
    
    # Process each file
    for i, json_file in enumerate(all_json_files, 1):
        if str(json_file) in processed_files:
            continue
            
        try:
            # Read the JSON file
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Update the class to "Unexploded Ordnance"
            data['class'] = 'Unexploded Ordnance'
            
            # Write the updated data back to the file
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=4)
            
            # Log the processed file
            with open(log_file, 'a') as f:
                f.write(f"{json_file}\n")
            
            print(f"Updated {json_file.name} ({i}/{total_files})")
            
            # Small delay to prevent overwhelming the system
            time.sleep(0.01)
            
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {json_file.name}: {str(e)}")
        except PermissionError as e:
            print(f"Permission error for {json_file.name}: {str(e)}")
        except Exception as e:
            print(f"Error processing {json_file.name}: {str(e)}")
            # Don't log failed files to allow retry
            continue

if __name__ == "__main__":
    update_labels() 