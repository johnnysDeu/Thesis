
import os, sys
from PIL import Image
from hashlib import md5
import logging
import PIL
import imagehash
import numpy as np
from collections import Counter
from glob import glob
import functions
import time


# ctrl + / to comment out and reverse
# use type annotations x : int = 10
# data : dict[str, int] = {'bob':1 , 'john':2}
#elements: list[str] = [1, 2, 'a'] # Mypy gives a an error here


logging.basicConfig(filename='exceptions.log', level=logging.INFO, format='%(asctime)s - %(message)s')
Image.LOAD_TRUNCATED_IMAGES = True

#reading from the .db file

def find_complete_duplicate_images(folder_path, delete_flag) -> None:
    '''
    Function uses Hash algorithm to find complete duplicate images.
    It calulates the Hash for all images in a folder and stores the Hashes in a dictionary [Hash, Image].
    If image with same hash if found, it is stored in the duplicates dictionary.
    If the "Delete_flag" is True, we call the delete_image() func to delete the duplicate.
    Finally it saves the detail of the duplicates in a TXT file for keeping history
    This function doesnt work very well because the images need to be completely identical and have the same hash.
    We use this func together with the find_near_duplicates()
    '''
    # Dictionary to store file hashes

    hashes: dict[str, str] = {}
    duplicates = {}
    try:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    file_path = os.path.join(root, file_name)

                    with Image.open(file_path) as img:
                        img_initial=img #for debugging
                        # Resize the image to reduce hash computation time
                        img = img.resize((128, 128), PIL.Image.Resampling.LANCZOS) # optional resizing
                        # Convert image to grayscale
                        img = img.convert('L')
                        #print(img)
                        # Calculate MD5 hash of the image
                        img_hash = md5(img.tobytes()).hexdigest()
                        #print(img_hash)
                        #print(hashes)

                        # Check if the hash already exists
                        if img_hash in hashes:
                            #print(f"Duplicate found: {file_path} and {hashes[img_hash]}")
                            if img_hash not in duplicates:
                                duplicates[img_hash] = [hashes[img_hash]]
                            duplicates[img_hash].append(file_path)
                        else:
                            hashes[img_hash] = file_path
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"An error occurred: {e}, {exc_tb.tb_lineno}")
        logging.info(f"Exception: {e}, {exc_tb.tb_lineno}")  # Log the exception


    ### storing the findings in a TXT file
    #print("Duplicate Tuples", duplicates)
    folder_name = os.path.split(folder_path)
    # print(folder_name)
    new_file = "complete_duplicates_" + folder_name[1] + ".txt"
    #display all duplicate images
    for img_hash, files in duplicates.items():
        if len(files) > 1:
            #file = open('duplicates.txt', 'w')
            file = open(new_file, 'a') # append mode, to avoid overwriting
            file.write(f"Duplicate images with hash {img_hash}:\n")
            #print(f"Duplicate images with hash {img_hash}:")
            file_cnt = 0
            for file_path in files:
                #print(f"- {file_path}")
                file.write(f"- {file_path}\n")
                if file_cnt >= 1:
                    if delete_flag:
                        print("Delete second Tuple:", file_path)
                        # here we will call delete_image()
                        #functions.delete_image(file_path)
                file_cnt = file_cnt + 1
            file.close()
#--------------------------------------------------------------------------------------------------------------------------


def find_near_duplicates(folder_path, delete_flag, log_flag) -> None:
    '''
        Function uses pHash algorithm to find near identical images.
        pHash includes a hash comparison and if it is smaller than a threshold, then the images are considered near identical.
        If the "Delete_flag" is True, we call the delete_image() func to delete the duplicate.
        Finally, it saves the detail of the duplicates in a TXT file for keeping history
        This function works very recognizing similar images that have slightly different resolution or size.
    '''

    # Dictionary to store hash values and file paths
    threshold: int = 5
    hashes: dict[str, str] = {}
    duplicates: list[str] = []
    # Iterate through all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # Check if the file is an image
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file_name)

                # Open the image using Pillow
                with Image.open(file_path) as img:
                    # image processing
                    img = img.resize((128, 128), Image.ANTIALIAS)
                    img = img.convert('L')  # Convert to grayscale

                    # Calculate the perceptual hash of the image
                    img_hash = str(imagehash.average_hash(img))
                    #print("Img_hash", img_hash)
                    # Check if a similar hash already exists
                    for h, path in hashes.items():
                        #print("Int Hash", int(img_hash, 16))
                        #print("Int Hash H", int(h, 16))

                        if abs(int(img_hash, 16) - int(h, 16)) <= threshold: # hamming distance for HEX
                            #print(f"Near duplicate found: {file_path} and {path}")
                            duplicates.append(f"Near duplicate found: {file_path} and {path}")

                            #call display images to check the pairs
                            #functions.display_img(file_path, path)

                            # call detele_image to delete only the second in each pair
                            if delete_flag:
                               print("Delete second Tuple:", path)
                               # here we will call delete_image()
                               functions.delete_image(path)
                            #functions.delete_image(path)
                            #file = open('duplicates.txt', 'w')
                            #file.write(f"Near duplicate found: {file_path} and {path}\n")
                            #file.close() # this will overwrite all and leave only the last pair
                            break
                    hashes[img_hash] = file_path
    print(duplicates)
    if log_flag:
        folder_name = os.path.split(folder_path)
        new_file2 = "Near_duplicates_" + folder_name[1] + ".txt"
        file = open(new_file2, 'w')
        for items in duplicates:
            if len(items) > 1:
                file.write(items+"\n")
        file.close()
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#-------------------------------  End Definitions   -----------------------------------------------------------------------


