import cv2
import os
import uuid
import numpy as np 
from PIL import Image

NUM_OF_SAMPLES = 25

#
# Register a user into our database
def enroll(name, face_detector):

    # Create unique ID for a user
    ID = uuid.uuid4().int & (1<<32)-1
    
    # Get a reference to a webcam
    video_capture = cv2.VideoCapture(0)

    # Set size of video window
    video_capture.set(3, 500)
    video_capture.set(4, 500)

    N = 0
    while True:
        ret, frame     = video_capture.read()
        gray_scale     = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to grayscale image
        face_locations = face_detector.detectMultiScale(gray_scale, 1.3, 5)

        for (x, y, w, h) in face_locations:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
            N += 1
            # Save the image to our dataset
            cv2.imwrite('./dataset/user.' + str(ID) + '.' + str(N) + '.jpg', gray_scale[y:y+h,x:x+w])
            cv2.imshow('image', frame)

        # Press 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if N >= NUM_OF_SAMPLES:
            break

    # Insert user into user database
    fp = open('users.txt', 'a')
    fp.write(name + '   ' + str(ID) + '\n')
    fp.close()

    # clean up on exit
    video_capture.release()
    cv2.destroyAllWindows()

#
# Train the recognizer
def train(path, face_detector, recognizer):

    # get the images from  the dataset and the associated IDs

    img_paths    = [ os.path.join(path,f) for f in os.listdir(path) ]
    face_samples = []
    IDs = []
    for img_path in img_paths:
        PIL_img        = Image.open(img_path).convert('L') # get a grayscale image
        array_img      = np.array(PIL_img, 'uint8')
        ID             = int(os.path.split(img_path)[-1].split('.')[1])
        face_locations = face_detector.detectMultiScale(array_img)

        for (x,y,w,h) in face_locations:
            face_samples.append(array_img[y:y+h,x:x+w])
            IDs.append(ID)
    
    # train the recognizer
    # IDs = [0]*len(face_locations)
    recognizer.train(face_samples, np.array(IDs))
    # save the model
    recognizer.write('trainer.yml')


def main():
    
    print('\n\n##################################################################')
    print('#\n#  Welcome to Rhezzon Security')
    print('#  Look into your camera, make sure your entire face is visible...')
    print('#\n##################################################################')

    # Get the user's name
    name = input('\nEnter your name: ')

    # Get the adaboost frontal face detector
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Path to dataset
    path          = 'dataset'
    # Get the recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
       
    # Enroll a user
    enroll(name, face_detector)

    # Train the recognizer
    train(path, face_detector, recognizer)

    print("You have been succesffuly enrolled")


if __name__ == '__main__':
    main()