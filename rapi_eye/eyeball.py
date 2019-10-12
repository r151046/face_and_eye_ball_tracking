import numpy as np
import cv2
#ser = serial.Serial('/dev/ttyACM0',9600)
face_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
camera=cv2.VideoCapture(1)
k=0
fwd=0
left=0
rgt=0
stop=0
pos=0
sl=0
arr=[0,0,0,0]
while True:
	if ( k < 5):
		ret, frame = camera.read()
		roi=frame
		frame=cv2.flip(frame,1)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		if(len(faces)!=0):
				for (x,y,w,h) in faces:
					iris_w=int(x+float(w/2))
					iris_h=int(y+float(h/2))
					roi=gray[iris_h-20:iris_h+20,iris_w-20:iris_w+20]
					cv2.imshow("fray",roi)
					roi = cv2.equalizeHist(roi)
					cv2.imshow("eqahist",roi)
					l=roi.shape[0]
					h=roi.shape[1]
					thres=cv2.inRange(roi,20,750)
					cv2.imshow("thresh",thres)
					kernel = np.ones((3,3),np.uint8)
					dilation = cv2.dilate(thres,kernel,iterations = 2)
					erosion = cv2.erode(dilation,kernel,iterations = 3)
					if (erosion[int(h/2)][int(l/2)] == 0 or erosion[int(h/2)+2][int(l/2)+2] == 0 or erosion[int(h/2)-2][int(l/2)-2] == 0):
						arr[0]=arr[0]+1
					elif(erosion[int(h/2)][10] == 0 or erosion[int(h/2)+5][10] == 0 or erosion[int(h/2)-5][10] == 0):
						arr[1]=arr[1]+1
					elif(erosion[int(h/2)][l-10] == 0 or erosion[int(h/2)-5][l-10] == 0 or erosion[int(h/2)+5][l-10] == 0):
						arr[2]=arr[2]+1
				cv2.imshow("roi",erosion)
				cv2.imshow('Iris Detector',frame)
				if cv2.waitKey(30)==27 & 0xff:
					break
		else:
			arr[3]=arr[3]+1

	if(k==5):
		k=0
		maximum=max(arr)
		value = arr.index(maximum)
		arr=[0,0,0,0]
		if(value == 0 and pos!='f'):
			pos='f'
			print("f")
		elif(value == 1 and pos!='le'):
			pos='le'
			print("l")
		elif(value == 2 and pos!='ri'):
			pos='ri'
			print("r")
		elif(value == 3 and pos!='st'):
			pos='st'
			print("s")
	else:
		k=k+1
camera.release()
cv2.destroyAllWindows()
