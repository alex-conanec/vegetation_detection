import requests
from pathlib import Path
from typing import List
from PIL import Image
from io import BytesIO

def download_images(urls: List[str], output_dir: Path) -> List[Path]:
    """
    Download images from a list of URLs and save them in PNG format in the output directory.

    Args:
        urls (List[str]): List of image URLs to download.
        output_dir (Path): Path to the directory where images will be saved.

    Returns:
        List[Path]: List of file paths where the images were saved.
    """
    image_paths = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            
            sanitized_url = url.replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_').replace('=', '_')
            image_filename = f"{sanitized_url}.png"
            image_path = output_dir / image_filename
            
            image.save(image_path, format='PNG')
            image_paths.append(image_path)
        except Exception as e:
            print(f"Erreur lors du téléchargement de {url}: {e}")
    return image_paths
