import unittest
import numpy as np
from pathlib import Path
from PIL import Image
from src.vegetation_detection import detect_vegetation

class TestVegetationDetection(unittest.TestCase):
    def test_detect_vegetation(self):
        # Créer une image de test avec une zone verte
        image_array = np.zeros((100, 100, 3), dtype=np.uint8)
        image_array[25:75, 25:75] = [0, 255, 0]  # Carré vert au centre
        test_image = Image.fromarray(image_array)
        test_image_path = Path('test_image.png')
        test_image.save(test_image_path)
        
        # Exécuter la fonction
        mask = detect_vegetation(test_image_path)
        
        # Vérifier que la zone verte est détectée
        self.assertTrue(mask[50, 50])
        self.assertFalse(mask[10, 10])
        
        # Nettoyer
        test_image_path.unlink()

if __name__ == '__main__':
    unittest.main()
