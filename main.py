import argparse
from pathlib import Path

from src.downloader import download_images
from src.vegetation_detection import detect_vegetation
from src.image_processing import process_image

def parse_arguments() -> argparse.Namespace:
    """
    Parse les arguments de la ligne de commande.

    Returns:
        argparse.Namespace: Arguments analysés incluant les URLs des images, 
                            le répertoire de sortie, et les flags pour FILL_HOLES et PRETTY_RESULT.
    """
    parser = argparse.ArgumentParser(description="Détection de la végétation dans les images RGB.")
    parser.add_argument('-o', '--output-dir', type=str, required=True, help='Chemin vers le répertoire de sortie.')
    parser.add_argument('image_urls', nargs='+', help='Liste des URLs des images à traiter.')
    parser.add_argument('--fill-holes', action='store_true', default=False, help='Remplir les petits trous dans la végétation détectée.')
    parser.add_argument('--pretty-result', action='store_true', default=False, help='Appliquer un flou en niveaux de gris aux zones non végétales.')
    return parser.parse_args()

def main():
    """
    Main function to execute the image processing pipeline.
    It handles argument parsing, image downloading, vegetation detection, 
    and image processing based on the flags provided.
    """
    args = parse_arguments()
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    images = download_images(args.image_urls, output_path)

    for image_path in images:
        mask = detect_vegetation(image_path)
        processed_image = process_image(
            image_path,
            mask,
            fill_holes=args.fill_holes,
            pretty_result=args.pretty_result
        )
        
        processed_image_filename = f"processed_{image_path.stem}.png"
        processed_image.save(output_path / processed_image_filename)

if __name__ == "__main__":
    main()
