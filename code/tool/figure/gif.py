import numpy as np
import imageio

def convert_3d_to_2d(image_3d):
    """
    Converts a 3D image to a 2D image by selecting the middle slice.
    """
    middle_slice = image_3d[:, :, image_3d.shape[2] // 2]
    return middle_slice

def create_gif(image_paths, output_path, duration=0.1):
    """
    Creates a GIF from a list of image paths.

    Args:
        image_paths: A list of paths to PNG or other image files.
        output_path: The path to save the generated GIF.
        duration: The duration of each frame in seconds (default: 0.1 seconds).
    """
    images = []
    for image_path in image_paths:
        try:
            image_3d = imageio.v2.imread(image_path)  # Use v2 for better compatibility
            if image_3d.ndim == 3 and image_3d.shape[2] == 4:  # Check if the image is 3D
                image = convert_3d_to_2d(image_3d)
            else:
                image = image_3d  # Assume the image is already 2D
            images.append(image)
        except FileNotFoundError:
            print(f"Error: Image file not found: {image_path}")
            return  # Stop if an image is missing
        except Exception as e:  # Catch other potential image reading errors
            print(f"Error reading image {image_path}: {e}")
            return

    if not images:  # Check if any images were successfully loaded
        print("No valid images found. Cannot create GIF.")
        return

    try:
        imageio.mimsave(output_path, images, duration=duration, loop=0)  # loop=0 for infinite loop
        print(f"GIF created successfully at: {output_path}")
    except Exception as e:
        print(f"Error creating GIF: {e}")

# Example usage:
image_files = [f"code/tool/figure/case_100_{_}.png" for _ in range(17)]
output_gif = "code/tool/figure/animated.gif"
frame_duration = 0.4  # 200 milliseconds per frame

create_gif(image_files, output_gif, frame_duration)
