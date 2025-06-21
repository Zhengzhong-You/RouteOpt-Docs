from PIL import Image


def crop_top_bottom(image_path, output_path, pixels_to_crop):
    """
    Removes a specified number of pixels from the top and bottom of an image.

    Parameters:
    - image_path: str, path to the input image.
    - output_path: str, path to save the cropped image.
    - pixels_to_crop: int, number of pixels to remove from both the top and bottom.

    Returns:
    - None
    """
    with Image.open(image_path) as img:
        img_width, img_height = img.size

        # Ensure the cropping does not exceed image dimensions
        if 2 * pixels_to_crop >= img_height:
            raise ValueError("The total pixels to crop exceed the image's height.")

        # Calculate coordinates to crop the specified pixels from top and bottom
        left = 0
        top = pixels_to_crop
        right = img_width
        bottom = img_height - pixels_to_crop

        # Crop the image
        cropped_img = img.crop((left, top, right, bottom))

        # Save the cropped image
        cropped_img.save(output_path)
        print(f"Cropped image saved to {output_path}")


# Example usage
input_image_path = 'RouteOpt_logo_left_right.png'
output_image_path = 'RouteOpt_logo_left_right_2.png'
pixels_to_crop = 1200  # Number of pixels to remove from both the top and bottom

crop_top_bottom(input_image_path, output_image_path, pixels_to_crop)
