import sqlite3
import os, sys
from PIL import Image
from hashlib import md5
import logging
import PIL
import imagehash
from collections import Counter
from glob import glob
import functions
# ctrl + / to comment out and reverse

#logging.basicConfig(filename='deleted_images.log', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.basicConfig(filename='exceptions.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def dhash(image, hash_size=128):
    try:
        # Convert the image to grayscale and resize it
        #image = image.convert('L').resize((hash_size + 1, hash_size), PIL.Image.Resampling.LANCZOS)
        img = image.resize((hash_size + 1, hash_size), PIL.Image.Resampling.LANCZOS)  # optional resizing
        img = img.convert('L')
        pixels = list(img.getdata()) # get pixel values
        print(pixels)
        # Calculate the difference between adjacent pixels
        diff = [1 if pixels[i] > pixels[i + 1] else 0 for i in range(len(pixels) - 1)]

        # Convert the binary difference to a hexadecimal hash
        return hex(int(''.join(map(str, diff)), 2))[2:]
    except Exception as e:
        xc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"An error occurred: {e}, {exc_tb.tb_lineno}")
        logging.info(f"Exception: {e}, {exc_tb.tb_lineno}")  # Log the exception


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
    duplicates = {}
    try:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    file_path = os.path.join(root, file_name)

                    with Image.open(file_path) as img:
                        img_initial=img
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
                            print(f"Duplicate found: {file_path} and {hashes[img_hash]}")
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

    #display all duplicate images
    for img_hash, files in duplicates.items():
        if len(files) > 1:
            file = open('duplicates.txt', 'w')
            file.write(f"Duplicate images with hash {img_hash}:\n")
            print(f"Duplicate images with hash {img_hash}:")
            for file_path in files:
                print(f"- {file_path}")
                file.write(f"- {file_path}\n")
            file.close()
#--------------------------------------------------------------------------------------------------------------------------

def find_near_duplicates(folder_path, threshold=5):
    # Dictionary to store hash values and file paths
    hashes = {}
    duplicates = []
    # Iterate through all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # Check if the file is an image
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file_name)

                # Open the image using Pillow
                with Image.open(file_path) as img:
                    # Calculate the perceptual hash of the image
                    img_hash = str(imagehash.average_hash(img))

                    # Check if a similar hash already exists
                    for h, path in hashes.items():
                        if abs(int(img_hash, 16) - int(h, 16)) <= threshold:
                            print(f"Near duplicate found: {file_path} and {path}")
                            duplicates.append(f"Near duplicate found: {file_path} and {path}")
                            #file = open('duplicates.txt', 'w')
                            #file.write(f"Near duplicate found: {file_path} and {path}\n")
                            break

                    #file.close()
                    hashes[img_hash] = file_path
    print(duplicates)
    file = open('duplicates.txt', 'w')
    for items in duplicates:
        if len(items) > 1:
            file.write(items+"\n")
    file.close()

#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#-------------------------------  End Definitions   -----------------------------------------------------------------------


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
    folder_path = "C:\\Users\\doitsinis\\PycharmProjects\\Thesis\\folder_108"
    print("Current folder : ", fold)
    print("Current folder : ", folder_path)
    #find_complete_duplicate_images(folder_path)
    #find_near_duplicates(folder_path)


if __name__ == "__main__":
    image_path = "C:\\Users\\doitsinis\\PycharmProjects\\Thesis\\folder_108\\iframe_73.jpg"
    #with Image.open(image_path) as img:
        #dhashing_image = dhash(img)
    #print(dhashing_image)
    #change 20240319

if __name__ == "__main__":
    image_path = "C:\\Users\\doitsinis\\PycharmProjects\\Thesis\\folder_108\\iframe_72.png"
    folder_path = "C:\\Users\\doitsinis\\PycharmProjects\\Thesis\\folder_108"
    #functions.img_is_black_or_white(folder_path)
    #result=functions.img_is_black_or_white(image_path)
    #if result:
    #    print(f"The image at '{image_path}' is either completely white or black.")
    #else:
    #    print(f"The image at '{image_path}' is not completely white or black.")
    # a change more changes

if __name__ == "__main__":
    image_path = "C:\\Users\\YannisPC\\PycharmProjects\\Thesis\\Thesis\\Crawler_results_Germany\\folder_1\\converted_iframe_1.jpg" # spiti\\converted_iframe_1.jpg"
    image_name = "converted_iframe_1.jpg"
    functions.delete_image(image_path)