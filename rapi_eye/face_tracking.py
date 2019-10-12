import numpy as np
import cv2
import matplotlib.pyplot as plt
boxScale=1
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
array=[]
cap = cv2.VideoCapture(1)
s=0
while 1:
	ret, img = cap.read()
	xx,yx,zx=img.shape
	acenter=[int(yx/2),int(xx/2)]
	cv2.line(img,(acenter[0],acenter[1]+300),(acenter[0],acenter[1]-300),(0,255,255),2)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	if(len(faces)!=0):
		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			roi_color = img[y:y+h, x:x+w]
			center1=[(int((x+(x+w))/2)),(int((y+(y+h))/2))]
			cv2.line(img,(center1[0],center1[1]+50),(center1[0],center1[1]-50),(255,255,255),2)
			eyes = eye_cascade.detectMultiScale(roi_color)
			for (ex,ey,ew,eh) in eyes:
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	
		if(center1[0] > acenter[0]-40):
			if(s!='l'):
				print('left')
			s='l'
		if(center1[0] >= acenter[0]-40 and center1[0] <= acenter[0]+40):
			if(s!='c'):
				print('forward')
			s='c'
		if(center1[0] < acenter[1]+40):
			if(s!='r'):
				print('right')
			s='r'
	else:
		if(s!='st'):
			print('stop')
		s='st'
	
	cv2.imshow('face',img)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()
