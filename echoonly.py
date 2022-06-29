import numpy as np     #
import os              #
import cv2             # Importing all required libraries
import csv             #
import pydicom         #
import time            #

st = time.time()    # This is start time
dicom_path = "C:/intern/New folder/avi/DICOM"  # This is input folder from which dicom files are to be taken
output_path = "C:/intern/echo"    # Output folder

if not os.path.exists(output_path + "/frames"):     # If the specified path is not existed
    os.mkdir(output_path + "/frames")            # We are creating that directory
if not os.path.exists(output_path + "/womframes"):  #
    os.mkdir(output_path + "/womframes")            #     Creating 5 folders in output folder
if not os.path.exists(output_path + "/video"):      #   5 folders are
    os.mkdir(output_path + "/video")                #       frames = folder that contains full sized frames
if not os.path.exists(output_path + "/womvideo"):   #       womframes = folder that contains cropped frames, i.e without any marking(wom)
    os.mkdir(output_path + "/womvideo")             #       video =  folder that contains video with full sized frames
if not os.path.exists(output_path + "/csvfiles"):   #       womvideo = folder that contains video with cropped frames
    os.mkdir(output_path + "/csvfiles")             #       csvfiles =  folder that contains csv files which contain information about each dicom file

dicom_list = os.listdir(dicom_path)    # dicom_list = List that contains all the dicoms present in input folder
dicom_list = sorted(dicom_list)    #    Sorting them in alphabetical order
print(dicom_list)       # Printing the names of dicom files and to check if the files are correct
lent = len(dicom_list)   # No.of dicom files present in input folder
for j in range(lent):      # for loop executes "lent" times
    filename = os.path.join(dicom_path, dicom_list[j])   # Joining dicom_path and name of each dicom file to get directory of each dicom file
    ds = pydicom.dcmread(filename, force=True)   # Reading the contents of dicom file and storing in variable 'ds'
    arr = ds.pixel_array  # Pixel_array function extract data from tag "Pixel Data" in 'ds' and converts into readable form
    arr_frames = np.array(arr)  # Converting arr to a numpy array

    with open('C:/intern/echo/csvfiles/csvfile_%d.csv' % j, 'w', newline='') as csvfile:   # Opening csv file in write mode
        writer = csv.writer(csvfile)   # We use csv.writer class to insert data into csv file
        writer.writerow("Tag Description VR value".split())   # To write a single row in csv file
        for elem in ds:                                                     #
            writer.writerow({                                               #
                elem.tag, elem.description(), elem.VR, str(elem.value)      #   storing data into csv file
            })
    try:
        print(ds[0x0028, 0x0008])      # This tag contains no of frames
        if not os.path.exists(output_path + "/frames/dcmfile_%d" % j):  #  Creating folder for each dicom file to save
            os.mkdir(output_path + "/frames/dcmfile_%d" % j)            #  frames extracted from ds
        marked_frame_dir = (output_path + "/frames/dcmfile_%d" % j)     #  marked_frame_dir is directory of each such folder
        if not os.path.exists(os.path.join(output_path, "womframes/wmdcmfile_%d" % j)): #  Creating folder to save
            os.mkdir(os.path.join(output_path, "womframes/wmdcmfile_%d" % j))           #  cropped frames from ds
        unmarked_frame_dir = (os.path.join(output_path, "womframes/wmdcmfile_%d" % j))
        print(marked_frame_dir)
        img_arr = []     # Creating empty array to store uncropped frames
        img_array = []   # Creating empty array to store cropped frames

        for i in range(len(arr_frames)):
            image = pydicom.pixel_data_handlers.convert_color_space(arr_frames[i], 'YBR_FULL_422', 'RGB')   # Changing colour space of each frame
            cv2.imwrite(os.path.join(marked_frame_dir, "frame%d.jpg" % i), image) # Saving the image in specified directory
            height, width, layer = image.shape  # .shape returns height, width, layers of an image
            size1 = (width, height)
            img_arr.append(image)

            img = image.copy()      # img is a copy of image
            img = img[70:580, 230:660]   # Determining the coordinates to which img is to be cropped
            cv2.imwrite(os.path.join(unmarked_frame_dir, "wmframe_%d.jpg" % i), img) # Saving the image in specified directory
            height, width, layes = img.shape # .shape returns height, width, layers of an image
            size2 = (width, height)
            img_array.append(img) # Appending all the frames into img_array
        vid_full = cv2.VideoWriter(os.path.join(output_path, "video/avivideo_%d.avi" % j), cv2.VideoWriter_fourcc(*'DIVX'),
                              15, size1)   # saving the video made from full sized frames
        for q in range(len(img_arr)):
            vid_full.write(img_arr[q])      # Inserting each frame into video
        vid_full.release()

        vid = cv2.VideoWriter(os.path.join(output_path, "womvideo/avivideo_%d.avi" % j), cv2.VideoWriter_fourcc(*'DIVX'),
                              15, size2)    # saving the video from cropped frames
        for k in range(len(img_array)):
            vid.write(img_array[k])  # Inserting each frame into video
        vid.release()

    except KeyError:   # Control comes here when try loop returns any error
        if not os.path.exists(output_path + "/frames/dcmfile_%d" % j):  #
            os.mkdir(output_path + "/frames/dcmfile_%d" % j)            # Creating folder for each dicom file
        path2 = (output_path + "/frames/dcmfile_%d" % j)                # to save single frame images
        print(path2)
        cv2.imwrite(os.path.join(path2, "sinle_frame_%d.jpg" % j), arr_frames)  # Saving the images

et = time.time()   # This is end time
time_elapsed = et - st   # Total runtime

print("Time elapsed = " + str(time_elapsed) + " sec")
