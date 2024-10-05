import numpy as np
from pathlib import Path
import cv2

def detect_vegetation(
    image_path: Path, 
    normalize_illumination: bool = True, 
    use_lab_color_space: bool = True
) -> np.ndarray:
    """
    Detect green vegetation in the input image using HSV or LAB color space, with optional image processing techniques.

    Args:
        image_path (Path): Path to the image file to process.
        normalize_illumination (bool): Apply histogram equalization to normalize illumination (default: False).
        use_lab_color_space (bool): Use LAB color space instead of HSV for vegetation detection (default: False).

    Returns:
        np.ndarray: A binary mask where pixels corresponding to vegetation are True.
    """
    # Load the image
    image = cv2.imread(str(image_path))

    # Optional: Use LAB color space
    if use_lab_color_space:
        # Convert to LAB and normalize the L channel
        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab_image)
        l_equalized = cv2.equalizeHist(l)
        normalized_image = cv2.merge((l_equalized, a, b))

        # Convert back to BGR and then to HSV for segmentation
        hsv_image = cv2.cvtColor(normalized_image, cv2.COLOR_LAB2BGR)
        hsv_image = cv2.cvtColor(hsv_image, cv2.COLOR_BGR2HSV)
    else:
        # Convert to HSV color space directly
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Optional: Normalize illumination (equalize the V channel in HSV)
    if normalize_illumination:
        h, s, v = cv2.split(hsv_image)
        v_equalized = cv2.equalizeHist(v)
        hsv_image = cv2.merge((h, s, v_equalized))

    # Define the green color range in HSV
    lower_green = np.array([35, 25, 25])
    upper_green = np.array([85, 255, 255])

    # Create a mask for green colors
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Convert mask to a boolean array
    vegetation_mask = mask.astype(bool)

    return vegetation_mask
