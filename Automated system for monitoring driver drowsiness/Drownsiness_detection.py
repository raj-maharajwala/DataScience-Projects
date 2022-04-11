from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import winsound
import smtplib
import imghdr
from email.message import EmailMessage
from mss import mss
from PIL import Image
import numpy as np
import os


bounding_box = {'top': 100, 'left': 0, 'width': 400, 'height': 300}

sct = mss()

Sender_Email = "rajmaharajwala_xyz@gmail.com"
Reciever_Email = "rajmaharajwala_pqr@gmail.com"
Password = "**********"

newMessage = EmailMessage()                         
newMessage['Subject'] = "Emergency! Driver is sleeping" 
newMessage['From'] = Sender_Email                   
newMessage['To'] = Reciever_Email                   
newMessage.set_content('Mr. Raj Maharajwala is currently sleeping while driving. Image attached!') 

#with open('C:/Users/asus/Pictures/art.png', 'rb') as f:
#    image_data = f.read()
#    image_type = imghdr.what(f.name)
#    image_name = f.name

#newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
	
thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap=cv2.VideoCapture(0)
flag=0
while True:
	ret, frame=cap.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	subjects = detect(gray, 0)
	for subject in subjects:
		shape = predict(gray, subject)
		shape = face_utils.shape_to_np(shape)#converting to NumPy Array
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR) / 2.0
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, 	(0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		if ear < thresh:
			flag += 1
			print (flag)
			if flag >= frame_check:
				cv2.putText(frame, "****************ALERT!****************", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0 , 255), 2)
				cv2.putText(frame, "****************ALERT!****************", (10,325),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0,  255), 2)
				frequency = 3000  # Set Frequency To 3000 Hertz
				duration = 2000  # Set Duration To 1000 ms == 1 second
				winsound.Beep(frequency, duration)
				sct_img = sct.grab(bounding_box)
				image = cv2.cvtColor(np.array(sct_img),cv2.COLOR_BGR2RGB  )  
				os.remove("image1.png")
				cv2.imwrite("image1.png", image)
				with open("image1.png", 'rb') as f:
					image_data = f.read()
					image_type = imghdr.what(f.name)
					image_name = f.name
				newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
				with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
					winsound.Beep(frequency, duration)
					smtp.login(Sender_Email, Password)              
					smtp.send_message(newMessage)
				
				#print ("Drowsy")
		else:
			flag = 0
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
cv2.destroyAllWindows()
cap.release() 
