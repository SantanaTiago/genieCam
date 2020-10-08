import sys
import time
import cv2
from aravis import Camera
from gi.repository import Aravis


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("None", "null"):
            cam = Camera(None)
        else:
            cam = Camera('Teledyne DALSA-Nano-C2420-S1138840')
    else:
        cam = Camera('Teledyne DALSA-Nano-C2420-S1138840')

    try:
        cam.set_region (0,0,2464,2056)
        cam.set_frame_rate (10.0)
        cam.set_pixel_format (Aravis.PIXEL_FORMAT_BAYER_BG_8)
        cam.start_acquisition_continuous()
        cv2.namedWindow('capture', flags=0)

        count = 0
        while True:
            count += 1
            print("frame nb: ", count)
            frame = cam.pop_frame()
            print("shape: ", frame.shape)
            print(time.time())
            if not 0 in frame.shape:
                cv2.imshow("capture", frame)
                cv2.waitKey(1)
    finally:
        cam.stop_acquisition()
