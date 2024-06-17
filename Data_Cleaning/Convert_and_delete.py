import sqlite3
import os, sys

#import pyvips
from PIL import Image
import logging
# read .svg # type: ignore
from collections import Counter
from glob import glob

# ctrl + / to comment out and reverse


logging.basicConfig(filename='exceptions.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def image_type_converter(folder_local):
    counter = 0
    try:
        for root, dirs, files in os.walk(folder_local):
            for file_name in files:
                if file_name.lower().endswith(('.png', '.bmp', '.tiff', '.gif', '.webp')):
                    if "converted" in file_name:
                        continue
                    else:
                        #print("Current Folder in function", folder_local)
                        full_path = folder_local + "\\" + file_name
                        print("Full path: ", full_path)
                        save_path = folder_local + "\\" + "converted_" + file_name
                        print("New path: ", save_path)
                        image_name = os.path.splitext(file_name)
                        print("Image name:", image_name[0]) #image name is a tuple
                        image_temp = Image.open(full_path)
                        image_temp = image_temp.convert('RGB')

                        image_temp.save(f"{folder_local}\\converted_{image_name[0]}.jpg")
                        #image_temp.save(save_path, "JPEG")
                        #print("Converted Image:", save_path)
                        counter += 1
                elif file_name.lower().endswith(('.svg')):
                    #image = pyvips.Image.thumbnail(file_name, 200)
                    file_name.write_to_file("test.png")
                else:
                    print(f"Skipped file: {file_name} (already in correct format)")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Exception details: ", exc_type, fname, exc_tb.tb_lineno)
        print(f"An exception occured: {e}")
        logging.info(f"Exception: {e}, {exc_tb.tb_lineno} , {file_name}")  # Log the deleted file name
    print("counter: ", counter)
# we call a func to verify if all images were converted to jpg successfully

# this is called after converter to delete all other images, testing
def delete_rest(folder_path):
    # delete whatever image doent have the word "new" in the name
    logging.info(f"Folder Delete Rest: {folder_path}")  # Log the deleted file name
    try:
        files_local = os.listdir(folder_path)
        for file_name in files_local:
            if file_name.lower().endswith(('.png', '.bmp', '.tiff', '.gif', '.svg', '.webp')):
                file_path = os.path.join(folder_path, file_name)
                print(file_path)
                os.remove(file_path)
                print(f"Deleted file: {file_name}")
                logging.info(f"Deleted file: {file_name}")  # Log the deleted file name
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"An error occurred: {e}, {exc_tb.tb_lineno}")
    #more changes




