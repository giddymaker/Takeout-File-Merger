import os
import shutil
from pathlib import Path
import argparse

def merge_takeout_folders(base_dir, output_dir):
    try:
        base_path = Path(base_dir).expanduser()
        output_path = Path(output_dir).expanduser()
        
        # Ensure the output directory exists
        print(f"Creating output directory: {output_path}")
        output_path.mkdir(parents=True, exist_ok=True)

        # Find all Takeout folders
        print(f"Scanning for Takeout folders in: {base_path}")
        takeout_folders = sorted([d for d in base_path.iterdir() if d.is_dir() and d.name.startswith("Takeout ")])
        
        if not takeout_folders:
            print("No Takeout folders found. Exiting.")
            return

        for takeout_folder in takeout_folders:
            print(f"Processing Takeout folder: {takeout_folder}")
            
            # Process both "Drive" and "Google Photos" subdirectories
            for subfolder in ["Drive", "Google Photos"]:
                subfolder_path = takeout_folder / subfolder
                if not subfolder_path.exists():
                    print(f"Skipping folder (no '{subfolder}' subdirectory): {takeout_folder}")
                    continue
                
                print(f"Processing '{subfolder}' subdirectory in: {takeout_folder}")
                for item in subfolder_path.rglob('*'):
                    relative_path = item.relative_to(subfolder_path)
                    dest_path = output_path / subfolder / relative_path
                    
                    try:
                        if item.is_dir():
                            print(f"Creating directory: {dest_path}")
                            dest_path.mkdir(parents=True, exist_ok=True)
                        else:
                            print(f"Moving file: {item} -> {dest_path}")
                            dest_path.parent.mkdir(parents=True, exist_ok=True)
                            if not dest_path.exists():
                                shutil.move(str(item), str(dest_path))
                            else:
                                print(f"Skipping existing file: {dest_path}")
                    except Exception as e:
                        print(f"Error processing item: {item}. Error: {e}")
        
        print("Merge completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge Google Takeout folders into a single directory.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input directory containing Takeout folders.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output directory where files will be merged.")
    
    args = parser.parse_args()
    
    print(f"Starting merge process with input: {args.input} and output: {args.output}")
    merge_takeout_folders(args.input, args.output)