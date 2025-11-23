"""
File: stanCodoshop.py
Name: 
----------------------------------------------
SC101_Assignment3 Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.
"""

import os
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue): #### m1
    """
    Returns a value that refers to the "color distance" between a pixel and a mean RGB value.

    Input:
        pixel (Pixel): the pixel with RGB values to be compared
        red (int): the average red value of the pixels to be compared
        green (int): the average green value of the pixels to be compared
        blue (int): the average blue value of the pixels to be compared

    Returns:
        dist (float): the "color distance" of a pixel to the average RGB value of the pixels to be compared.
    """
    return ((red - pixel.red)**2 + (green - pixel.green)**2 + (blue - pixel.blue)**2) ** 0.5


def get_average(pixels): #### m2
    """
    Given a list of pixels, finds their average red, blue, and green values.

    Input:
        pixels (List[Pixel]): a list of pixels to be averaged

    Returns:
        rgb (List[int]): a list of average red, green, and blue values of the pixels
                        (returns in order: [red, green, blue])
    """
    # Initialize the RGB components for the TTL color before using it.
    ttl_r = 0
    ttl_g = 0
    ttl_b = 0

    # Sum the pixel values from all images at this position.
    for pixel in pixels:
        ttl_r += pixel.red
        ttl_g += pixel.green
        ttl_b += pixel.blue

    # total photo cnts
    n = len(pixels)
    # avg RGB
    return [ttl_r//n, ttl_g//n, ttl_b//n]

    # # You can shorten this into a one-liner, but it will loop the data three times,
    # # making the runtime 3N instead of N.
    # return [sum(pixel.red for pixel in pixels) // len(pixels), sum(pixel.green for pixel in pixels) // len(pixels),
    #         sum(pixel.blue for pixel in pixels) // len(pixels)]




def get_best_pixel(pixels): #### m3
    """
    Given a list of pixels, returns the pixel with the smallest "color distance", which has the closest color to the average.

    Input:
        pixels (List[Pixel]): a list of pixels to be compared
    Returns:
        best (Pixel): the pixel which has the closest color to the average
    """
    avg_rgb = get_average(pixels)
    # Initialize min_dist to infinity.
    min_dist = float('inf')
    best_pixel = None

    for pixel in pixels:
        dist = get_pixel_dist(pixel, avg_rgb[0], avg_rgb[1], avg_rgb[2])
        # We can rewrite this without using the avg_rgb variable.
        # >> dist = get_pixel_dist(pixel, *get_average(pixels)) # * >> 把list打開，依序丟入

        if dist < min_dist:
            min_dist = dist
            best_pixel = pixel
    return best_pixel






def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    
    # ----- YOUR CODE STARTS HERE ----- #
    # Write code to populate image and create the 'ghost' effect

    for x in range(width):
        # Start by iterating through the first row: (0,0) → (0,1) → ...
        # then move on to the next row: (1,1), (1,2), etc.
        for y in range(height):
            pixels = []
            for image in images: # Go through all images and read their (0,0) pixel in sequence.
                pixel = image.get_pixel(x, y) # The (x, y) pixel from each image.
                pixels.append(pixel) # A list storing all pixels from all images at the same (x, y) position.

            best = get_best_pixel(pixels) # The best pixel at position (x, y).
            result.set_pixel(x, y, best) # Set the output image’s (x, y) pixel to the best one.



#-----------------------------------------------------------------------------------------------------------------------

    #### m1
    # green_im = SimpleImage.blank(20, 20, 'green')
    # green_pixel = green_im.get_pixel(0, 0)
    # print(get_pixel_dist(green_pixel, 5, 255, 10))

    #### m2
    # green_pixel = SimpleImage.blank(20, 20, 'green').get_pixel(0, 0)
    # red_pixel = SimpleImage.blank(20, 20, 'red').get_pixel(0, 0)
    # blue_pixel = SimpleImage.blank(20, 20, 'blue').get_pixel(0, 0)
    # print(get_average([green_pixel, green_pixel, green_pixel, blue_pixel]))

    #### m3
    # green_pixel = SimpleImage.blank(20, 20, 'green').get_pixel(0, 0)
    # red_pixel = SimpleImage.blank(20, 20, 'red').get_pixel(0, 0)
    # blue_pixel = SimpleImage.blank(20, 20, 'blue').get_pixel(0, 0)
    # best1 = get_best_pixel([green_pixel, blue_pixel, blue_pixel])
    # print(best1.red, best1.green, best1.blue)





    # ----- YOUR CODE ENDS HERE ----- #



    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
