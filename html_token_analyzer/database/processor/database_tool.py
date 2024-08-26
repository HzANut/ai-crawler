import os
import py7zr
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict


def _extract_7z_recursive(dir_or_file_path):
    if isinstance(dir_or_file_path, list):
        zip_files = dir_or_file_path
    elif isinstance(dir_or_file_path, str) and os.path.isdir(dir_or_file_path):
        zip_files = Path(dir_or_file_path).rglob("*.7z")
    else:
        zip_files = [dir_or_file_path]

    for zip_file in tqdm(zip_files, desc="Extracting 7z files"):
        zip_file = Path(zip_file)
        file_name = zip_file.name
        if file_name.startswith("."):
            continue

        if zip_file.is_dir():
            continue

        with py7zr.SevenZipFile(zip_file, "r") as archive:
            folder = zip_file.parent
            archive.extractall(folder._str)


def unzip_all_recursive(src_dir):
    zip_files = defaultdict(list)
    for root, dirs, files in os.walk(src_dir, followlinks=True):
        for file in files:
            if file.endswith(".7z"):
                zip_files["7z"].append(os.path.join(root, file))
    _extract_7z_recursive(zip_files["7z"])


if __name__ == "__main__":
    unzip_all_recursive(r"html_token_analyzer\database\swde")