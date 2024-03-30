#import matplotlib
import logging
# import matplotlib.image as mpimg
import os
import sys

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