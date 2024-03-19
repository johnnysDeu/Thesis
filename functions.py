#import matplotlib
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
from PIL import Image

def print_img(image):
    #img = mpimg.imread(image)
    #imgplot = plt.imshow(img)
    #plt.show()

    image = Image.open(image)
    image.show()