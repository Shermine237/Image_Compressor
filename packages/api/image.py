from os import path, makedirs

from PIL import Image


class CustomImage:
    def __init__(self, input_image, output_folder):
        self.image = Image.open(input_image)
        self.width_size, self.height_size = self.image.size
        self.image_name = path.basename(input_image)
        self.source_location = path.dirname(input_image)
        self.output_location = path.join(self.source_location, output_folder)
        self.output_image = path.join(self.output_location, f"c_{self.image_name}")

    def compress(self, reduction=0.5, new_quality=75):
        new_width = round(self.width_size * reduction)  # round to round float number
        new_height = round(self.height_size * reduction)
        new_image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Save
        if not path.exists(self.output_location):   # If path don't exist: create it
            makedirs(self.output_location)
        new_image.save(self.output_image, quality=new_quality)
        return path.exists(self.output_image)
