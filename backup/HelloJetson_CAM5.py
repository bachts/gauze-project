import jetson.inference
import jetson.utils
import cv2
import numpy as np
import time
import datetime

# Initialise variables for FPS calculation
timeMark=time.time()
dtFIL=0

# Load Gauze Model
net=jetson.inference.detectNet(argv=['--model=models/1000gauzedataset_900by675/ssd-mobilenet.onnx', '--labels=models/1000gauzedataset_900by675/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'], threshold=0.01)

# Raspberry Wide Eye Lens is of resolution 2592x1944
width=900 #2592/2.88
height=675 #1944/2.88
flip=2
font=cv2.FONT_HERSHEY_SIMPLEX

# Connect 2 raspberry pi cameras to Jetson
camSet1='nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=2592, height=1944, framerate=12/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-0.2 saturation=1.2 ! appsink drop=True'
camSet2='nvarguscamerasrc sensor-id=1 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=2592, height=1944, framerate=12/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-0.2 saturation=1.2 ! appsink drop=True'
cam1=cv2.VideoCapture(camSet1)
cam2=cv2.VideoCapture(camSet2)

while True:
    # Initialise counter variables for number of gauzes in Input and Output frames
    countOutput = 0
    countInput = 0

    # Initialise input from the 2 cameras
    _, frame1 = cam1.read()
    _, frame2 = cam2.read()

    # To merge the 2 camera inputs into frame3
    frame3=np.hstack((frame1,frame2))
      
    # Incorporating model detection capabilities with new variable frame4
    frame4 = frame3
    frame4=cv2.cvtColor(frame3,cv2.COLOR_BGR2RGBA).astype(np.float32)
    frame4=jetson.utils.cudaFromNumpy(frame4)

    detections=net.Detect(frame4, width*2, height)
    
    for detect in detections:
        #print(detect)
        # Extract all variables from detect variable
        ID=detect.ClassID
        confidence=(detect.Confidence)*100 #confidence is changed from 0.0000000 format to percentage format
        confidence=round(confidence,1) #confidence is rounded to 1 dp
        left=detect.Left
        top=detect.Top
        right=detect.Right
        bottom=detect.Bottom
        area=detect.Area
        center=detect.Center
        item=net.GetClassDesc(ID)
        #print(item,top,left,bottom,right) 

        # Draw bounding box around the gauze and show its confidence rating
        cv2.rectangle(frame3, (int(left), int(bottom)), (int(right), int(top)), (0,255,0), 2) #draw rectangle around gauze
        cv2.putText(frame3,'Gauze '+str(confidence)+'%',(int(left),int(top)),font,1,(0,255,255),2) #write "gauze" and confidence above rectangle

        # Count the number of gauzes in Input & Output within this current frame
        if center[0] > width:
            countOutput += 1
        if center[0] < width:
            countInput += 1

    print("Input: ", countInput, " Output: ", countOutput)

    # Create a bordered frame so we have space to display additional information for our system
    #cv2.imshow('comboCam',frame3)
    #cv2.moveWindow('comboCam',0,0)
    borderedFrame = cv2.copyMakeBorder(frame3,0,350,0,0,cv2.BORDER_CONSTANT,value=[0,0,0])
    #Syntax: cv2.copyMakeBorder(src, top, bottom, left, right, borderType, value)

    # To get FPS and mark FPS windows bar
    dt=time.time()-timeMark
    timeMark=time.time()
    dtFIL=.9*dtFIL + .1*dt
    fps=1/dtFIL
    cv2.putText(borderedFrame,'FPS:'+str(round(fps,1)),(width-65,30+height),font,1,(200,200,200),2)

    # Mark date and time in borderedFrame
    d = datetime.datetime.now()
    current_time = d - datetime.timedelta(microseconds=d.microsecond)
    cv2.putText(borderedFrame,str(current_time),(width-180,60+height),font,1,(200,200,200),2)

    # Mark "Input" & "Output" in borderedFrame for identification purposes
    cv2.putText(borderedFrame,'INPUT',(int(width/2)-150,50+height),font,2,(0,255,0),3)
    cv2.putText(borderedFrame,'OUTPUT',(int(width*1.5)-130,50+height),font,2,(0,0,255),3)

    # Mark all input & output relevant counters in borderedFrame
    cv2.putText(borderedFrame,"Detected Input: "+str(10),(38,120+height),font,1.5,(255,255,255),2)
    cv2.putText(borderedFrame,"Confirmed Input: "+str(100),(5,170+height),font,1.5,(255,255,255),2)
    cv2.putText(borderedFrame,"Detected Output: "+str(10),(width,120+height),font,1.5,(255,255,255),2)
    cv2.putText(borderedFrame,"Gauze Left: "+str(90),(130+width,170+height),font,1.5,(255,255,255),2)
    cv2.putText(borderedFrame,"Gauze Kept: "+str(10),(115+width,220+height),font,1.5,(255,255,255),2)
    # PSEUDO NUMBERS USED FOR NOW. Variable to replace the pseudo number in str(__)

    # Show borderedFrame window with iGauze System Title
    cv2.imshow("iGauze System", borderedFrame)
    cv2.moveWindow('iGauze System',0,0)

    if cv2.waitKey(1)==ord('b'):
        break
cam.release()
cv2.destroyAllWindows()