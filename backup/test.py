import cv2 
import numpy as np
print(cv2.__version__)
width=820
height=616
flip=0
camSet= 'nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3280, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-0.2 saturation=1.2 ! appsink drop=True'
#camSet ='v4l2src device=/dev/video1 ! video/x-raw,width='+str(width)+',height='+str(height)+',framerate=24/1 ! videoconvert ! appsink'
cam=cv2.VideoCapture(camSet,cv2.CAP_GSTREAMER)
#cam.open()
print (cv2.getBuildInformation())
if not cam.isOpened():
    print('cannot open camera')
    exit()
while True:
    ret, frame = cam.read()
    if not ret:
        print('cannot receive frame')
        break
    cv2.imshow('myCam',frame)
    cv2.moveWindow('myCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

#gst-launch-1.0 nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=1 ! 'video/x-raw(memory:NVMM), width=3280, height=2464, framerate=21/1,format=NV12' ! nvvidconv flip-method=0 ! 'video/x-raw, width=968, height=616, format=BGRx' ! videoconvert! appsink nvvidconv ! nvegltransform ! nveglglessink -e
#gst-launch-1.0 nvarguscamerasrc sensor_mode=0 ! 'video/x-raw(memory:NVMM),width=3820, height=2464, framerate=21/1, format=NV12' ! nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=616' ! nvvidconv ! nvegltransform ! nveglglessink -e