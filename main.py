import time
import cv2
import sys
from aravis import Camera
from panorama import Stitcher
import imutils
import measure_lines
import argparse
import os


def start_capture():

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dist",type=float, required=True,
        help="distance between camera and object in cm")
    args = vars(ap.parse_args())

    #path where images are stored
    path='/home/santana/Desktop/genieCam/images/'

    try:
        args = vars(ap.parse_args())
        #initialize both cameras
        cam = Camera('Teledyne DALSA-Nano-M2420-S1187124')
        cam2 = Camera('Teledyne DALSA-Nano-M2420-S1187109')
        #get distance of between cameras and object, input by user
        distance = args["dist"]
        #set frame rate and region of capture
        cam.set_frame_rate (2.0)
        cam2.set_frame_rate(2.0)
        cam.set_region (0,0,2464,2056)
        cam2.set_region (0,0,2464,2056)
        #start both cameras
        cam.start_acquisition_continuous()
        cam2.start_acquisition_continuous()
        #initialize sticher object
        stitcher = Stitcher()
        
        #define windows of capture cameras
        cv2.namedWindow("capture", flags=0)
        cv2.namedWindow("capture2", flags=0)

        #set counters
        img_counter = 0
        count = 0
        while True:
            count += 1
            print("frame nb: ", count)
            #get frames from cameras
            frame = cam.pop_frame()
            frame2 = cam2.pop_frame()
            #resize image of cameras
            #cropped = imutils.rotate(frame, 6)
            #cropped2 = imutils.rotate(frame2, -6)
            #cropped = cropped[0:2056, 0:2224]
            #cropped2 = cropped2[0:2056, 240:2464]
            left = imutils.resize(frame, width=1000)
            right = imutils.resize(frame2, width=1000)
            #result = stitcher.stitch([left, right])
            print("shape: ", frame.shape)
            print(time.time())
            #if frame exists
            if not 0 in frame.shape and frame2.shape:
                #show frames in window with opencv
                cv2.imshow("capture", left)
                cv2.imshow("capture2", right)
                #cv2.imshow('Result', result)
                k=cv2.waitKey(1)
            #if space bar is pressed
            if k%256 == 32:
                #save image to file of left camera
                img_name = "opencv_frame_left{}.tif".format(img_counter)
                cv2.imwrite(os.path.join(path, img_name), frame)
                print("{} written!".format(img_name))
                #get measurements of laser lines
                #L=measure_lines.measure(img_name,distance)
                #print(L)
                #save image to file of right camera
                img_name = "opencv_frame_right{}.tif".format(img_counter)
                cv2.imwrite(os.path.join(path, img_name),frame2)
                print("{} written!".format(img_name))
                #get measurements of laser lines
                #R=measure_lines.measure(img_name,distance)
                #print(R)

                #merge = stitcher.stitch([left, right])
                #img_name = "opencv_frame_merge{}.tif".format(img_counter)
                #cv2.imwrite(img_name, merge)
                #print("{} written!".format(img_name))
                #measure_lines.measure(img_name,distance)
                img_counter += 1
            #if key 'q' is pressed or esc, break loop
            elif k==27 or k == ord('q'):
                break
    except:
        print('Error initializing cameras')
        print('restarting after 5 seconds')
        time.sleep(5)
        start_capture()
        
    finally:
        #destroy opencv windows and stop acquisiton of cameras
        cv2.destroyAllWindows()
        cam.stop_acquisition()
        cam2.stop_acquisition()

if __name__ == "__main__":
    start_capture()
