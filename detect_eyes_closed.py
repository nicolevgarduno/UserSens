''''
environment:
source SensProj/bin/activate

to run:
arch -x86_64 python detect_eyes_closed.py
'''


import cv2
import dlib
import pyttsx3
from scipy.spatial import distance
import time
 
engine = pyttsx3.init()
cap = cv2.VideoCapture(0)
 
# mapping face to get eyes
face_detector = dlib.get_frontal_face_detector()
 
# file for predicting landmarks on face
dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
 
# constants for eye aspect ratio
EYES_AR_THRESH = 0.13 #thresh for eye closure
CLOSE_EYE_TIME_LIM = 10 # seconds eyes can remain closed until it's concerning
WARNINGS = 5 # before it notifies that you are unsuaully sleepy
start_time = None #tracks when eyes first close
drowsy_count = 0# counts consecutive drowsiness warnings
alert_text = ""    


# calculating aspect ratio for eyes using euclidean distance function
def Detect_Eye(eye):
    poi_A = distance.euclidean(eye[1], eye[5])
    poi_B = distance.euclidean(eye[2], eye[4])
    poi_C = distance.euclidean(eye[0], eye[3])
    aspect_ratio_Eye = (poi_A+poi_B)/(2*poi_C)
    return aspect_ratio_Eye
 
# loop to run until killed
while True:
    ret, frame = cap.read()
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray_scale)
    eyes_closed = False

    for face in faces:
        face_landmarks = dlib_facelandmark(gray_scale, face)
        leftEye, rightEye = [], [] 
 
        # point allocation for eyes from the .dat file
        for n in range(42, 48):
            x,y = face_landmarks.part(n).x, face_landmarks.part(n).y
            rightEye.append((x, y))
        for n in range(36, 42):
            x,y = face_landmarks.part(n).x, face_landmarks.part(n).y
            leftEye.append((x, y))
 
        # calculating aspect ratio for eyes 
        right_Eye,left_Eye = Detect_Eye(rightEye), Detect_Eye(leftEye)
        Eye_Rat = round((left_Eye+right_Eye)/2, 2)

        # determining if eyes closed
        if Eye_Rat < EYES_AR_THRESH:
            if start_time is None:
                start_time = time.time() # starting timer when eyes first close
            eyes_closed = True
            
        else:
            start_time = None # reset time when eyes are open
            drowsy_count = 0 # reset consective count

    # checking if eyes have been clsoed for too long
    if eyes_closed and start_time is not None:
        elapsed_time = time.time() - start_time
        print(f"Eyes closed for: {elapsed_time:.2f} seconds")  #debugging
        
        if elapsed_time >= CLOSE_EYE_TIME_LIM: 
            #cv2.putText(frame, "WAKE UP!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            print("ALERT: WAKE UP!")  
            alert_text = "WAKE UP!"
            alert_start_time = time.time()
            start_time = None  # reset timer
            drowsy_count += 1  
            
    if drowsy_count > WARNINGS:
        # cv2.putText(frame, "You keep falling asleep. drink coffee", (50,450), cv2.FONT_HERSHEY_CIMPLEX, 1, (0, 255, 255), 3)
        print("ALERT: You keep falling asleep. Drink coffee.")  
        alert_text = "You keep falling asleep. Drink coffee!"
        alert_start_time = time.time()
        engine.say("You keep falling asleep. Drink coffee!")
        engine.runAndWait()
        drowsy_count = 0

    # clears after 5 seconds
    if alert_text and alert_start_time is not None:
        if time.time() - alert_start_time >= 5:
            alert_text = ""
            alert_start_time = None  # Reset timer  

     # always draw the alert text if it's active  
    if alert_text:
        cv2.putText(frame, alert_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Drowsiness Detector", frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()