#import matplotlib
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
from PIL import Image
import os, sys


def print_img(image):
    #img = mpimg.imread(image)
    #imgplot = plt.imshow(img)
    #plt.show()

    image = Image.open(image)
    image.show()

def img_is_black_or_white(image_path):
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


