from PIL import Image as PImage
import matplotlib.pyplot as plt
import numpy as np
from skimage import io
import os
from os import listdir

def load_images_from_file(file_path) : #-> list[tuple[str,str]]
    '''
    i use this func to display the near duplicate images so for debugging reasons.
    load the image path from the near_duplicate.txt, split for 'and'
    '''
    image_pairs = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                # remove "Near duplicate found: "
                line = line.replace("Near duplicate found: ","")
                print("Line:", line)
                paths = line.split(' and ')
                image_name1 = os.path.split(paths[0])
                imgs = loadImages(image_name1)

                image_name2 = os.path.split(paths[1])
                if len(paths) == 2:
                    img = io.imread(paths[0], format = 'JPG')
                    io.imshow(img)
                    img2 = io.imread(paths[1], format = 'JPG')
                    io.imshow(img2)


                    image_pairs.append((PImage.open(paths[0]), PImage.open(paths[1])))
    return image_pairs


def create_image_grid(image_pairs) -> None:
    num_pairs = len(image_pairs)
    num_rows = (num_pairs + 1) // 2
    fig, axes = plt.subplots(num_rows, 2, figsize=(10, 5*num_rows))

    for idx, (img1, img2) in enumerate(image_pairs):
        image = PImage.open(img1)
        image.show()
        image = PImage.open(img2)
        image.show()

        row_idx = idx // 2
        col_idx = idx % 2
        ax = axes[row_idx, col_idx]
        ax.imshow(img1)
        ax.axis('off')
        ax = axes[row_idx, col_idx + 1]
        ax.imshow(img2)
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def loadImages(path):
    # return array of images

    imagesList = listdir(path)
    loadedImages = []
    for image in imagesList:
        img = PImage.open(path + image)
        loadedImages.append(img)

    return loadedImages


def main() -> None:
    file_path = 'near_duplicates_folder_1.txt'
    #image_pairs = load_images_from_file(file_path)
    #create_image_grid(image_pairs)

if __name__ == "__main__":
    main()
