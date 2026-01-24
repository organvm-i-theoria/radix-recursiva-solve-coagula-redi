"""
ZIP UNIT SCRIPT
Zips any essay unit folder (e.g., NRTV0100_narrative_essay) for LMS upload or archive.
"""

import zipfile
import os
import sys

def zip_unit(folder_name):
    zip_filename = f"{folder_name}_FULL.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_name):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_name)
                zipf.write(full_path, arcname)
    print(f"Zipped: {zip_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python zip_unit.py [folder_name]")
    else:
        zip_unit(sys.argv[1])
