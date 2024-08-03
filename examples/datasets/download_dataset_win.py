"""Script to download benchmark dataset(s)"""

import os
import requests
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import tyro

# dataset names
dataset_names = Literal[
    "mipnerf360",
]

# dataset urls
urls = {"mipnerf360": "http://storage.googleapis.com/gresearch/refraw360/360_v2.zip"}

# rename maps
dataset_rename_map = {"mipnerf360": "360_v2"}


@dataclass
class DownloadData:
    dataset: dataset_names = "mipnerf360"
    save_dir: Path = Path(os.getcwd() + "/data")

    def main(self):
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.dataset_download(self.dataset)

    def dataset_download(self, dataset: dataset_names):
        (self.save_dir / dataset_rename_map[dataset]).mkdir(parents=True, exist_ok=True)

        file_name = Path(urls[dataset]).name

        # download
        try:
            response = requests.get(urls[dataset])
            response.raise_for_status()
            with open(self.save_dir / dataset_rename_map[dataset] / file_name, 'wb') as f:
                f.write(response.content)
            print("File downloaded successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            return

        # if .zip
        if Path(urls[dataset]).suffix == ".zip":
            with zipfile.ZipFile(self.save_dir / dataset_rename_map[dataset] / file_name, 'r') as zip_ref:
        # extract
                zip_ref.extractall(self.save_dir / dataset_rename_map[dataset])
            print("Extraction complete.")
        else:
            print("Unsupported file format for extraction.")

        os.remove(self.save_dir / dataset_rename_map[dataset] / file_name)

if __name__ == "__main__":
    tyro.cli(DownloadData).main()