#import matplotlib
import logging
# import matplotlib.image as mpimg
import os
import sys
import sqlite3
from pathlib import Path
import shutil
import cv2
import numpy as np

import matplotlib.pyplot as plt  # type: ignore

logging.basicConfig(filename='deleted_images.log', level=logging.INFO, format='%(asctime)s - %(message)s')

display_img_flag= False
delete_flag= False


def display_img(image1, image2) ->None:
    image1_dis = Image.open(image1)
    image_name1 = os.path.split(image1)
    #new_image1 = image1_dis.resize((256, 256))
    image2_dis = Image.open(image2)
    image_name2 = os.path.split(image2)
    #new_image2 = image2_dis.resize((256, 256))
    num_rows = 1
    num_cols = 2

    fig = plt.figure(figsize=(10, 7))

    #fig, axes = plt.subplots(num_rows, num_cols)  #figsize=(10, 5 * num_rows)
    fig.add_subplot(num_rows, num_cols, 1)
    # showing image
    plt.imshow(image1_dis)
    plt.axis('off')
    plt.title(image_name1[1])

    # Adds a subplot at the 2nd position
    fig.add_subplot(num_rows, 2, 2)
    # showing image
    plt.imshow(image2_dis)
    plt.axis('off')
    plt.title(image_name2[1])



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

def identify_image_color(folder_path, delete_flag): #image_path

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
                    write_in_file(file_name, f"{folder_path} All Black: ",folder_path)
                    if delete_flag:
                        file_path = os.path.join(folder_path, file_name)
                        delete_image(file_path)

                # Check if all pixels are white (255, 255, 255)
                is_all_white = all(pixels[x, y] == (255, 255, 255) for x in range(width) for y in range(height))
                if is_all_white:
                    img.close()
                    print(f"All White: {file_name}")
                    write_in_file(file_name, f"{folder_path} All White: ",folder_path)
                    if delete_flag:
                        file_path = os.path.join(folder_path, file_name)
                        delete_image(file_path)


                # Check if all pixels have the same color
                first_pixel_color = pixels[0, 0]
                is_all_same_color = all(pixels[x, y] == first_pixel_color for x in range(width) for y in range(height))
                if is_all_same_color:
                    img.close()
                    print(f"All Same Color: {file_name}")
                    write_in_file(file_name, f"{folder_path} All Same color: ", folder_path)
                    if delete_flag:
                        file_path = os.path.join(folder_path, file_name)
                        delete_image(file_path)

                file_path = os.path.join(folder_path, file_name)
                if is_mostly_same_color(file_path):
                    print(f"All Same Color: {file_name}")

                img.close()
                # If none of the above conditions are met, the image has multiple colors
                #print("Multiple Colors")


def write_in_file(same_image, same_color, file_path):
    file_path = os.path.join(file_path, same_image)
    file = open('Same_Images.txt', 'a')
    file.write(same_color + same_image+"\n")
    if display_img_flag:
        dummy_img= r"C:\Users\YannisPC\PycharmProjects\Thesis\Thesis\Crawler_results_Germany\folder_1\iframe_7.png"
        display_img(file_path,dummy_img)
    file.close()


def read_from_db(local_folder): # -> list[str]
    path = local_folder + "\\" + 'images.db'

    if os.path.isfile(path):
        #print("Current Folder in function", os.getcwd())
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute('SELECT file_name, is_ad FROM images')
        data = c.fetchall()
        # print(data)
        c.close
        conn.close()

        #for row in data:
        #    print(row)
        return data
    else:
        print("File image.db or path Not Exists")


def read_all_img_and_rename(folder_path: str) -> None:
    # call to rename all images in a folder if they are Ads.
    # new name = image_name_AD.png

    #new_path = r"C:\Users\YannisPC\PycharmProjects\Thesis\Thesis\Ads"

    images_data = read_from_db(folder_path)
    #print("Image Data", images_data)
    for img in images_data:
        if Path(img[0]).is_file():
            if img[1] == '1':
                print(img)
                image_name = os.path.split(img[0])
                print("Image name:", image_name[1])

                name, ext = os.path.splitext(image_name[1])

                abs_path = os.path.abspath(img[0])
                print("Absolute path: ", abs_path)

                new_abs_path = os.path.split(abs_path)
                print(new_abs_path)
                #print("target image: ", target_image)
                # move image to Ads folder
                try:
                    # renaming
                    new_name = f"{new_abs_path[0]}\\{name}_AD{ext}"
                    print("New_name: ", new_name)
                    #calling rename func.
                    rename_img(abs_path, new_name)

                    #target_image = f"{new_folder_path}\\{image_name[1]}"
                    #print("Target_name:" , target_image)
                    #shutil.move(abs_path, target_image) # move files
                    # print(f"File {image_name[1]} moved to Ads.")
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(f"An error occurred: {e}, {exc_tb.tb_lineno}")
                    # logging.info(f"Exception: {e}, {exc_tb.tb_lineno}")  # Log the exception

                # Path(abs_path).rename(target_image)
        else:
            # in case we have deleted an image
            print(f"Image: {Path(img[0])} not exist or renamed" )
            continue


# used to rename the images to ads or normal
def rename_img(old_name: str, new_name: str) -> None:
    try:
        os.rename(old_name, new_name)
        print(f"old_name: {old_name} - new name: {new_name}")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"An error occurred: {e}, {exc_tb.tb_lineno}")


#
def is_mostly_same_color(image_path, threshold=10) -> bool:
    try:
        # Load the image
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate the standard deviation of pixel values
        std_dev = np.std(gray_image)

        # Check if standard deviation is below the threshold
        if std_dev < threshold:
            return True  # Mostly the same color
        else:
            return False  # Contains useful information
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]  # type: ignore
        print("Error with image", image_path)
        print(f"An error occurred: {e}, {exc_tb.tb_lineno}")


def delete_subfolder(folder_path: str) ->None:
    print("Current folder to be deleted:",folder_path)
    full_path= f"{folder_path}\\subfolder"
    print("Full Path:",full_path)
    if os.path.exists(full_path):
        shutil.rmtree(full_path)
        print("Deleted folder:", full_path)