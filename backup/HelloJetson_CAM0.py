# This program is not within the Docker environment
# Run this program via Terminal to ensure stability. VS Code may crash.
# Original code to run 2 cameras

import jetson.inference
import jetson.utils
import datetime

net1 = jetson.inference.detectNet(argv=['--model=models/1000gauzedataset/ssd-mobilenet.onnx', '--labels=models/1000gauzedataset/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'], threshold=0.3)
camera1 = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
camera2 = jetson.utils.videoSource("csi://1")      # '/dev/video0' for V4L2
display1 = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
display2 = jetson.utils.videoOutput("display://1") # 'my_video.mp4' for file

while display1.IsStreaming():
	img1 = camera1.Capture()
	detections1 = net1.Detect(img1)
	display1.Render(img1)
	display1.SetStatus("Input Camera 0 | Network {:.0f} FPS".format(display1.GetFrameRate()))

	img2 = camera2.Capture()
	detections2 = net1.Detect(img2)
	display2.Render(img2)
	display2.SetStatus("Output Camera 1 | Network {:.0f} FPS".format(net1.GetNetworkFPS()))

	print(datetime.datetime.now())