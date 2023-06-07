import os
import gzip
import shutil

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

source_folder = str(BASE_DIR / 'data/GTSP_symmetric')
destination_folder = source_folder


def extract_all_gz_files_to_new_folder(src_folder_path, dest_folder_path):
    for root, dirs, files in os.walk(src_folder_path):
        for file in files:
            if file.endswith(".gz"):
                file_path = os.path.join(root, file)
                with gzip.open(file_path, 'rb') as f_in:
                    with open(os.path.join(dest_folder_path, file[:-3]), 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)


extract_all_gz_files_to_new_folder(source_folder, destination_folder)

