import cv2

# Setting a default count for testing
current_count = 10

def get_count():
    return current_count


def reset_count():
    global current_count
    current_count = 0


def decrement_count():
    global current_count
    current_count -= 1


def increment_count():
    global current_count
    current_count += 1

# Update the count depending on the gesture_number
def update_count(gesture_number):
    if gesture_number == 1:
        increment_count()
    elif gesture_number == 2:
        decrement_count()
    else:
        reset_count()

# Just a function to display the countdown timer
def countdown_display(curGestureTime: int, gesture_no: int, countdownTime: int = 50):
    rem = countdownTime - curGestureTime

    count_update_string = ""
    if gesture_no == 1:
        count_update_string = "COUNT INCREMENTED"
    elif gesture_no == 2:
        count_update_string = "COUNT DECREMENTED"
    else:
        count_update_string = "COUNT RESET"

    printed_string = f"Hold gesture {gesture_no} for {rem} more ms" if rem > 0 else count_update_string

    cv2.putText(frame, printed_string,
                (60, 60), font, 1, color, 2, cv2.LINE_AA)


def detect_gesture():
    # If m is pressed return 1
    if cv2.waitKey(50) & 0xFF == ord('m'):
        return 1
    # If n is pressed return 2
    elif cv2.waitKey(50) & 0xFF == ord('n'):
        return 2
    # If b is pressed return 3
    elif cv2.waitKey(50) & 0xFF == ord('b'):
        return 3
    # Return 0
    else:
        return 0


# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Set up the text font and color
font = cv2.FONT_HERSHEY_SIMPLEX
color = (255, 255, 255)

# This is a tracker of how many times the bottom while-loop has been run with the gesture having been detected
curGestureTime = 0

# Start looping
while True:

    # Capture frame-by-frame
    ret, frame = cap.read()

    # This is a gesture function. Returns 0 if no gesture detected. Returns 1,2,3 etc depending on gesture number
    gesture = detect_gesture()

    # If gesture is detected
    if gesture != 0:

        # Current time with a gesture held is incremented
        curGestureTime += 1

        # Display
        countdown_display(curGestureTime, gesture, countdownTime=50)

        # If the countdown has reached 0
        if 50-curGestureTime == 0:

            # We update the count depending on the gesture number
            update_count(gesture_number=gesture)
    else:
        # Gesture is no longer detected. Reset count
        curGestureTime = 0

    # Make sure to put the text on every frame
    cv2.putText(frame, f"Gauze Count: {get_count()}",
                (10, 300), font, 1, color, 2, cv2.LINE_AA)

    # Quit the window if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Display the resulting frame
    cv2.imshow('Frame', frame)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
