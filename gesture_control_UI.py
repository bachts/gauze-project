import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Open the video stream
cap = cv2.VideoCapture(0)

# Create the Tkinter window and label
window = tk.Tk()
label = tk.Label(window)
label.pack()

# Create a label widget to display the count
count_label = tk.Label(window, text="Count: 10", font=("Helvetica", 24))
count_label.pack(pady=10)

count = 10  # Initial count value

def increment():
    global count
    count += 1
    count_label.config(text="Count: {}".format(count))

def decrement():
    global count
    count -= 1
    count_label.config(text="Count: {}".format(count))

def reset_count():
    global count
    count = 0
    count_label.config(text="Count: {}".format(count))

# Create the increment button
button1 = tk.Button(window, text="Increment", command=increment, font=("Helvetica", 16), width=20, bg='grey')
button1.pack(side='left', padx=100)

# Create the decrement button
button2 = tk.Button(window, text="Decrement", command=decrement, font=("Helvetica", 16), width=20, bg='grey')
button2.pack(side='left', padx=100)

# Create the decrement button
button3 = tk.Button(window, text="Reset Count", command=reset_count, font=("Helvetica", 16), width=20, bg='grey')
button3.pack(side='left', padx=100)

def update_frame():
    # Read the next frame from the stream
    ret, frame = cap.read()

    # Convert the frame to a PhotoImage object
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)
    image = ImageTk.PhotoImage(image)

    # Update the label with the new frame
    label.config(image=image)
    label.image = image

    # Schedule the next frame update
    window.after(30, update_frame)


# Start updating the frame
update_frame()

# Run the Tkinter event loop
window.mainloop()
