from src.verifier import BadgeVerifier
from src.converter import BadgeConverter
import os

INPUT_DIR = os.path.join("images", "input")
OUTPUT_DIR = os.path.join("images", "output")
WELCOME_MESSAGE = "\nWelcome to the Badge Verifier and Converter!"
ERROR_IMAGE_NOT_FOUND = "Error: The image '{}' does not exist in the 'images/input/' directory."

class BadgeProcessor:

    def __init__(self):
        self.input_image_name = ""
        self.input_image_path = ""
        self.output_dir = OUTPUT_DIR

    def user_interface(self):
        print(WELCOME_MESSAGE)
        self.input_image_name = input("Enter the name or path of the image you want to process (e.g., my_image.png): ")
        self.input_image_path = os.path.join(INPUT_DIR, self.input_image_name)

    def verify_image_exists(self):
        return os.path.exists(self.input_image_path)

    def verify_image(self):
        verifier = BadgeVerifier(self.input_image_path)
        return verifier.verify()

    def convert_image(self):
        converter = BadgeConverter(self.input_image_path, self.output_dir)
        return converter.convert()

    def process_image(self):
        result, message = self.verify_image()
        print(message)
        
        if not result:
            convert_message = self.convert_image()
            print(convert_message)
            print(f"Converted image saved to: {self.output_dir}")

    def run(self):
        while True:
            self.user_interface()

            if self.verify_image_exists():
                self.process_image()
            else:
                print(ERROR_IMAGE_NOT_FOUND.format(self.input_image_name))
            
            user_choice = input("\nDo you want to process another image? (yes/no): ").strip().lower()
            if user_choice != "yes":
                break

if __name__ == "__main__":
    processor = BadgeProcessor()
    processor.run()
