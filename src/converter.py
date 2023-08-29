from PIL import Image, UnidentifiedImageError
import numpy as np
import os
import time

class BadgeConverter:

    def __init__(self, input_path, output_dir):
        self.input_path = input_path
        self.output_dir = output_dir
        self.img, self.error_message = self.load_image_for_conversion()

    def load_image_for_conversion(self):
        try:
            img = Image.open(self.input_path)
            return img, ""
        except FileNotFoundError:
            return None, "Error: The specified image file was not found."
        except UnidentifiedImageError:
            return None, "Error: The image format is unsupported or the file is corrupted."

    def convert_to_png_if_needed(self):
        if self.img.format != 'PNG':
            return self.img.convert('RGBA')
        return self.img

    def resize_image(self):
        return self.img.resize((512, 512))

    def make_pixels_transparent(self):
        img_array = np.array(self.img)
        width, height = self.img.size

        x, y = np.ogrid[:width, :height]
        mask_circle = (x - 256)**2 + (y - 256)**2 > 256**2

        img_array[mask_circle, 3] = 0  # Set alpha to 0 (transparent) for pixels outside circle
        self.img = Image.fromarray(img_array)
        return self.img

    def generate_output_path(self):
        base_name = os.path.basename(self.input_path)
        name_without_extension = os.path.splitext(base_name)[0]
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        new_filename = f"{name_without_extension}_converted_{timestamp}.png"
        return os.path.join(self.output_dir, new_filename)

    def convert(self):
        if not self.img:
            return self.error_message

        self.img = self.convert_to_png_if_needed()
        self.img = self.resize_image()
        self.img = self.make_pixels_transparent()
        output_path = self.generate_output_path()

        try:
            self.img.save(output_path, "PNG")
            return "Image converted successfully!"
        except Exception as e:
            return f"Error: Could not save the image. {str(e)}"