import os
import json

def generate_catalog(folder, output_file):
    # Get all .zip files in the folder
    files = [f for f in os.listdir(folder) if f.lower().endswith('.zip')]
    # Sort them by name (case-insensitive for better matching)
    files.sort(key=lambda x: x.lower())
    # Write to JSON
    with open(os.path.join(folder, output_file), 'w') as f:
        json.dump(files, f, indent=4)
    print(f"Generated {output_file} in {folder} with {len(files)} entries.")

# Generate for diskimages
generate_catalog('diskimages', 'catalog.json')

# Generate for tapeimages
generate_catalog('tapeimages', 'catalog.json')