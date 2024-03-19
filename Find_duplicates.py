import sqlite3
import os, sys
from PIL import Image
import logging
from collections import Counter
from glob import glob

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


def image_type_converter(image, folder_local):
    try:
        print("Current Folder in function", folder_local)
        full_path = folder_local + "\\" + image
        print("Full path: ", full_path)
        save_path = folder_local + "\\" + "converted_" + image
        print("New path: ", save_path)
        image_name = os.path.splitext(image)
        print("Image name:", image_name[0]) #image name is a tuple
        image_temp = Image.open(full_path)
        image_temp = image_temp.convert('RGB')
        print("Image Temp:", image_temp)
        image_temp.save(f"{folder_local}\\converted_{image_name[0]}.jpg")
        image_temp.save(save_path, "JPEG")
        print("Converted Image:", save_path)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Exception details: ", exc_type, fname, exc_tb.tb_lineno)
        print(f"An exception occured: {e}")
        logging.info(f"Exception: {e}, {exc_tb.tb_lineno} , {image}")  # Log the deleted file name

# we call a func to verify if all images were converted to jpg successfully

# this is called after converter to delete all other images
def delete_rest(folder_path):
    # delete whatever image doent have the word "new" in the name
    logging.info(f"Folder: {folder_path}")  # Log the deleted file name
    try:
        files_local = os.listdir(folder_path)
        for file_name in files_local:
            if file_name.lower().endswith(('.png', '.bmp', '.tiff', '.gif')):
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


Current_dir = os.getcwd()

subfolders = [ f.path for f in os.scandir(Current_dir) if f.is_dir()]
#print(subfolders)
#image_type_converter('iframe_1.png')

for fold in list(subfolders):
    files = os.listdir(fold)
    #print("Current folder : ", fold)
    images_data = read_from_db(fold)
    #print(images_data)
    #print(os.getcwd())

# this is working
counter = 0
for files in os.listdir(fold):
    if files.lower().endswith(('.png', '.bmp', '.tiff', '.gif')):
        print(files)
        print(fold)
        counter += 1
        image_type_converter(files, fold)
    else:
        print(f"Skipped file: {files} (already in correct format)")
print("counter: ", counter)

#delete_rest(fold)

#change 20240319