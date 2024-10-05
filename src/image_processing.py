import numpy as np
from pathlib import Path
from typing import Union
from PIL import Image, ImageFilter
import cv2

def process_image(
    image_path: Path,
    mask: np.ndarray,
    fill_holes: bool = False,
    pretty_result: bool = False,
    fill_holes_method: str = 'morphology',
) -> Image.Image:
    """
    Process the image based on the vegetation mask and apply additional transformations
    based on the FILL_HOLES and PRETTY_RESULT flags.

    Args:
        image_path (Path): Path to the original image file.
        mask (np.ndarray): Binary mask of detected vegetation.
        fill_holes (bool, optional): Whether to fill small holes in the vegetation mask. Defaults to False.
        pretty_result (bool, optional): Whether to apply a grayscale blur to non-vegetation areas. Defaults to False.
        fill_holes_method (str, optional): Method to fill small holes in the mask. Defaults to 'contour'. Options: 'morphology' or 'contour'.

    Returns:
        Image.Image: The processed image.
    """
    image = Image.open(image_path).convert('RGB')
    image_array = np.array(image)

    if fill_holes:
        if fill_holes_method == 'morphology':
            mask_uint8 = mask.astype(np.uint8)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            mask_uint8 = cv2.morphologyEx(mask_uint8, cv2.MORPH_CLOSE, kernel)
            mask = mask_uint8.astype(bool)
        elif fill_holes_method == 'contour':
            mask = fill_small_holes(mask, max_size_area=25)
        else:
            raise ValueError("fill_holes_method must be 'morphology' or 'contour'")

    if pretty_result:
        processed_image = apply_pretty_effect(image_array, mask)
    else:
        processed_image = apply_white_background(image_array, mask)

    return Image.fromarray(processed_image)

def fill_small_holes(mask: np.ndarray, max_size_area: int = 25) -> np.ndarray:
    """
    Fill small holes in the vegetation mask.

    Args:
        mask (np.ndarray): Binary mask of detected vegetation.
        max_size_area (int, optional): Maximum size area of holes to fill in pixels. Defaults to 25.

    Returns:
        np.ndarray: Updated mask with small holes filled.
    """
    # Convert the boolean mask to uint8
    mask_uint8 = mask.astype(np.uint8)

    # Find contours in the inverted mask (holes)
    contours, _ = cv2.findContours(
        1 - mask_uint8,
        cv2.RETR_CCOMP,
        cv2.CHAIN_APPROX_SIMPLE
    )
    for contour in contours:
        area = cv2.contourArea(contour)
        if area <= max_size_area:
            # Draw contours on the mask with the value 1 (foreground)
            cv2.drawContours(mask_uint8, [contour], -1, color=1, thickness=cv2.FILLED)
    # Convert the mask back to boolean
    mask_filled = mask_uint8.astype(bool)
    return mask_filled


def apply_white_background(image_array: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Apply a white background to non-vegetation areas of the image.

    Args:
        image_array (np.ndarray): Original image as a NumPy array.
        mask (np.ndarray): Binary mask of detected vegetation.

    Returns:
        np.ndarray: Image array with non-vegetation areas filled with white.
    """
    result = image_array.copy()
    result[~mask] = [255, 255, 255]
    return result

def apply_pretty_effect(image_array: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Apply a grayscale blur to non-vegetation areas of the image.

    Args:
        image_array (np.ndarray): Original image as a NumPy array.
        mask (np.ndarray): Binary mask of detected vegetation.

    Returns:
        np.ndarray: Image array with non-vegetation areas blurred and in grayscale.
    """
    gray_image = Image.fromarray(image_array).convert('L')
    blurred_image = gray_image.filter(ImageFilter.GaussianBlur(radius=5))
    blurred_array = np.array(blurred_image)
    result = image_array.copy()
    result[~mask] = np.stack([blurred_array]*3, axis=-1)[~mask]
    return result
