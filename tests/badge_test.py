import pytest
from PIL import Image, ImageDraw
from src.verifier import BadgeVerifier
from src.converter import BadgeConverter
import os
import numpy as np

def create_mock_image(size=(512, 512), color=(255, 255, 255, 255), format="PNG"):
    img = Image.new("RGBA", size, color)
    img_path = "tests/mock_image.png"
    img.save(img_path, format=format)
    return img_path

def create_mock_circle_image(radius=256, bgcolor=(0, 0, 0, 0), circlecolor=(255, 255, 255, 255)):  # Using white for the circle
    img = Image.new("RGBA", (512, 512), bgcolor)
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, 2*radius, 2*radius), fill=circlecolor, outline=bgcolor)
    
    # Ensure pixels inside the circle are fully opaque
    img_array = np.array(img)
    x, y = np.ogrid[:512, :512]
    mask_circle = (x - 256)**2 + (y - 256)**2 <= 256**2
    img_array[mask_circle, 3] = 255
    img = Image.fromarray(img_array)

    img_path = "tests/mock_circle_image.png"
    img.save(img_path)
    return img_path


def test_badge_verifier_with_wrong_size():
    mock_img_path = create_mock_image(size=(500, 500))
    verifier = BadgeVerifier(mock_img_path)
    result, message = verifier.verify()
    assert not result
    assert message == "Image size is not 512x512"
    os.remove(mock_img_path)

def test_badge_verifier_with_correct_size_but_outside_pixels():
    mock_img_path = create_mock_image(size=(512, 512), color=(255, 255, 255, 255))
    verifier = BadgeVerifier(mock_img_path)
    result, message = verifier.verify()
    assert not result
    assert message == "Invalid pixel transparency within or outside the circle"
    os.remove(mock_img_path)

def test_badge_verifier_with_correct_badge():
    mock_img_path = create_mock_circle_image()
    verifier = BadgeVerifier(mock_img_path)
    result, message = verifier.verify()
    print(message)  # Print out the message for debugging
    assert result
    assert message == "Image verified successfully"
    os.remove(mock_img_path)

def test_badge_converter():
    mock_img_path = create_mock_image(size=(500, 500))
    converter = BadgeConverter(mock_img_path, "tests/output/")
    message = converter.convert()
    assert message == "Image converted successfully!"
    os.remove(mock_img_path)
