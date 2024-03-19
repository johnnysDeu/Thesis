import sqlite3
import os, sys
from PIL import Image
from hashlib import md5
import logging
from collections import Counter
from glob import glob
import functions
# ctrl + / to comment out and reverse

#logging.basicConfig(filename='deleted_images.log', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.basicConfig(filename='exceptions.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def read_from_db(local_folder):
    path = local_folder + "\\" + 'images.db'
    #print(path)
    if os.path.isfile('images.db'):
        #print("Current Folder in function", os.getcwd())
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute('SELECT file_name FROM images')
        data = c.fetchall()
        # print(data)
        c.close
        conn.close()
        return data
        # for row in data:
        #    print(row)
    else:
        print("File image.db Not Exists")


def find_complete_duplicate_images(folder_path):
    # Dictionary to store file hashes
    hashes = {}
    try:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    file_path = os.path.join(root, file_name)

                    with Image.open(file_path) as img:
                        #img_initial=img
                        # Resize the image to reduce hash computation time
                        #img = img.resize((8, 8), Image.ANTIALIAS) # optional resizing
                        # Convert image to grayscale
                        img = img.convert('L')
                        print(img)
                        # Calculate MD5 hash of the image
                        img_hash = md5(img.tobytes()).hexdigest()
                        #print(img_hash)
                        #print(hashes)


                        # Check if the hash already exists
                        if img_hash in hashes:
                            print(f"Duplicate found: {file_path} and {hashes[img_hash]}")
                            #functions.print_img(img_initial)
                        else:
                            hashes[img_hash] = file_path
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"An error occurred: {e}, {exc_tb.tb_lineno}")
        logging.info(f"Exception: {e}, {exc_tb.tb_lineno}")  # Log the exception


Current_dir = os.getcwd()


subfolders = [f.path for f in os.scandir(Current_dir) if f.is_dir()]
#print(subfolders)
#image_type_converter('iframe_1.png')

for fold in list(subfolders):
    files = os.listdir(fold)
    #print("Current folder : ", fold)
    images_data = read_from_db(fold)
    #print(images_data)
    #print(os.getcwd())


if __name__ == "__main__":
    folder_path = "../folder_109"
    print("Current folder : ", fold)
    find_complete_duplicate_images(fold)


#change 20240319