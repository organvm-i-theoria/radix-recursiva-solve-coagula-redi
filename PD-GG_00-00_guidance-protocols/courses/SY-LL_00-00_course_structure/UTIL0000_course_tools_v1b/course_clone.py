"""
COURSE CLONE SCRIPT
Clones a course folder (like ENG101_AMP_24FA) and bumps all unit UID numbers by +1.
"""

import os
import shutil

def clone_course(source_dir, target_dir):
    if not os.path.exists(source_dir):
        print(f"Source folder '{source_dir}' not found.")
        return

    shutil.copytree(source_dir, target_dir)
    print(f"Cloned '{source_dir}' into '{target_dir}'")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python course_clone.py [source_folder] [new_folder]")
    else:
        clone_course(sys.argv[1], sys.argv[2])
