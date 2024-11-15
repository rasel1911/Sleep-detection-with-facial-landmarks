import cv2
import dlib
from scipy.spatial import distance
import pyautogui

def calculate_EAR(eye):
	A = distance.euclidean(eye[1], eye[5])

	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	#print(A,B,C)
	ear_aspect_ratio = (A+B)/(2.0*C)
	return ear_aspect_ratio
def guirasel():
	pyautogui.press("m")

cap = cv2.VideoCapture(0)
facDec= dlib.get_frontal_face_detector()
DlMark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
x=12
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = facDec(gray)
    for face in faces:

        fmark = DlMark(gray, face)
        leftEye = []
        rightEye = []

        for n in range(36,42):
        	x = fmark.part(n).x
        	y = fmark.part(n).y
        	leftEye.append((x,y))
        	next_point = n+1
        	if n == 41:
        		next_point = 36
        	x2 = fmark.part(next_point).x
        	y2 = fmark.part(next_point).y
        	cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

        for n in range(42,48):
        	x = fmark.part(n).x
        	y = fmark.part(n).y
        	rightEye.append((x,y))
        	next_point = n+1
        	if n == 47:
        		next_point = 42
        	x2 = fmark.part(next_point).x
        	y2 = fmark.part(next_point).y
        	cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

        left_ear = calculate_EAR(leftEye)
        right_ear = calculate_EAR(rightEye)

        EAR = (left_ear+right_ear)/2
        EAR = round(EAR,2)
        if EAR<0.16:
        	cv2.putText(frame,"DROWSY",(20,100), cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),4)
        	cv2.putText(frame,"Are you Sleepy?",(20,400), cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4)
        	print("Drowsy")
        print(EAR)

    cv2.imshow("Are you Sleepy", frame)

    
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()