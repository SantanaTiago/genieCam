import cv2
import numpy as np
import os

window_name = ('Sobel Demo - Simple Edge Detector')
scale = 1
delta = 0
ddepth = cv2.CV_16S


path='/home/santana/Desktop/genieCam/images/'

# Load the image
#src=cv2.imread('opencv_frame_right0.tif')
img_name='opencv_frame_right0.tif'
src=cv2.imread(os.path.join(path, img_name))
src = cv2.GaussianBlur(src, (3, 3), 0)

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
# Gradient-Y
# grad_y = cv.Scharr(gray,ddepth,0,1)
grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)


abs_grad_x = cv2.convertScaleAbs(grad_x)
abs_grad_y = cv2.convertScaleAbs(grad_y)


grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)


cv2.imshow(window_name, grad)
cv2.imwrite('sobel.png',grad)
cv2.waitKey(0)
