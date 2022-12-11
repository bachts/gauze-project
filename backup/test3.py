import cv2


print(cv2.getBuildInformation())

#connect to a webcam
cap = cv2.VideoCapture(1)

#loop through every frame until webcam is closed
while cap.isOpened():
    #read from webcam
    ret, frame = cap.read()

    #Show image
    cv2.imshow('Webcam',frame)

    #break if q key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#release webcam
cap.release()
#closes window
cv2.destroyAllWindows()