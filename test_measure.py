import cv2
import numpy as np
import json
import imutils
import sys
import os
import math
import pandas as pd
from sklearn.cluster import KMeans

def start():
    #path='/home/santana/Desktop/genieCam/images/'
    #imgL = cv2.imread(os.path.join(path, 'opencv_frame_left0.tif')) 
    #imgR = cv2.imread(os.path.join(path, 'opencv_frame_right1.tif'))
    img=cv2.imread('teste7.tif') 
    #img2=cv2.imread('opencv_frame_right0.tif') 

    #image = cv2.hconcat([imgL, imgR])

    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,150,150])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    mask = mask0+mask1

    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0

    # or your HSV image, which I *believe* is what you want
    output_hsv = img_hsv.copy()
    output_hsv[np.where(mask==0)] = 0

    cv2.imwrite('maska.png', output_img)
    cv2.imwrite('maska2.png', output_hsv)

    gray = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=30)

    #if exists lines
    if lines is not None:
        for line in lines:
            #get values of each line, start and end
            x1, y1, x2, y2 = line[0]
            if y1==y2:
                #draw the lines in image frame
                cv2.line(output_img, (x1, y1), (x2, y2), (0, 255, 0), 1)

    cv2.imwrite('maska3.png', output_img)



    #cv2.imwrite("concatenated.png", image)

    grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret,thresh_img = cv2.threshold(img,1,255,cv2.THRESH_BINARY)
    ret2,thresh_img2 = cv2.threshold(img,1,255,cv2.THRESH_BINARY)
    ret3,thresh_img3 = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY)
    ret4,thresh_img4 = cv2.threshold(grayscaled,70,255,cv2.THRESH_BINARY)

    # Taking a matrix of size 5 as the kernel
 
    kernel = np.ones((3,3), np.uint8) 
    img_erosion = cv2.erode(thresh_img4, kernel, iterations=1) 
    #ret,thresh_img2 = cv2.threshold(imgR,30,255,cv2.THRESH_BINARY)
    #dst = cv2.GaussianBlur(thresh_img,(5,5),cv2.BORDER_DEFAULT) 
    edges = cv2.Canny(img_erosion, 50, 150)
    cv2.imwrite('left_edges.png',edges)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength = 20, maxLineGap=80)
    edges = cv2.Canny(img_erosion, 50, 150)
    lines2 = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength = 20, maxLineGap=80)

    l=[]
    if lines is not None:
        for line in lines:
            #get values of each line, start and end
            x1, y1, x2, y2 = line[0]
            myradians = math.atan2(y2-y1, x2-x1)
            mydegrees = math.degrees(myradians)
            print(x2)
            #if mydegrees<20 and mydegrees>-20:
                #if x1>1800 and y1>300:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            l.append(line[0])

    data=pd.DataFrame(l)
    #print(data)
    X=np.array(l)
    km = KMeans(n_clusters=10, random_state=0).fit(data)
    cluster_map = data
    #cluster_map['data_index'] = data.index.values
    cluster_map['cluster'] = km.labels_

    for i in range(10):
        data=cluster_map[cluster_map.cluster == i]
        #print(data)
        #print(data[0])
        x1=data[0].min()
        x11=int(data[0].mean())
        #print(data[2])
        x2=data[2].max()
        x22=int(data[2].mean())
        #print(x2-x1)
        lengthP = x2-x1
        length = (x2-x1) *0.006
        print("tamanho em cm", length)
        print("tamanho em pixeis", lengthP)
        y1=int(data[1].mean())
        print(y1)
        y2=int(data[3].mean())
        print(y2)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.line(img, (x11, y1), (x22, y2), (255, 0, 0), 2)



    # if lines2 is not None:
    #     for line in lines2:
    #         #get values of each line, start and end
    #         x1, y1, x2, y2 = line[0]
    #         myradians = math.atan2(y2-y1, x2-x1)
    #         mydegrees = math.degrees(myradians)
    #         #print(mydegrees)
    #         if mydegrees<20 and mydegrees>-20:
    #             if x2>400:
    #                 cv2.line(img2, (x1, y1), (x2, y2), (0, 0, 255), 1)

    cv2.imwrite("Binary_right_test5.png", img)
    cv2.imwrite("Binary_left_test2.png", thresh_img)
    cv2.imwrite("Binary_right_test2.png", thresh_img2)
    cv2.imwrite("Binary_right_test3.png", img_erosion)
    cv2.imwrite("Binary_right_test4.png", thresh_img4)
    #cv2.imwrite("Binary2.png", thresh_img2)
        

    

if __name__ == "__main__":
    start()
