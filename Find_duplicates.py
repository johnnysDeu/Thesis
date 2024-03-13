import sqlite3
import os
from PIL import Image


def read_from_db():
    c.execute('SELECT file_name FROM images')
    data = c.fetchall()
    # print(data)
    return data
    # for row in data:
    #    print(row)


def image_type_converter(image):
    image_name = os.path.splitext(image)
    print("Image name:", image_name[0]) #image name is a tuple
    image_temp = Image.open(image)
    image_temp = image_temp.convert('RGB')
    image_temp.save(f"converted_{image_name[0]}.jpg")
    print("Image converted.")

# this is called after converter to delete all other images
def delete_rest():


# create_table()
# data_entry()

conn = sqlite3.connect('images.db')
c = conn.cursor()



# for i in range(1):
images_data = read_from_db()
print(len(images_data))
print(*images_data)
    # time.sleep(1)

c.close
conn.close()

#file_name = os.path.basename('/Crawler_results_Germany/Crawler_results_Germany/folder_1/iframe_1.png')
# file name without extension
#print(os.path.splitext(file_name)[0])

#for filename in os.listdir(os.getcwd()):
#    with open(os.path.join(os.getcwd(), filename), 'r') as f:  # open in readonly mode
        # do your stuff


print(os.listdir())
print(os.getcwd())
#image_type_converter('iframe_1.png')


for images in images_data:
    file_name = os.path.basename(images[0])
    #images_2 = os.path.splitext(file_name)
    print(file_name)
    #print(os.path.splitext(file_name))
    image_type_converter(file_name) # tuple
    #print(images[0])

