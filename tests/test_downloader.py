
import unittest
from pathlib import Path
from src.downloader import download_images


class TestDownloader(unittest.TestCase):
    def test_download_images_with_real_urls(self):
        # Préparer les données de test
        urls = [
            'https://picsum.photos/id/1058/400/400.jpg',
            'https://picsum.photos/id/1025/400/400.jpg'
        ]
        output_dir = Path('test_output')
        output_dir.mkdir(exist_ok=True)

        # Exécuter la fonction
        image_paths = download_images(urls, output_dir)

        # Vérifier que les images ont été téléchargées
        self.assertEqual(len(image_paths), 2)
        for path in image_paths:
            self.assertTrue(path.exists())
            self.assertTrue(path.name.startswith('https___picsum.photos_id_'))
            self.assertTrue(path.name.endswith('.png'))

        # Nettoyer les fichiers créés
        for path in image_paths:
            path.unlink()
        output_dir.rmdir()
    
    def test_download_images_failure(self):
        # Préparer les données de test avec des URLs invalides
        urls = [
            'http://invalid-url.example.com/nonexistent_image.jpg',
            'http://thisurldoesnotexist.tld/image.png'
        ]
        output_dir = Path('test_output')
        output_dir.mkdir(exist_ok=True)
        
        # Exécuter la fonction
        image_paths = download_images(urls, output_dir)
        
        # Vérifier qu'aucune image n'a été téléchargée
        self.assertEqual(len(image_paths), 0)
        
        # Nettoyer
        output_dir.rmdir()

if __name__ == '__main__':
    unittest.main()
