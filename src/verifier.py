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

    # def check_happy_colors(self):
    #     # Convert image to RGB (ignore alpha channel)
    #     rgb_img = self.img.convert('RGB')
    #     data = np.array(rgb_img)
        
    #     # Calculate brightness
    #     r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    #     brightness = (r + g + b) / 3
        
    #     # Check average brightness
    #     if brightness.mean() < 80:  # Slightly reduced threshold
    #         return False
        
    #     # Convert RGB to HSV and check saturation
    #     hsv_img = self.img.convert('HSV')
    #     h, s, v = hsv_img.split()
    #     if np.array(s).mean() < 100:  # Reduced saturation threshold
    #         return False
            
    #     return True

    def check_happy_colors(self):
        # Convert the image to RGBA if not already in that mode
        img = self.img.convert("RGBA")

        # Compute brightness and saturation considering only the pixels inside the circle
        average_brightness, average_saturation = self.compute_circle_brightness_and_saturation(img)

        # Check average brightness
        if average_brightness < 80:  # Slightly reduced threshold
            return False, "The colors in the badge don't give a 'happy' feeling"

        # Check average saturation
        if average_saturation < 100:  # Reduced saturation threshold
            return False, "The colors in the badge don't give a 'happy' feeling"

        return True, "Image verified successfully"

    def compute_circle_brightness_and_saturation(self, img, radius=256):
        # Convert image to RGB (ignore alpha channel)
        rgb_img = img.convert('RGB')
        data = np.array(rgb_img)

        # Create a mask for pixels inside the circle
        x, y = np.ogrid[:512, :512]
        mask_circle = (x - 256)**2 + (y - 256)**2 <= radius**2

        # Extract only the pixels inside the circle
        circle_data = data[mask_circle]

        # Calculate brightness for the circle pixels
        r, g, b = circle_data[:, 0], circle_data[:, 1], circle_data[:, 2]
        brightness = (r + g + b) / 3

        # Convert RGB to HSV and check saturation for the circle pixels
        hsv_img = img.convert('HSV')
        h, s, v = hsv_img.split()
        s_data = np.array(s)[mask_circle]

        average_brightness = brightness.mean()
        average_saturation = s_data.mean()

        return average_brightness, average_saturation



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
