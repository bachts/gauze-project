import jetson.inference
import jetson.utils
import cv2
import numpy as np
import time

# Variables for FPS calculation
timeMark=time.time()
dtFIL=0

# Load Gauze Model
net=jetson.inference.detectNet(argv=['--model=models/1000gauzedataset/ssd-mobilenet.onnx', '--labels=models/1000gauzedataset/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'], threshold=0.1)

# Raspberry Wide Eye Lens is of resolution 2592x1944
width=900 #2592/2.88
height=675 #1944/2.88
flip=2
font=cv2.FONT_HERSHEY_SIMPLEX

# Connect 2 raspberry pi cameras to Jetson
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

    # Show frames in window
    cv2.imshow('comboCam',frame3)
    cv2.moveWindow('comboCam',0,0)

    if cv2.waitKey(1)==ord('b'):
        break
cam.release()
cv2.destroyAllWindows()