# First version with Wireless Connected Raspberry Pi Camera
# CAM12 is for NTUitive Presentation purposes.
# NMS set at 0.5 for detectNet.h file 

import jetson.inference
import jetson.utils
import cv2
import numpy as np
import time
import datetime
import RPi.GPIO as GPIO

# INITIALISE GLOBAL VARIABLES 
# Initialise Pins for GPIO Control```
GPIO.setmode(GPIO.BOARD)
inPin1 = 29
inPin2 = 31
inPin3 = 33
inPin4 = 35
inPin5 = 32
inPin6 = 36
inPin7 = 38
inPin8 = 40

GPIO.setup(inPin1, GPIO.IN)
GPIO.setup(inPin2, GPIO.IN)
GPIO.setup(inPin3, GPIO.IN)
GPIO.setup(inPin4, GPIO.IN)
GPIO.setup(inPin5, GPIO.IN)
GPIO.setup(inPin6, GPIO.IN)
GPIO.setup(inPin7, GPIO.IN)
GPIO.setup(inPin8, GPIO.IN)

# Initialise global variables for count variables 
countChangeInput = 10
countChangeOutput = 10
countConfirmedInput = 10
countGauzeLeft = 0
countGauzeKept = 0
inputTimekeeper = 0 #for implementing 0.5 second lag between each button press to prevent accidental double pressing
outputTimekeeper = 0

# Initialise global variables for FPS calculation
timeMark=time.time()
dtFIL=0

# Initialise History Arrays to record all Users' interactions with system
historyInput = [" "," "]
historyOutput = [" "," "]




# INITIALISE COMPUTER VISION SEGMENT
# Load own custom Gauze Model
net=jetson.inference.detectNet(argv=['--model=models/gauzecombine/ssd-mobilenet.onnx', '--labels=models/gauzecombine/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--threshold=0.3'])
# Load pre-trained detectnet to replace Gauze Model while doing prototyping. Gauze model takes too long to load.
#net=jetson.inference.detectNet()

# Raspberry Pi Camera V2 is of resolution 3280x2464
width=900 #3280/3.64
height=675 #2464/3.64
#Syntax for flip-method -- 0:none, 1:counter-clockwise 90 degrees, 2:rotate-180, 3:clockwise 90 degrees, 4:horizontal-flip, 5:upper-right-diagonal, 6:vertical-flip, 7:upper-left-diagonal
flip=2 #For Jetson Connected Camera
flip_pi=0 #For Raspberry Pi Connected Camera
font=cv2.FONT_HERSHEY_SIMPLEX

# Connect Raspberry Pi Camera to Cam0 slot on Jetson Xavier NX. Thats why sensor-id=0. If using Cam1 instead, change to sensor-id=1 (refer older codes for execution)
# Ensure JetsonHotspot is turned on, with Raspberry Pi connected to it and the Raspberry Pi's IP address is accurate for host=10.42.0232
camSet1=' tcpclientsrc host=10.42.0.232 port=8554 ! gdpdepay ! rtph264depay ! h264parse ! nvv4l2decoder  ! nvvidconv flip-method='+str(flip_pi)+' ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw, width='+str(width)+', height='+str(height)+',format=BGR ! appsink  drop=true sync=false '
camSet2='nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3280, height=2464, framerate=12/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-0.2 saturation=1.2 ! appsink drop=True'

cam1=cv2.VideoCapture(1)#camSet1)
cam2=cv2.VideoCapture(camSet2)

