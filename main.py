import time
#from tqdm import tqdm # too slow
import functions
import Convert_and_delete, display_images
import os, sys
from pathlib import Path
import shutil
import Find_duplicates
from time import sleep



# when delete flag = true, delete the duplicate
# run this for all folders
delete_flag = False
log_flag = False
copy_image_flag = True


start_time = time.time()
if __name__ == "__main__":
    # Current_dir = os.getcwd()
    Current_dir = "C:\\Users\\YannisPC\\PycharmProjects\\Thesis\\Thesis\\Crawler_results_Germany"
    #Current_dir = r"C:\Users\doitsinis\PycharmProjects\Thesis\Crawler_results_Germany"
    subfolders = [f.path for f in os.scandir(Current_dir) if f.is_dir()]
    #print(subfolders)
    # call for all folders in Germany
    for fold in list(subfolders):
        files = os.listdir(fold)
        print("Current folder : ", fold)

        #functions.identify_image_color(fold, delete_flag)  # about 8-12 min runtime , First to run
        #Find_duplicates.find_complete_duplicate_images(fold, delete_flag, log_flag) # about 8 min runtime
        #Find_duplicates.find_near_duplicates(fold, delete_flag, log_flag, copy_image_flag)# about 10 min runtime
        #images_data = read_from_db(fold)

        #functions.read_all_img_and_rename(fold)  # renaming images when ADs

        #Convert_and_delete.image_type_converter(fold)
        #Convert_and_delete.delete_rest(fold)

        # delete all "subfolder" folders
        #functions.delete_subfolder(fold)

#print("Same color image Identification finished.")
print("--- %s seconds ---" % (time.time() - start_time))


# run this for specific folder
start_time = time.time()
if __name__ == "__main__":
    #for i in tqdm(range(100)):
        #folder_path = "C:\\Users\\doitsinis\\PycharmProjects\\Thesis\\Crawler_results_Germany\\folder_2"# douleia
        folder_path = "C:\\Users\\YannisPC\\PycharmProjects\\Thesis\\Thesis\\Crawler_results_Germany\\folder_94"  #spiti
        #print("Current folder : ", fold)
        print("Current folder : ", folder_path)
        folder_name = os.path.split(folder_path)
        #functions.delete_subfolder(folder_path)
        #print(folder_name)
        #Find_duplicates.find_complete_duplicate_images(folder_path, delete_flag, copy_image_flag)
        Find_duplicates.find_near_duplicates(fold, delete_flag, log_flag, copy_image_flag)
        #Find_duplicates.find_near_duplicates(folder_path, delete_flag, log_flag, copy_image_flag)
        #functions.identify_image_color(folder_path, delete_flag)                # this func has issue with .gif images. we need to convert all first
        #functions.read_all_img_and_rename(folder_path) # renaming images when ADs

        #sleep(0.02)

print("--- %s seconds ---" % (time.time() - start_time))


# black and white image, testing
if __name__ == "__main__":
    image_path = "C:\\Users\\doitsinis\\PycharmProjects\\Thesis\\Crawler_results_Germany\\folder_108\\iframe_72.png"
    folder_path = "C:\\Users\\doitsinis\\PycharmProjects\\Thesis\\Crawler_results_Germany\\folder_108"
    #functions.img_is_black_or_white(folder_path)
    #result=functions.img_is_black_or_white(image_path)
    #if result:
    #    print(f"The image at '{image_path}' is either completely white or black.")
    #else:
    #    print(f"The image at '{image_path}' is not completely white or black.")
    # a change more changes

# call detele image, testing
if __name__ == "__main__":
    #image_path = "C:\\Users\\YannisPC\\PycharmProjects\\Thesis\\Thesis\\Crawler_results_Germany\\folder_1\\converted_iframe_1.jpg" # spiti\\converted_iframe_1.jpg"
    image_name = "converted_iframe_1.jpg"
    #functions.delete_image(image_path)


#Displaying similar images, testing
if __name__ == "__main__":
    print("  ")
    #file_path = r"C:\Users\YannisPC\PycharmProjects\Thesis\Thesis\duplicates_folder_3.txt"
    #functions.display_images(file_path)

#Reading from DB file and moving ads to a folder
if __name__ == "__main__":
    folder_path = r"C:\Users\YannisPC\PycharmProjects\Thesis\Thesis\Crawler_results_Germany\folder_3"
    new_path = r"C:\Users\YannisPC\PycharmProjects\Thesis\Thesis\Crawler_results_Germany\Ads"
    #half_path= r"C:\Users\YannisPC\PycharmProjects\Thesis\Thesis"

    #functions.read_all_img_and_rename(folder_path)

    # images_data = functions.read_from_db(folder_path)
    # print("Image Data", images_data)
    # for img in images_data:
    #     if Path(img[0]).is_file():
    #         if img[1]== '1':
    #             print(img)
    #             image_name = os.path.split(img[0])
    #             print("Image name:", image_name[1])
    #
    #             name, ext = os.path.splitext(image_name[1])
    #
    #             target_image = f"{new_path}\\{image_name[1]}"
    #             abs_path = os.path.abspath(img[0])
    #             print("Absolute path: ", abs_path)
    #             print("target image: ", target_image)
    #             # move image to Ads folder
    #             try:
    #                 # renaming
    #                 new_name= f"{name}_AD{ext}"
    #                 print("New_name: ", new_name)
    #
    #                 #shutil.move(abs_path, target_image) # move files
    #                 #print(f"File {image_name[1]} moved to Ads.")
    #             except Exception as e:
    #                 exc_type, exc_obj, exc_tb = sys.exc_info()
    #                 fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #                 print(f"An error occurred: {e}, {exc_tb.tb_lineno}")
    #                 #logging.info(f"Exception: {e}, {exc_tb.tb_lineno}")  # Log the exception
    #
    #             #Path(abs_path).rename(target_image)
    #     else:
    #         # in case we have deleted an image
    #         continue


#convert to JPEG
counter = 0
if __name__ == "__main__":
    folder_path = r"C:\Users\YannisPC\PycharmProjects\Thesis\Thesis\Crawler_results_Germany\folder_2"
    #folder_path = r"C:\Users\doitsinis\PycharmProjects\Thesis\Crawler_results_Germany\folder_1" # douleia
    print("Current folder : ", folder_path)
    #Convert_and_delete.image_type_converter(folder_path)
    #Convert_and_delete.delete_rest(folder_path) # delete everything that is not .jpg and .db

if __name__ == "__main__":
    #print("Running Display image as Thumbnail")
    folder_path = r"C:\Users\doitsinis\PycharmProjects\Thesis\Crawler_results_Germany\folder_109"  # douleia
    #display_images.display_thumbnails(folder_path)