import cv2
import os
import uuid

width=820
height=616
flip=0
i = 100

IMAGES_PATH = os.path.join('gauzedata', 'images')
cap=cv2.VideoCapture(0,cv2.CAP_GSTREAMER)
#cap = cv2.VideoCapture('nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3280, height=2464, framerate=12/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-0.2 saturation=1.2 ! appsink drop=True')

print("Taking Gauze Images")

while True:
    #read from webcam
    ret, frame = cap.read()

    #Show image
    cv2.imshow('Gauze Data', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('t'):
        imgname = os.path.join(IMAGES_PATH, 'pic'+str(i)+'.'+str(uuid.uuid1())+'.jpg')
        cv2.imwrite(imgname, frame)
        print("Image "+str(i)+ "Taken")
        i+=1

    #break if q key is pressed
    elif cv2.waitKey(10) & 0xFF == ord('q'):
        break
#release webcam
cap.release()
#closes window
cv2.destroyAllWindows()
print("Images Taken")