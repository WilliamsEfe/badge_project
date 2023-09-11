from PIL import Image, UnidentifiedImageError
import numpy as np
import os
import time

IMAGE_SIZE = (512, 512)
CIRCLE_RADIUS = 256
CIRCLE_CENTER = (256, 256)

class ImageLoadError(Exception):
    pass

class BadgeConverter:

    def __init__(self, input_path, output_dir):
        self.input_path = input_path
        self.output_dir = output_dir
        self.img = self.load_image_for_conversion()

    def load_image_for_conversion(self):
        try:
            return Image.open(self.input_path)
        except FileNotFoundError:
            raise ImageLoadError("Error: The specified image file was not found.")
        except UnidentifiedImageError:
            raise ImageLoadError("Error: The image format is unsupported or the file is corrupted.")

    def convert_to_png_if_needed(self):
        if self.img.format != 'PNG':
            self.img = self.img.convert('RGBA')

    def resize_image(self):
        self.img = self.img.resize(IMAGE_SIZE)

    def make_pixels_transparent(self):
        img_array = np.array(self.img)
        x, y = np.ogrid[:IMAGE_SIZE[0], :IMAGE_SIZE[1]]
        mask_circle = (x - CIRCLE_CENTER[0])**2 + (y - CIRCLE_CENTER[1])**2 > CIRCLE_RADIUS**2
        img_array[mask_circle, 3] = 0  # Set alpha to 0 (transparent) for pixels outside circle
        self.img = Image.fromarray(img_array)

    def generate_output_path(self):
        base_name = os.path.basename(self.input_path)
        name_without_extension = os.path.splitext(base_name)[0]
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        new_filename = f"{name_without_extension}_converted_{timestamp}.png"
        return os.path.join(self.output_dir, new_filename)

    def apply_happy_color_transformations(self):
        """Apply transformations to give the image a 'happy' color scheme."""
        img_array = np.array(self.img)
        happy_colors = {
            (255, 154, 85),
            (255, 234, 108),
            (84, 255, 251),
            (231, 178, 255),
            (137, 255, 204)
        }
        
        for color in happy_colors:
            mask = np.all(img_array[:, :, :3] == color, axis=2)
            img_array[mask] = [*color, 255]
        
        self.img = Image.fromarray(img_array)

    def convert(self):
        if not self.img:
            return "No image loaded."

        self.convert_to_png_if_needed()
        self.resize_image()
        self.make_pixels_transparent()
        self.apply_happy_color_transformations()

        output_path = self.generate_output_path()
        try:
            self.img.save(output_path, "PNG")
            return "Image converted successfully!"
        except Exception as e:
            raise Exception(f"Error: Could not save the image. {str(e)}")

