# This is to test if the camera is working
import cv2
print(cv2.__version__)
width=900 #3280/3.64
height=675 #2464/3.64
flip=2
camSet1='nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3280, height=2464, framerate=12/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-0.2 saturation=1.2 ! appsink drop=True'
cam=cv2.VideoCapture(camSet1)
while True:
    _,frame = cam.read()
    cv2.imshow('myCam', frame)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows