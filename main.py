import os
import time
from tqdm import tqdm # too slow
import functions
import Find_duplicates
from time import sleep
# when delete flag = true, delete the duplicate
# run this for all folders
delete_flag = True
log_flag = False
start_time = time.time()
if __name__ == "__main__":
    # Current_dir = os.getcwd()
    Current_dir = "C:\\Users\\YannisPC\\PycharmProjects\\Thesis\\Thesis\\Crawler_results_Germany"
    subfolders = [f.path for f in os.scandir(Current_dir) if f.is_dir()]
    # print(subfolders)
    # call for all folders in Germany
    for fold in list(subfolders):
        files = os.listdir(fold)
        print("Current folder : ", fold)
        #Find_duplicates.find_complete_duplicate_images(fold, delete_flag) # about 8 min runtime
        #Find_duplicates.find_near_duplicates(fold, delete_flag, log_flag) # about 8 min runtime
        #images_data = read_from_db(fold)
        #functions.identify_image_color(fold)   # about 5 min runtime
print("Same color image Identification finished.")
print("--- %s seconds ---" % (time.time() - start_time))

# when delete flag = true, delete the duplicate
delete_flag = False
log_flag = False
# run this for specific folder
start_time = time.time()
if __name__ == "__main__":
    #for i in tqdm(range(100)):
        #folder_path = "C:\\Users\\doitsinis\\PycharmProjects\\Thesis\\folder_108"# douleia
        folder_path = "C:\\Users\\YannisPC\\PycharmProjects\\Thesis\\Thesis\\Crawler_results_Germany\\folder_63"  #spiti
        #print("Current folder : ", fold)
        #print("Current folder : ", folder_path)
        folder_name = os.path.split(folder_path)
        print(folder_name)
        #Find_duplicates.find_complete_duplicate_images(folder_path)
        #Find_duplicates.find_near_duplicates(folder_path, delete_flag, log_flag)
        #functions.identify_image_color(folder_path)

        #sleep(0.02)

print("--- %s seconds ---" % (time.time() - start_time))


# black and white image, testing
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

# call detele image, testing
if __name__ == "__main__":
    image_path = "C:\\Users\\YannisPC\\PycharmProjects\\Thesis\\Thesis\\Crawler_results_Germany\\folder_1\\converted_iframe_1.jpg" # spiti\\converted_iframe_1.jpg"
    image_name = "converted_iframe_1.jpg"
    #functions.delete_image(image_path)


#Displaying similar images, testing
if __name__ == "__main__":
    file_path = r"C:\Users\YannisPC\PycharmProjects\Thesis\Thesis\duplicates_folder_3.txt"
    #functions.display_images(file_path)