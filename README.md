# genieCam

Imaging processing in Python using Aravis and OpenCv


### Installation

This project requires [Aravis](https://github.com/AravisProject/aravis) to run, [OpenCv](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/) with imutils, and [NumPy](https://pypi.org/project/numpy/).



### Task list

- [ ] Camera image aquisition
    - [x] Get camera image with Aravis and process with openCv
    - [ ] Calibrate both cameras, save config and load it.
    - [x] Save images from camera
    - [x] Make panoramic image with images of both cameras
    - [ ] Calculate distance between cameras and object
- [ ] Image processing
    - [x] Convert image to binary to enhance laser lines
    - [x] Apply smooth on image 
    - [x] Retrive lines in image
    - [x] Measure lenght of lines
    - [ ] Calculate pixel size depending on distance of camera
- [ ] Laser work
    - [ ] Calculate distance between laser lines
    - [ ] Calculate laser angle aperture
