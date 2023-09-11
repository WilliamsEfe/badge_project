import pytest
from PIL import Image, ImageDraw
from src.verifier import BadgeVerifier
from src.converter import BadgeConverter, ImageLoadError
import os
import numpy as np

@pytest.fixture
def mock_image():
    img_path = create_mock_image()
    yield img_path
    os.remove(img_path)

@pytest.fixture
def mock_circle_image():
    img_path = create_mock_circle_image()
    yield img_path
    os.remove(img_path)

def create_mock_image(size=(512, 512), color=(255, 255, 255, 255), format="PNG"):
    img = Image.new("RGBA", size, color)
    img_path = "tests/mock_image.png"
    img.save(img_path, format=format)
    return img_path

def create_mock_circle_image(radius=256, bgcolor=(0, 0, 0, 0), circlecolor=(255, 154, 85)):
    img = Image.new("RGBA", (512, 512), bgcolor)
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, 2*radius, 2*radius), fill=circlecolor, outline=bgcolor)
    
    img_array = np.array(img)
    x, y = np.ogrid[:512, :512]
    mask_circle = (x - 256)**2 + (y - 256)**2 <= 256**2
    img_array[~mask_circle, 3] = 0
    img_array[mask_circle, 3] = 255
    img = Image.fromarray(img_array)

    img_path = "tests/mock_circle_image.png"
    img.save(img_path)
    return img_path

def test_badge_verifier_with_wrong_size(mock_image):
    verifier = BadgeVerifier(mock_image)
    result, message = verifier.verify()
    assert not result, f"Expected verification to fail due to size, but got: {message}"

def test_badge_verifier_with_correct_size_but_outside_pixels(mock_image):
    verifier = BadgeVerifier(mock_image)
    result, message = verifier.verify()
    assert not result, f"Expected verification to fail due to transparency, but got: {message}"

def test_badge_verifier_with_correct_badge(mock_circle_image):
    verifier = BadgeVerifier(mock_circle_image)
    result, message = verifier.verify()
    
    if not result:
        img = Image.open(mock_circle_image)
        # ... [rest of the code to print problematic pixels] ...
        assert False, f"Expected successful verification, but got: {message}"

def test_badge_converter_success(mock_image):
    converter = BadgeConverter(mock_image, "tests/output/")
    message = converter.convert()
    assert message == "Image converted successfully!", f"Expected successful conversion, but got: {message}"

def test_badge_converter_image_load_error():
    with pytest.raises(ImageLoadError):
        converter = BadgeConverter("nonexistent_image.png", "tests/output/")

