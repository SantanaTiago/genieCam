import cv2
import numpy as np 
import glob
from tqdm import tqdm
import PIL.ExifTags
import PIL.Image
import os
import json


def camera_calibration_left():
	#============================================
	# Camera calibration
	#============================================

	#Define size of chessboard target. 

	chessboard_size = (9,6)

	#Define arrays to save detected points
	obj_points_l = [] #3D points in real world space 
	img_points_l = [] #3D points in image plane

	#Prepare grid and points to display

	objp = np.zeros((np.prod(chessboard_size),3),dtype=np.float32)


	objp[:,:2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1,2)

	#read images

	calibration_paths = glob.glob('./images_cal_left/*')

	#Iterate over images to find intrinsic matrix
	for image_path in tqdm(calibration_paths):

		#Load image
		image = cv2.imread(image_path)
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		print("Image loaded, Analizying...")
		#find chessboard corners
		#ret,corners = cv2.findCirclesGrid(gray_image, chessboard_size, None, flags = cv2.CALIB_CB_SYMMETRIC_GRID)
		ret, corners = cv2.findChessboardCorners(gray_image, chessboard_size,None)

		if ret == True:
			print("Chessboard detected!")
			print(image_path)
			#define criteria for subpixel accuracy
			criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
			#refine corner location (to subpixel accuracy) based on criteria.
			cv2.cornerSubPix(gray_image, corners, (9,6), (-1,-1), criteria)
			obj_points_l.append(objp)
			img_points_l.append(corners)

	path='/home/santana/Desktop/genieCam/images_cal_left/'
	img = cv2.imread(os.path.join(path, 'opencv_frame_left2.tif')) 
	gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points_l, img_points_l, gray_image.shape[:2], None, None)
	
	"""Save camera calibration parameters in json file."""
	data = {
		"camera_matrix": mtx.tolist(),
		"dist_coeff": dist.tolist(),
		}
	with open('cal_file_left', "w") as file:
		json.dump(data, file)


def camera_calibration_right():
	#============================================
	# Camera calibration
	#============================================

	#Define size of chessboard target. 
	
	chessboard_size = (9,6)

	#Define arrays to save detected points
	obj_points = [] #3D points in real world space 
	img_points = [] #3D points in image plane

	#Prepare grid and points to display

	objp = np.zeros((np.prod(chessboard_size),3),dtype=np.float32)


	objp[:,:2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1,2)

	#read images

	calibration_paths = glob.glob('./images_cal_right/*')

	#Iterate over images to find intrinsic matrix
	for image_path in tqdm(calibration_paths):

		#Load image
		image = cv2.imread(image_path)
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		print("Image loaded, Analizying...")
		#find chessboard corners
		#ret,corners = cv2.findCirclesGrid(gray_image, chessboard_size, None, flags = cv2.CALIB_CB_SYMMETRIC_GRID)
		ret, corners = cv2.findChessboardCorners(gray_image, chessboard_size,None)

		if ret == True:
			print("Chessboard detected!")
			print(image_path)
			#define criteria for subpixel accuracy
			criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
			#refine corner location (to subpixel accuracy) based on criteria.
			cv2.cornerSubPix(gray_image, corners, (9,6), (-1,-1), criteria)
			obj_points.append(objp)
			img_points.append(corners)

	path='/home/santana/Desktop/genieCam/images_cal_right/'
	img = cv2.imread(os.path.join(path, 'opencv_frame_right2.tif')) 
	gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray_image.shape[::-1], None, None)


	"""Save camera calibration parameters in json file."""
	data = {
		"camera_matrix": mtx.tolist(),
		"dist_coeff": dist.tolist(),
		}
	with open('cal_file_right', "w") as file:
		json.dump(data, file)

def begin():
	camera_calibration_left()
	camera_calibration_right()

if __name__ == "__main__":
    begin()
