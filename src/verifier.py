from PIL import Image, UnidentifiedImageError
import numpy as np

IMAGE_SIZE = (512, 512)
CIRCLE_RADIUS = 256
CIRCLE_CENTER = (256, 256)

class BadgeVerifier:

    def __init__(self, img_path):
        self.img_path = img_path
        self.img, self.error_message = self.load_image()
        self.happy_colors_set = {
            (255, 154, 85),
            (255, 234, 108),
            (84, 255, 251),
            (231, 178, 255),
            (137, 255, 204)
        }

    def load_image(self):
        try:
            img = Image.open(self.img_path)
            return img, ""
        except FileNotFoundError:
            return None, "Error: The specified image file was not found."
        except UnidentifiedImageError:
            return None, "Error: The image format is unsupported or the file is corrupted."

    def check_format(self):
        return self.img.format == 'PNG'

    def verify_size(self):
        return self.img.size == IMAGE_SIZE

    def verify_pixel_transparency(self):
        width, height = self.img.size
        img_array = np.array(self.img)

        x, y = np.ogrid[:width, :height]
        mask_circle = (x - CIRCLE_CENTER[0])**2 + (y - CIRCLE_CENTER[1])**2 <= CIRCLE_RADIUS**2

        if mask_circle.shape != img_array.shape[:2]:
            return False

        if img_array.shape[2] == 4:
            outside_circle = img_array[~mask_circle]
            if outside_circle.shape[0] > 0 and outside_circle[:, 3].any():
                problematic_pixels_outside = np.argwhere((~mask_circle) & (img_array[:, :, 3] > 0))
                print("Problematic Pixels Outside Circle:", problematic_pixels_outside)
                print("Their RGBA values:", img_array[problematic_pixels_outside[:, 0], problematic_pixels_outside[:, 1]])
                return False

            inside_circle = img_array[mask_circle]
            if inside_circle.shape[0] > 0 and not inside_circle[:, 3].all():
                problematic_pixels_inside = np.argwhere(mask_circle & (img_array[:, :, 3] == 0))
                print("Problematic Pixels Inside Circle:", problematic_pixels_inside)
                print("Their RGBA values:", img_array[problematic_pixels_inside[:, 0], problematic_pixels_inside[:, 1]])
                return False
        else:
            return False

        return True

    def has_happy_colors(self):
        img_rgb = self.img.convert('RGB')
        pixels_set = set(img_rgb.getdata())
        return bool(self.happy_colors_set.intersection(pixels_set))

    def check_happy_colors(self):
        if not self.has_happy_colors():
            return False, "The image doesn't contain any of the happy colors."
        return True, "Image verified successfully"

    def verify(self):
        errors = []

        if not self.img:
            errors.append(self.error_message)

        if not self.check_format():
            errors.append("Error: The image is not in PNG format.")

        if not self.verify_size():
            errors.append("Error: Image size is not 512x512.")

        if not self.verify_pixel_transparency():
            errors.append("Error: Invalid pixel transparency within or outside the circle.")

        verified, message = self.check_happy_colors()
        if not verified:
            errors.append(message)

        if errors:
            error_message = "\n".join(errors)
            return False, error_message

        return True, "Image verified successfully"
