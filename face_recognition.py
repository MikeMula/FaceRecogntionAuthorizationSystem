import cv2
import numpy as np
import os
import time
import pyttsx3
import arduino

engine = pyttsx3.init()
engine.setProperty('volume',1.0)
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[33].id)
engine.setProperty('rate', 180)

#
# First time user should enroll first using enroll.py
#

# Match user to users in our database; return True if found, false otherwise
def matching(DATABASE):

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX

    id = 0
    N = 0 # number of times user is recognized
    capture_duration = 2.2 # duration in seconds of video capture

    # Start video capture
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 500)
    video_capture.set(4, 500)

    # minimum window size to be recognized as a face
    minW = 0.1*video_capture.get(3)
    minH = 0.1*video_capture.get(4)

    start_time = time.time()
    while( int(time.time() - start_time) < capture_duration ):
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_locations = face_detector.detectMultiScale(
            gray,
            scaleFactor  = 1.3,
            minNeighbors = 5,
            minSize      = (int(minW), int(minH))
        )

        for (x,y,w,h) in face_locations:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            confidence = round(100-confidence)

            # perfect match if confidence == 100
            if(confidence >= 60):
                N += 1
                id = DATABASE[id]
                confidence = f" {confidence}%"
            else:
                id = 'unknown'
                confidence = f" {confidence}%"
            
            # display results
            cv2.putText(
                frame,
                str(id),
                (x+5,y-5),
                font,
                1,
                (255,255,255),
                2
            )
            cv2.putText(
                frame,
                str(confidence),
                (x+5,y+h-5),
                font,
                1,
                (255,255,0),
                1
            )

        cv2.imshow('camera', frame)

        # Press 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Clean up on exit
    video_capture.release()
    cv2.destroyAllWindows()

    if N >= 5:
        return id
    elif N == 0:
        return  id
    else:
        return None
    


# Grant a user access
def grantAccess(name):
    arduino.openDoor('open')
    engine.say('Access granted!')
    engine.say(f'Welcome home {name}')
    engine.runAndWait()

# Deny a user access
def denyAccess():
    engine.say('Access Denied!')
    engine.runAndWait()

def faceNotRecognized():
    engine.say('No face was found. Please try again!')
    engine.runAndWait()

def main():
    
    print("PROGRAM STARTING")
    # get the user DATABASE
    DATABASE = dict()
    fd = open('users.txt', 'r')

    DATABASE[0] = 'unknown'
    for line in fd:
        line = line.split()
        DATABASE[int(line[1])] = line[0] 
    fd.close()
    
    # print(DATABASE)
    name =  matching(DATABASE)

    if name == None:
        faceNotRecognized()
    elif( name != 'unknown' and name != 0):
        grantAccess(name)
    else:
        denyAccess()

    print("Match: ", name)




if __name__ == '__main__':
    main()