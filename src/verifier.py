# from PIL import Image, UnidentifiedImageError
# import numpy as np

# class BadgeVerifier:

#     def __init__(self, img_path):
#         self.img_path = img_path
#         self.img, self.error_message = self.load_image()

#     def load_image(self):
#         try:
#             img = Image.open(self.img_path)
#             return img, ""
#         except FileNotFoundError:
#             return None, "Error: The specified image file was not found."
#         except UnidentifiedImageError:
#             return None, "Error: The image format is unsupported or the file is corrupted."

#     def check_format(self):
#         return self.img.format == 'PNG'

#     # def verify_size(self):
#     #     return self.img.size == (512, 512)
        
#     # def verify_pixel_transparency(self):
#     #     width, height = self.img.size
#     #     img_array = np.array(self.img)

#     #     x, y = np.ogrid[:width, :height]
#     #     mask_circle = (x - 256)**2 + (y - 256)**2 <= 256**2
        
#     #     # Check pixels outside circle
#     #     if img_array[~mask_circle, 3].any():
#     #         return False
        
#     #     # Check pixels inside circle
#     #     if not img_array[mask_circle, 3].all():
#     #         return False

#     #     return True

#     def verify_pixel_transparency(self):
#         width, height = self.img.size
#         img_array = np.array(self.img)

#         x, y = np.ogrid[:width, :height]
#         mask_circle = (x - 256)**2 + (y - 256)**2 <= 256**2

#         # Check pixels outside circle
#         outside_circle = img_array[~mask_circle]
#         if outside_circle[:, 3].any():  # If any non-transparent pixel outside circle
#             problematic_pixels = np.argwhere((~mask_circle) & (img_array[:, :, 3] > 0))
#             print("Problematic Pixels Outside Circle:", problematic_pixels)
#             return False

#         # Check pixels inside circle
#         inside_circle = img_array[mask_circle]
#         if not inside_circle[:, 3].all():  # If any transparent pixel inside circle
#             problematic_pixels = np.argwhere(mask_circle & (img_array[:, :, 3] == 0))
#             print("Problematic Pixels Inside Circle:", problematic_pixels)
#             return False

#         return True


#     def check_happy_colors(self):
#         avg_color = np.mean(self.img)
#         return avg_color >= 128

#     def verify(self):
#         if not self.img:
#             return False, self.error_message
        
#         if not self.check_format():
#             return False, "Error: The image is not in PNG format."

#         if not self.verify_size():
#             return False, "Image size is not 512x512"
        
#         if not self.verify_pixel_transparency():
#             return False, "Invalid pixel transparency within or outside the circle"
        
#         if not self.check_happy_colors():
#             return False, "The colors in the badge don't give a 'happy' feeling"
        
#         return True, "Image verified successfully"

from PIL import Image, UnidentifiedImageError
import numpy as np

class BadgeVerifier:

    def __init__(self, img_path):
        self.img_path = img_path
        self.img, self.error_message = self.load_image()

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
        return self.img.size == (512, 512)
        
    def verify_pixel_transparency(self):
        width, height = self.img.size
        img_array = np.array(self.img)

        x, y = np.ogrid[:width, :height]
        mask_circle = (x - 256)**2 + (y - 256)**2 <= 256**2

        # Check pixels outside circle
        outside_circle = img_array[~mask_circle]
        if outside_circle[:, 3].any():  # If any non-transparent pixel outside circle
            problematic_pixels = np.argwhere((~mask_circle) & (img_array[:, :, 3] > 0))
            print("Problematic Pixels Outside Circle:", problematic_pixels)
            return False

        # Check pixels inside circle
        inside_circle = img_array[mask_circle]
        if not inside_circle[:, 3].all():  # If any transparent pixel inside circle
            problematic_pixels = np.argwhere(mask_circle & (img_array[:, :, 3] == 0))
            print("Problematic Pixels Inside Circle:", problematic_pixels)
            return False

        return True

    def check_happy_colors(self):
        avg_color = np.mean(self.img)
        return avg_color >= 128

    def verify(self):
        if not self.img:
            return False, self.error_message
        
        if not self.check_format():
            return False, "Error: The image is not in PNG format."

        if not self.verify_size():
            return False, "Image size is not 512x512"
        
        if not self.verify_pixel_transparency():
            return False, "Invalid pixel transparency within or outside the circle"
        
        if not self.check_happy_colors():
            return False, "The colors in the badge don't give a 'happy' feeling"
        
        return True, "Image verified successfully"
