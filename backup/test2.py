import sys
import cv2

def read_cam():
    cap=cv2.VideoCapture(0,cv2.CAP_GSTREAMER)
    #cap = cv2.VideoCapture('nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3280, height=2464, framerate=12/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-0.2 saturation=1.2 ! appsink drop=True')
    if cap.isOpened():
        cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
        while True:
            ret_val, frame = cap.read()
            cv2.imshow('demo',frame)
            cv2.waitKey(10)
    else:
     print ("camera open failed")

    cv2.destroyAllWindows()


if __name__ == '__main__':
    read_cam()
    #"nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !  appsink"