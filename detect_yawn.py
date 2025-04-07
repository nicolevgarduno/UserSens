"""
to run: 
source SensProj/bin/activate
arch -x86_64 python detect_yawn.py

blinking: https://github.com/antoinelame/GazeTracking
"""

import cv2
import time
import numpy as np
import dlib
from scipy.spatial import distance as dist
from imutils import face_utils

# load models
face_model = dlib.get_frontal_face_detector()
landmark_model = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# constants for drowsiness detection
YAWN_THRESH = 80 # minimum mouth opening distance to count a yawn
WARNINGS = 8
ptime = 0
yawn_count = 0
start_time = None

# this calcualtes the distance between the upper and lower lip so that it can be compared to the yawn threshold and detect yawning movemnts
def calc_lip_dist(shape):
    top_lip = np.concatenate((shape[50:53], shape[61:64]))
    bottom_lip = np.concatenate((shape[56:59], shape[65:68]))

    return dist.euclidean(np.mean(top_lip, axis=0), np.mean(bottom_lip, axis=0))

cam = cv2.VideoCapture(0)

while True:
    success, frame = cam.read()
    if not success:
        break
    ctime = time.time()
    fps = int(1/(ctime-ptime))
    primte = ctime

    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 
    faces = face_model(gray_frame)

    for face in faces:
        shapes = landmark_model(gray_frame, face) # gets facial landmarks
        shape = face_utils.shape_to_np(shapes) #converting to array

        # detect yawning
        lip_distance = calc_lip_dist(shape)

        if lip_distance > YAWN_THRESH:
            yawn_count += 1
            cv2.putText(frame, "Yawning detected", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    cv2.imshow("Yawn Detection", frame)

    key = cv2.waitKey(1)
    if key == 27:  # Esc to exit
        break

cam.release()
cv2.destroyAllWindows()

