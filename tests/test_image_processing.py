import unittest
import numpy as np
from pathlib import Path
from PIL import Image
from src.image_processing import process_image, fill_small_holes, apply_white_background, apply_pretty_effect

class TestImageProcessing(unittest.TestCase):
    def setUp(self):
        # Créer une image de test
        self.image_array = np.zeros((100, 100, 3), dtype=np.uint8)
        self.image_array[25:75, 25:75] = [0, 255, 0]  # Carré vert au centre
        self.test_image = Image.fromarray(self.image_array)
        self.test_image_path = Path('test_image.png')
        self.test_image.save(self.test_image_path)
        
        # Créer un masque de test
        self.mask = np.zeros((100, 100), dtype=bool)
        self.mask[25:75, 25:75] = True  # Masque pour le carré central
    
    def tearDown(self):
        # Supprimer l'image de test
        self.test_image_path.unlink()
    
    def test_process_image_without_options(self):
        # Exécuter la fonction sans options
        result_image = process_image(self.test_image_path, self.mask)
        result_array = np.array(result_image)
        
        # Vérifier que les zones non végétales sont blanches
        self.assertTrue(np.array_equal(result_array[10, 10], [255, 255, 255]))
        # Vérifier que les zones végétales sont inchangées
        self.assertTrue(np.array_equal(result_array[50, 50], [0, 255, 0]))
    
    def test_process_image_with_fill_holes(self):
        # Ajouter un petit trou dans le masque
        self.mask[50, 50] = False
        filled_mask = fill_small_holes(self.mask, max_size_area=5)
        # Vérifier que le trou a été rempli
        self.assertTrue(filled_mask[50, 50])
    
    def test_process_image_with_pretty_result(self):
        # Exécuter la fonction avec l'option pretty_result
        result_image = process_image(self.test_image_path, self.mask, pretty_result=True)
        result_array = np.array(result_image)
        # Vérifier que les zones non végétales sont en niveaux de gris
        self.assertTrue(np.array_equal(result_array[10, 10], [0, 0, 0]))
        # Vérifier que les zones végétales sont inchangées
        self.assertTrue(np.array_equal(result_array[50, 50], [0, 255, 0]))
    
    def test_apply_white_background(self):
        result_array = apply_white_background(self.image_array, self.mask)
        # Vérifier que les zones non végétales sont blanches
        self.assertTrue(np.array_equal(result_array[10, 10], [255, 255, 255]))
    
    def test_apply_pretty_effect(self):
        result_array = apply_pretty_effect(self.image_array, self.mask)
        # Vérifier que les zones non végétales sont en niveaux de gris
        self.assertTrue(np.array_equal(result_array[10, 10], [0, 0, 0]))
    
if __name__ == '__main__':
    unittest.main()
