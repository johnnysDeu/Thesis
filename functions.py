#import matplotlib
import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
from PIL import Image
import os, sys
import logging
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
import cv2
logging.basicConfig(filename='deleted_images.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def display_img(image1, image2):
    image1_dis = Image.open(image1)
    new_image1 = image1_dis.resize((128, 128))
    image2_dis = Image.open(image2)
    new_image2 = image2_dis.resize((128, 128))
    num_rows =1
    fig, axes = plt.subplots(num_rows, 2, figsize=(10, 5 * num_rows))
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                     nrows_ncols=(1, 2),  # creates 2x2 grid of axes
                     axes_pad=0.1,  # pad between axes in inch.
                     )
    for ax, im in zip(grid, [new_image1, new_image2]):
        # Iterating over the grid returns the Axes.
        ax.imshow(im)

    #image = Image.open(image1)
    #image.show()


def img_is_black_or_white_old(image_path):
    threshold= 240
    with Image.open(image_path) as img:
        min_val, max_val = img.convert("L").getextrema()
        print(min_val)
        if min_val >= threshold or max_val <= threshold: # full black means: max_val=0 and min_val=0
            return True # True means either black or white
        else:
            return False


def img_is_black_or_white(folder_path):
    black_and_white = []

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file_name)
                threshold= 240
                with Image.open(file_path) as img:
                    min_val, max_val = img.convert("L").getextrema() #convert("L").
                    im_extr = img.getextrema()
                    print("Single values extrema", im_extr)
                    print("Image name: ", file_path)
                    print(f"Min val: {min_val}, Max val: {max_val}")
                    if min_val >= threshold or max_val <= threshold: # full black means: max_val=0 and min_val=0
                        black_and_white.append(f"Black or white image: {file_path}")
                        #return True # True means either black or white
                    #else:
                        #return False

    print(black_and_white)
    file = open('black_and_white.txt', 'w')
    for items in black_and_white:
        if len(items) > 1:
            file.write(items + "\n")
    file.close()


def delete_image(file_path):

    logging.info(f"Folder: {file_path}")  # Log the deleted file name
    file_name = os.path.split(file_path)
    print("File Name:", file_name[1])
    print("Path:", file_name[0])
    try:
        if file_name[1].lower().endswith(('.png', '.bmp', '.tiff', '.gif', '.jpg')):
            if os.path.isfile(file_path):
                print(f"Deleted file: {file_name[1]}")
                logging.info(f"Deleted file: {file_name[1]}")  # Log the deleted file name
                os.remove(file_path)
            else:
                print(f"The file {file_path} does not exist")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"An error occurred: {e}, {exc_tb.tb_lineno}")


from PIL import Image

def identify_image_color(folder_path): #image_path

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file_name)
                # Open the image
                img = Image.open(file_path)
                # Get the dimensions of the image
                width, height = img.size
                # Get the pixel data
                pixels = img.load()

                # Check if all pixels are black (0, 0, 0)
                is_all_black = all(pixels[x, y] == (0, 0, 0) for x in range(width) for y in range(height))
                if is_all_black:
                    img.close()
                    print(f"All Black: {file_name}")
                    write_in_file(file_name, f"{folder_path} All Black: ")

                # Check if all pixels are white (255, 255, 255)
                is_all_white = all(pixels[x, y] == (255, 255, 255) for x in range(width) for y in range(height))
                if is_all_white:
                    img.close()
                    print(f"All White: {file_name}")
                    write_in_file(file_name, f"{folder_path} All White: ")


                # Check if all pixels have the same color
                first_pixel_color = pixels[0, 0]
                is_all_same_color = all(pixels[x, y] == first_pixel_color for x in range(width) for y in range(height))
                if is_all_same_color:
                    img.close()
                    print(f"All Same Color: {file_name}")
                    write_in_file(file_name, f"{folder_path} All Same color: ")

                img.close()
                # If none of the above conditions are met, the image has multiple colors
                #print("Multiple Colors")


def write_in_file(same_image, same_color):
    file = open('Same_Images.txt', 'a')
    file.write(same_color + same_image+"\n")
    file.close()