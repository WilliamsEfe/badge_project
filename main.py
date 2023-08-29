from src.verifier import BadgeVerifier
from src.converter import BadgeConverter
import os

class BadgeProcessor:

    def __init__(self):
        self.input_image_name = ""
        self.input_image_path = ""
        self.output_dir = os.path.join("images", "output")

    def user_interface(self):
        print("\nWelcome to the Badge Verifier and Converter!")
        self.input_image_name = input("Enter the name or path of the image you want to process (e.g., my_image.png): ")
        self.input_image_path = os.path.join("images", "input", self.input_image_name)

    def verify_image_exists(self):
        return os.path.exists(self.input_image_path)

    def process_image(self):
        verifier = BadgeVerifier(self.input_image_path)
        result, message = verifier.verify()
        print(message)
        
        if not result:
            converter = BadgeConverter(self.input_image_path, self.output_dir)
            convert_message = converter.convert()
            print(convert_message)

    def run(self):
        while True:
            self.user_interface()

            if self.verify_image_exists():
                self.process_image()
            else:
                print(f"Error: The image '{self.input_image_name}' does not exist in the 'images/input/' directory.")
            
            user_choice = input("\nDo you want to process another image? (yes/no): ").strip().lower()
            if user_choice != "yes":
                break

if __name__ == "__main__":
    processor = BadgeProcessor()
    processor.run()
