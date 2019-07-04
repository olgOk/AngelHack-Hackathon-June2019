import numpy as np
import cv2
import boto3
import sys
import json

cap = cv2.VideoCapture(0)
rekog_client = boto3.client("rekognition")

while(cap.isOpened()):
	success, image = cap.read()
	cnt = 0
	while success:
		success, frame = cap.read()
		if success:
			scaled_frame = frame#cv2.resize(frame, (int(width * scale_fractor), int(height * scaled_factor)))

			rval, buffer = cv2.imencode('.jpg', scaled_frame)
			img_bytes = bytearray(buffer)
			response = rekog_client.detect_faces(Image={'Bytes': img_bytes}, Attributes=['ALL'])
			#display(frame, response)
			print(response)

cap.release()
cv2.destroyAllWindows()
