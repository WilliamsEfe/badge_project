
# Badge Project

The Badge Project aims to allow users to upload an avatar, which should be an image within a circle, meeting certain criteria.

## Project Features

1.  **Badge Verification**:
    
    -   Accepts PNG images.
    -   Verifies if the image size is 512x512 pixels.
    -   Ensures that the only non-transparent pixels are within a circle.
    -   Checks if the colors in the badge give a "happy" feeling.
2.  **Badge Conversion**:
    
    -   Converts images of any format into the specified PNG format.
    -   If the image does not meet the verification criteria, an attempt is made to convert it.

## Project Architecture

-   **Main Application (`main.py`)**:
    
    -   Provides an interactive interface to process images.
    -   Uses the `BadgeProcessor` class to handle user inputs and image processing tasks.
-   **Source Code (`src/` directory)**:
    
    -   **Verifier (`verifier.py`)**:
        -   Contains the `BadgeVerifier` class which checks images against the specified criteria.
    -   **Converter (`converter.py`)**:
        -   Contains the `BadgeConverter` class which converts images to meet the criteria if they don't initially.
-   **Images (`images/` directory)**:
    
    -   **Input (`input/`)**: Place images here to be processed.
    -   **Output (`output/`)**: Processed and/or converted images are saved here.
-   **Tests (`tests/` directory)**: The `tests/` directory contains unit tests that validate the functionality of the `BadgeVerifier` and `BadgeConverter` classes. These tests make use of mock images to ensure that the verifier and converter are working as expected.

1.  **`test_badge_verifier_with_wrong_size`**: Validates that the verifier correctly identifies images of the incorrect size.
2.  **`test_badge_verifier_with_correct_size_but_outside_pixels`**: Validates that the verifier identifies images with pixels outside the designated circle area.
3.  **`test_badge_verifier_with_correct_badge`**: Ensures that the verifier correctly identifies and approves valid circle images.
4.  **`test_badge_converter`**: Validates the converter's ability to adjust images to meet the desired specifications.

	Utility functions, such as `create_mock_image` and `create_mock_circle_image`, are included to facilitate the creation of mock images for testing.

	To run these tests, navigate to the project directory and use the pytest framework:

	`pytest`
	    
-   **Docker (`Dockerfile`)**:
    
    -   Provides a containerized environment for the project.
    -   Uses the official Python 3.9 slim image as a base.
    -   Copies and installs necessary dependencies from `requirements.txt`.
    -   Sets up the necessary directories and files within the container.
    -   The container runs `main.py` on startup and remains running indefinitely due to the infinite loop at the end of the script.

## Requirements

1.  Python 3.9
2.  Pillow library (and other dependencies specified in `requirements.txt`)

## Usage

1.  Ensure you have the required dependencies installed:
    
    `pip install -r requirements.txt` 
    
2.  Run the `main.py` script:
    
    `python main.py` 
    
3.  Follow the interactive prompts to specify the image you wish to process, which is previously saved in the `images/input` directory.

4. The converted image is saved in the `images/output`
    

## Docker Usage

To build and run the application inside a Docker container:

1.  Build the Docker image:
  
    `docker build -t badge_project:latest .` 
    
2.  Run the Docker container in interactive mode:
    
    `docker run -it badge_project:latest`
