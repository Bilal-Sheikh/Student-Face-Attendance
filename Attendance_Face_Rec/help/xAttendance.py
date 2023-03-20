import face_recognition
import cv2
import os
import numpy as np
from datetime import datetime
import random

def loadedImgs():
    for img_name in Face_list:
    # loading each img in path to find faces
        loaded_image = face_recognition.load_image_file(f'{path}\\{img_name}')

    # we don't really have to convert the img as we will only use this to compare the imgs captured in the WebCam
    # its just used to check if the list is working properly or not
        # converted_img = cv2.cvtColor(loaded_image,cv2.COLOR_BGR2RGB)
        # known_images.append(converted_img)

        known_images.append(loaded_image)
    # we want only name of the img and not its extension so [0] is used and [1] will return the extension
        Images_name.append(os.path.splitext(img_name)[0])
        # cv2.imshow(img_name,converted_img)
    # print(Images_name)
    # cv2.waitKey(0)

def find_encodings(knownimages):
    encodeList = []
    for img in knownimages:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('C:\\Users\\Bilal Sheikh\\Desktop\\Coding Stuff\\Python\\practise\\xAttendance_Face_Rec\\Attendance.csv','r+') as f:
        myFile_Data = f.readlines()# To read all the lines in the files at once
        nameInFile = []
        for line in myFile_Data:
            entry = line.split(',')
            nameInFile.append(entry[0])
        if name not in nameInFile:
            current_time = datetime.now()
            dtString = current_time.strftime('%H:%M:%S')
            f.writelines(f'{name},{dtString}\n')

def saveFace():
    print("Capturing Face...\n***Please stay still and make sure your face is visible")
    print('''***Press "ESC" to exit and "Spacebar" to capture Face''')
    
    # counter = 1
    while True:
        _, saveFrame = webCam.read()
        cv2.imshow("Save A New Face", saveFrame)

        key = cv2.waitKey(1)

        if key == ord('\x1b'):
            print("Closed successfully.")
            break

        elif key == ord(' '):
            new_img_name = f"Image {random.randint(1,1000)}.jpg"
            cv2.imwrite(os.path.join(New_Face_path, new_img_name), saveFrame)    
            print("Face saved successfully.")
    # webCam.release() # THE BUG THAT TOOK 5 DAY TO SOLVE -_-
    cv2.destroyAllWindows()

def takeFace():
    print('''Taking attendance...
    Capturing Face...
    ***Please stay still and make sure your face is visible
    ***Press "ESC" to exit\n''')
    
    while True:
            _, frame = webCam.read() # capturing each frame from the WebCam.

            resize_img = cv2.resize(frame, (0,0), None, 0.25, 0.25)
            webCamImg = cv2.cvtColor(resize_img, cv2.COLOR_BGR2RGB)

            facesInFrame = face_recognition.face_locations(webCamImg)
            encodesInFrame = face_recognition.face_encodings(webCamImg, facesInFrame)

            for encodeFaceFrame, faceLocFrame in zip(encodesInFrame, facesInFrame):
                # matches = face_recognition.compare_faces(known_encodingsList, encodeFaceFrame)
                faceDistance = face_recognition.face_distance(known_encodingsList, encodeFaceFrame)
                # print(faceDistance)
                # print(matches)
        # To find the best face match we have to choose the index which has the lowest element in the array
                matchIndex = np.argmin(faceDistance)
        # This will return the lowest face distance available in the array and the lowest face 
        # distance is the true match 
        # For ex: if it see the Barack Obama face it will return 0 as the other face distance 
        # value will definetely will be higher than the others and if it sees Bilal's face it will return 1
                # print(matchIndex)
                # z = faceDistance[matchIndex]
                # print(z)
                
                if faceDistance[matchIndex]< 0.50:
                    frame_name = Images_name[matchIndex].upper()
                    markAttendance(frame_name)
                    # print(frame_name)
                    top, right, bottom, left = faceLocFrame
                    top, right, bottom, left = top*4, right*4, bottom*4, left*4

                    cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)
                    cv2.rectangle(frame,(left,bottom-15),(right,bottom),(0,0,0),-1)
                    cv2.putText(frame, frame_name, (left,bottom), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
                else: 
                    frame_name = 'Unknown'
                    # print(frame_name)
                    top, right, bottom, left = faceLocFrame
                    top, right, bottom, left = top*4, right*4, bottom*4, left*4

                    cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)
                    cv2.rectangle(frame,(left,bottom-15),(right,bottom),(0,0,0),-1)
                    cv2.putText(frame, 'Unknown', (left,bottom), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)

            cv2.imshow('Webcam', frame)
            key = cv2.waitKey(1)
            
            if key == ord('\x1b'):
                print("Closed successfully.")
                break
    
    # webCam.release()
    cv2.destroyAllWindows()

path = 'C:\\Users\\Bilal Sheikh\\Desktop\\Coding Stuff\\Github\\Final Year Project\\Attendance_Face_Rec\\known'
New_Face_path = 'C:\\Users\\Bilal Sheikh\\Desktop\\Coding Stuff\\Github\\Final Year Project\\Attendance_Face_Rec\\New Saved Faces'
known_images = [] #contains RGB converted imgs
Images_name = []
Face_list = os.listdir(path)

# root = Tk()
# root.geometry("500x500")

# print(Face_list)
loadedImgs()
known_encodingsList = find_encodings(known_images)
print(f'{len(known_encodingsList)} face encodings found') 

webCam = cv2.VideoCapture(0)

while True:
    message = '''***********SELECT YOUR OPTION***********\n
    1: Take attendance\n
    2: Save a new face\n
    3: Exit\n'''

    try:
        print(message)
        choice = int(input("Enter your choice: "))

        if choice == 1:
            takeFace()

        elif choice == 2:
            saveFace()

        elif choice == 3:
            print("Program closed")
            webCam.release()
            cv2.destroyAllWindows()
            break

        elif choice != 1 or 2 or 3:
        # elif choice != random.randint(1,3):
            print("Invalid Input")
    
    except Exception as e:
        print(f"An Error Occured!!\nEnter numbers only.\nERROR CODE: {e}")

webCam.release()
cv2.destroyAllWindows()