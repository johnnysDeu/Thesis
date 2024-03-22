from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def load_images_from_file(file_path):
    image_pairs = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                paths = line.split(' and ')
                if len(paths) == 2:
                    image_pairs.append((Image.open(paths[0]), Image.open(paths[1])))
    return image_pairs

def create_image_grid(image_pairs):
    num_pairs = len(image_pairs)
    num_rows = (num_pairs + 1) // 2
    fig, axes = plt.subplots(num_rows, 2, figsize=(10, 5*num_rows))

    for idx, (img1, img2) in enumerate(image_pairs):
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

def main():
    file_path = 'image_paths.txt'
    image_pairs = load_images_from_file(file_path)
    create_image_grid(image_pairs)

if __name__ == "__main__":
    main()
