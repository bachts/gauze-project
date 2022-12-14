# Reference: https://toptechboy.com/jetson-xavier-nx-lesson-8-controlling-dual-pan-tilt-raspberry-pi-cameras/
# Bare code to run 2 cameras using cv2

import cv2
import numpy as np
import time
print(cv2.__version__)


timeMark=time.time()
dtFIL=0

# Raspberry Wide Eye Lens is of resolution 2592x1944
width=900 #2592/2.88
height=675 #1944/2.88
flip=2
font=cv2.FONT_HERSHEY_SIMPLEX
camSet1='nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-0.2 saturation=1.2 ! appsink drop=True'
camSet2='nvarguscamerasrc sensor-id=1 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-0.2 saturation=1.2 ! appsink drop=True'
 
cam1=cv2.VideoCapture(camSet1)
cam2=cv2.VideoCapture(camSet2)

while True:
    _, frame1 = cam1.read()
    _, frame2 = cam2.read()

    # To merge the 2 frames into 1 new frame
    frame3=np.hstack((frame1,frame2))

    # To get FPS
    dt=time.time()-timeMark
    timeMark=time.time()
    dtFIL=.9*dtFIL + .1*dt
    fps=1/dtFIL
    cv2.rectangle(frame3,(0,0),(150,40),(0,0,255),-1)
    cv2.putText(frame3,'fps: '+str(round(fps,1)),(0,30),font,1,(0,255,255),2)
    print('fps: ',fps)

    cv2.imshow('comboCam',frame3)
    cv2.moveWindow('comboCam',0,0)

    if cv2.waitKey(1)==ord('b'):
        break
cam.release()
cv2.destroyAllWindows()