while True:
    # INITIALISE LOCAL VARIABLES
    # Initialise counter variables for detected number of gauzes in Input and Output frames
    # Reset them to 0 at the start of every loop
    countDetectedInput = 0
    countDetectedOutput = 0





    # COMPUTER VISION SEGMENT
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
            countDetectedOutput += 1
        if center[0] < width:
            countDetectedInput += 1

    #print("Input: ", countDetectedInput, " Output: ", countDetectedOutput)

    # Create a bordered frame so we have space to display additional information for our system
    #cv2.imshow('comboCam',frame3)
    #cv2.moveWindow('comboCam',0,0)
    borderedFrame = cv2.copyMakeBorder(frame3,0,350,0,0,cv2.BORDER_CONSTANT,value=[0,0,0])
    #Syntax: cv2.copyMakeBorder(src, top, bottom, left, right, borderType, value)





    # USER INTERACTION SEGMENT
    #Link to global variable outside of loop
    countConfirmedInput
    countGauzeKept
    countGauzeLeft
    countChangeInput
    countChangeOutput

    # Date and Time Calculations
    d = datetime.datetime.now()
    current_time = d - datetime.timedelta(microseconds=d.microsecond)

    # GPIO Buttons Logic
    inPin1_INPUT=GPIO.input(inPin1)
    if inPin1_INPUT == 1 and (inputTimekeeper+0.5)<time.time():
        inputTimekeeper=time.time()
        countChangeInput += 1

    inPin2_INPUT=GPIO.input(inPin2)
    if inPin2_INPUT == 1 and (inputTimekeeper+0.5)<time.time():
        inputTimekeeper=time.time()
        countChangeInput -= 1
    
    inPin3_INPUT=GPIO.input(inPin3)
    if inPin3_INPUT == 1 and (inputTimekeeper+0.5)<time.time():
        #print("countConfirmedInput = ",str(countConfirmedInput))
        inputTimekeeper=time.time()
        countConfirmedInput += countChangeInput  
        historyInput.append("+"+str(countChangeInput)+" "+str(current_time))
        countChangeInput = 10 #Reset the variable that changes our confirmed input to default 10

    inPin4_INPUT=GPIO.input(inPin4)
    if inPin4_INPUT == 1 and (inputTimekeeper+0.5)<time.time():
        #print("countConfirmedInput = ",str(countConfirmedInput))
        inputTimekeeper=time.time()
        countConfirmedInput -= countChangeInput  
        historyInput.append("-"+str(countChangeInput)+" "+str(current_time))
        countChangeInput = 10 #Reset the variable that changes our confirmed input to default 10


    inPin5_OUTPUT=GPIO.input(inPin5)
    if inPin5_OUTPUT == 1 and (outputTimekeeper+0.5)<time.time():
        outputTimekeeper=time.time()
        countChangeOutput += 1

    inPin6_OUTPUT=GPIO.input(inPin6)
    if inPin6_OUTPUT == 1 and (outputTimekeeper+0.5)<time.time():
        outputTimekeeper=time.time()
        countChangeOutput -= 1
    
    inPin7_OUTPUT=GPIO.input(inPin7)
    if inPin7_OUTPUT == 1 and (outputTimekeeper+0.5)<time.time():
        #print("countGauzeKept = ",str(countGauzeKept))
        outputTimekeeper=time.time()
        countGauzeKept += countChangeOutput 
        historyOutput.append("+"+str(countChangeOutput)+" "+str(current_time))
        countChangeOutput = 10 #Reset the variable that changes our confirmed output to default 10

    inPin8_OUTPUT=GPIO.input(inPin8)
    if inPin8_OUTPUT == 1 and (outputTimekeeper+0.5)<time.time():
        #print("countGauzeKept = ",str(countGauzeKept))
        outputTimekeeper=time.time()
        countGauzeKept -= countChangeOutput 
        historyOutput.append("-"+str(countChangeOutput)+" "+str(current_time))
        countChangeOutput = 10 #Reset the variable that changes our confirmed output to default 10






    # Count Logic for variables to be displayed
    countGauzeIn = countConfirmedInput - countDetectedInput
    countGauzeLeft = countGauzeKept + countDetectedOutput
    countGauzeInPlay = countGauzeIn - countGauzeLeft





    
    # USER INTERFACE SEGMENT
    # To get FPS and mark FPS windows bar
    dt=time.time()-timeMark
    timeMark=time.time()
    dtFIL=.9*dtFIL + .1*dt
    fps=1/dtFIL
    cv2.putText(borderedFrame,'FPS:'+str(round(fps,1)),(width-65,30+height),font,1,(180,180,180),2)

    # Mark date and time in borderedFrame
    cv2.putText(borderedFrame,str(current_time),(width-180,60+height),font,1,(180,180,180),2)

    # Mark "Input" & "Output" in borderedFrame for identification purposes
#    cv2.putText(borderedFrame,'INPUT',(int(width/2)-150,50+height),font,2,(0,255,0),3)
#    cv2.putText(borderedFrame,'OUTPUT',(int(width*1.5)-130,50+height),font,2,(0,0,255),3)

    cv2.putText(borderedFrame,'Gauze In: '+str(countGauzeIn),(int(width/2)-350,50+height),font,2,(150,150,150),3)
    cv2.putText(borderedFrame,'Gauze Out: '+str(countGauzeLeft),(int(width*1.5)-80,50+height),font,2,(150,150,150),3)
    cv2.putText(borderedFrame,"Gauze In Play: ",(width-250,120+height),font,2,(0,255,255),5)
    cv2.putText(borderedFrame, str(countGauzeInPlay),(width-90,250+height),font,5,(0,255,255),10)
    

    # Mark when countChangeInput != 0 or countChangeOutput != 0
    if countChangeInput != 10:
        cv2.putText(borderedFrame,str(countChangeInput),(int(width/2)-130,int(height/2)+100),font,6,(0,0,0),14)
    if countChangeOutput != 10:
        cv2.putText(borderedFrame,str(countChangeOutput),(int(1.5*width)-130,int(height/2)+100),font,6,(0,0,0),14)

    # Mark latest 2 entries of recorded users' actions in borderedFrame
    cv2.putText(borderedFrame,"History: "+str(historyInput[-1]),(5,290+height),font,1,(180,180,180),2)
    cv2.putText(borderedFrame,str(historyInput[-2]),(133+5,320+height),font,1,(180,180,180),2)
    cv2.putText(borderedFrame,"History: "+str(historyOutput[-1]),(300+width,290+height),font,1,(180,180,180),2)
    cv2.putText(borderedFrame,str(historyOutput[-2]),(300+133+width,320+height),font,1,(180,180,180),2)

    # Show borderedFrame window with iGauze System Title
    cv2.imshow("iGauze System", borderedFrame)
    cv2.moveWindow('iGauze System',0,0)

    if cv2.waitKey(1)==ord('b'):
        break

cam1.release()
cam2.release()
cv2.destroyAllWindows()