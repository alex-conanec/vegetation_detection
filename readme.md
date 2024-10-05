# Vegetation Detection in RGB Images

This project involves writing a Python script to detect green vegetation in RGB images. The script processes a list of image URLs, detects vegetation, and outputs the results with optional image processing features.

## Table of Contents

- [Exercise Description](#exercise-description)
- [Usage](#usage)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Command-Line Interface](#command-line-interface)
- [Testing](#testing)
- [Vegetation Detection Approach](#vegetation-detection-approach)

---

## Exercise Description

**Detection of vegetation in RGB images.**

Write a Python script satisfying the following requirements:

**Arguments:**

- A list of image URLs  
  In this exercise, consider these 3 image URLs:
  - `https://picsum.photos/id/1058/400/400.jpg`
  - `https://picsum.photos/id/1025/400/400.jpg`
  - `https://picsum.photos/id/1040/400/400.jpg`
- A path to an output directory
- A first flag (default: False), referred to as `FILL_HOLES` in the following
- A second flag (default: False), referred to as `PRETTY_RESULT` in the following

**Description:** For each image URL of the input list:

- Download the image
- Save the image (PNG format) in the output directory
- Roughly detect the green vegetation
- If `FILL_HOLES` flag is enabled, also consider as vegetation the small holes in the detected vegetation (for instance, holes < 5x5 pixels)
- Build the result image as follows:
  - For vegetation areas, consider the pixel values of the input image
  - For other areas:
    - Fill in white if `PRETTY_RESULT` flag is disabled
    - Otherwise, fill with a grayscale and blurred version of the input image
  - The output should be an RGB image the same size as the input image.
- Save the result image (PNG format) in the output directory

**Note:** Do not aim for a perfect and universal detection of the vegetation; we are simply interested in your ability to work with images.

**Feel free to use any Python packages you may need.**

---

## Usage

### Prerequisites

Ensure you have Python 3.7 or later installed on your system.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/vegetation-detection.git
   cd vegetation-detection

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required dependencies:**   
    ```bash
    pip install -r requirements.txt

## Command-Line Interface
The script can be executed via the command line using main.py. Below is the usage information.

**Basic Command:**

```bash
    python main.py -o OUTPUT_DIR IMAGE_URLS [OPTIONS]
```

**Arguments:**

* `-o, --output-dir`: Path to the output directory (required).

* `IMAGE_URLS`: One or more image URLs to process.

**Options:**

* `--fill-holes`: Enable filling small holes in the detected vegetation (default: False).

* `--pretty-result`: Apply a grayscale blur to non-vegetation areas (default: False).

***Example:**

```bash
    python main.py -o output_directory \
        https://picsum.photos/id/1058/400/400.jpg \
        https://picsum.photos/id/1025/400/400.jpg \
        https://picsum.photos/id/1040/400/400.jpg \
        --fill-holes --pretty-result
```

This command will:

* Download the specified images.
* Detect green vegetation, filling small holes.
* Apply a grayscale blur to non-vegetation areas.
* Save the original and processed images in the output_directory.

## Testing
To run the unit tests for the project, use the following commands:

**1. Install test dependencies (if any are specified separately):**

```bash
    pip install -r test_requirements.txt
```

**2. Run tests using pytest:**

```bash
    pytest tests/
```

This will execute all tests located in the tests/ directory.

## Vegetation Detection Approach

The detection of green vegetation is performed by converting the RGB image to the HSV color space and applying a color threshold.

**Methodology:**

1. **Color Space Conversion and Illumination Normalization:**

   - **LAB Color Space:**
     - The image is converted from RGB to LAB color space.
     - LAB color space separates luminance (L channel) from color information (A and B channels), making it effective for handling illumination variations.
     - Histogram equalization is applied to the L channel to normalize lighting across the image, reducing the impact of shadows and highlights.

   - **Conversion to HSV Color Space:**
     - The normalized LAB image is converted back to RGB and then to HSV color space.
     - HSV color space is suitable for color-based segmentation because it separates hue from saturation and value (brightness).

2. **Thresholding and Mask Creation:**

   - **HSV Thresholding:**
     - A range of HSV values corresponding to green vegetation is defined.
     - **Lower Green Range:** `[35, 25, 25]`
     - **Upper Green Range:** `[85, 255, 255]`
     - A binary mask is created where pixels within this range are marked as vegetation.

3. **Optional Image Processing Techniques:**

   - **Illumination Normalization in HSV Space:**
     - Histogram equalization is optionally applied to the V (Value) channel of the HSV image.
     - This step further reduces the effects of uneven lighting and shadows.

   - **Filling Small Holes in the Vegetation Mask:**
     - **Morphological Operations:**
       - Morphological closing is applied using an elliptical structuring element.
       - This fills small holes and gaps in the vegetation mask, improving continuity.
     - **Contour-Based Filling:**
       - Alternatively, contours of small holes are detected.
       - Holes with an area smaller than a defined threshold are filled.
       - This method provides precise control over which holes to fill.





