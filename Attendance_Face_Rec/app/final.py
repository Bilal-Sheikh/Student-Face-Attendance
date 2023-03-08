from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
import face_recognition
import cv2
import os
import numpy as np
import random
from posixpath import expanduser
from datetime import datetime
import time
import subprocess
from email.message import EmailMessage
import smtplib

def Loaded_Imgs(folder_path):
    for img_name in face_list:
    # loading each img in path to find faces
        loaded_image = face_recognition.load_image_file(f'{folder_path}\\{img_name}')

    # we don't really have to convert the img as we will only use this to compare the imgs captured in the WebCam
    # its just used to check if the list is working properly or not
        # converted_img = cv2.cvtColor(loaded_image,cv2.COLOR_BGR2RGB)
        # known_images.append(converted_img)

        known_images.append(loaded_image)

    # we want only name of the img and not its extension so [0] is used and [1] will return the extension
        # Images_name.append(os.path.splitext(img_name)[0])
        # email_add.append(os.path.splitext(img_name)[1])

        name = img_name.split('(') #To split name and email
        images_name.append(name[0]) #[0] will give name
        email = name[1].split(')')  #[1] will give list which contains <email>.<extension>
        email_add.append(email[0]) #[0] will give email

        # print(Images_name)
        # print(Email_add)
        
        # cv2.imshow(img_name,converted_img)
    # print(known_images)
    # print(Images_name)
    # cv2.waitKey(0) 

def Find_Encodings(knownimages):
    try: #Trying to get face encodings, if not found jump to except
        encode_list = []
        for img in knownimages:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Converting the loaded imgs from BGR to RGB format
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)
        # print(encodeList)
        return encode_list
    except Exception as e:
        print(e)
        messagebox.showerror("No Face found", f"ERROR:{e}\nPlease select a folder with only visible Faces")

def Mark_Attendance(name, email):
# Making a Attendance folder in C\User\Documents(default can't change) and file with currents date and time 
    
    # Store the date and time in str and only creates only one file in one hr only(1hr delay considering normal lecture time)

    # print(filename)
    
    folder_path = f"{home}\\Documents\\Attendance" #Default folder path
    if not os.path.exists(folder_path): #Checks if folder exists or not. If not then create one
            os.makedirs(f"{home}\\Documents\\Attendance")

    with open(filename, 'a'): #Creates a .csv file with current date and time
        with open(filename, 'r+') as f:
            attendance_file = f.readlines() #To read and store all the lines in the file at once
            names_in_attendanceFile = [] #Create a empty list to store names later

            for line in attendance_file: #Read each stored line
                entry = line.split(',') #Seperate them by "," to get the name and date values
                names_in_attendanceFile.append(entry[0]) #Append name i.e, entry[0] to [] defined above
            
            if name not in names_in_attendanceFile: #Check if name exists or not,if not then write name and date in the .csv
                current_time = datetime.now()
                dt_string = current_time.strftime('%I:%M:%S')
                f.writelines(f'{name},{email},{dt_string}\n')

def Absent_Alert(to, subject, body):
    message = EmailMessage() 
    message.set_content(body) #Body of email
    message['to'] = to # Guardian's email
    message['subject'] = subject # Subject of email

    username = "coeta.attendance.alerts@gmail.com" 
    message['from'] = username # Sender's email
    password = "smasyohyxcovuixf" # Google account app password

    server = smtplib.SMTP("smtp.gmail.com", 587) # 587 is the port no. for gmail's TLS
    server.starttls() 
    server.login(username, password)
    server.send_message(message) 
    server.quit()

def Open_Attendance_Sheet(): #Opens Attendance sheet directory
    home = os.path.expanduser('~')
    attendance_folder_path = f"{home}\\Documents\\Attendance"
    subprocess.Popen(f'''explorer "{attendance_folder_path}"''')

def Open_New_Saved_Faces_Folder(): #Opens New Saved folder directory
    newSavedFaces_folder_path = 'C:\\Face Attendance for Students\\New Saved Faces'
    subprocess.Popen(f'''explorer "{newSavedFaces_folder_path}"''')

def Save_Face(): #Capture a new face
    messagebox.showinfo("Information", '''Capturing Face...\nPlease stay still and make sure your face is visible\nPress "ESC" to exit and "Spacebar" to capture Face''')

    while True: #Open webcam
        _, save_frame = webCam.read()
        cv2.imshow("Save A New Face", save_frame)

        key = cv2.waitKey(1)

        if key == ord('\x1b'): #'\x1b' is the code for "ESC" key
            messagebox.showinfo("Success", "Save Face closed successfully")
            break

        elif key == ord(' '): #"SPACEBAR" to capture face
            if not os.path.exists(default_new_face_folder): #Checks if the default folder exists or not,if not then make one
                os.makedirs(default_new_face_folder)

            #Firstly save the face with random number to avoid "File already exists error"
            random_img_name = f"Face {random.randint(1,1000)}.jpg"
            cv2.imwrite(os.path.join(default_new_face_folder, random_img_name), save_frame) #Capture the face and save it in default folder

            print(f'''"{random_img_name}" saved successfully.''')
            messagebox.showinfo("Success", "Captured successfully")
            
            try: #Try to ask the user to save the Face with the name of the captured person
                new_name = askstring("Name the Face", '''Write the name of student and guardian's email in the format given below\n
                <student name><space><student surname>(<guardian's email>)\n
                ex: John Doe(johndoe@gmail.com)\n''')
                
                #Then rename the random file with the user entered name
                os.rename(f'C:\\Face Attendance for Students\\New Saved Faces\\{random_img_name}',
                f'C:\\Face Attendance for Students\\New Saved Faces\\{new_name}.jpg')
                messagebox.showinfo("Success", f"Saved Successfully in\n{default_new_face_folder}")
                break
                
            # if user enters a name which already exists, delete the random file and show error
            except Exception as e:
                messagebox.showerror("File Error", "File already exists")
                os.remove(f'C:\\Face Attendance for Students\\New Saved Faces\\{random_img_name}')

    # webCam.release() # DONT RELEASE THE CAM until all your work is done
    cv2.destroyAllWindows() # windows can be destroyed tho
 
def Take_Face(ab_email, ab_name):#Take the face from webcam and matching it with the previously loaded imgs
    

    messagebox.showinfo("Information", '''Taking attendance...\nCapturing Face...\nPlease stay still and make sure your face is visible\nPress "ESC" to exit''')
    
    while True:#open web cam
            _, frame = webCam.read() # capturing each frame from the WebCam.

            resize_img = cv2.resize(frame, (0,0), None, 0.25, 0.25)#Decrease the size webcam img for faster processing
            webCamImg = cv2.cvtColor(resize_img, cv2.COLOR_BGR2RGB)

            facesInFrame = face_recognition.face_locations(webCamImg)#Find faces in the webcam
            encodesInFrame = face_recognition.face_encodings(webCamImg, facesInFrame)#take face encodings of the located face

            #zip() take the [0] index of 1st list and binds it with [0] index of 2nd list
            for encodeFaceFrame, faceLocFrame in zip(encodesInFrame, facesInFrame):
                faceDistance = face_recognition.face_distance(known_encodings_list, encodeFaceFrame)
                
                # matches = face_recognition.compare_faces(known_encodings_list, encodeFaceFrame)
                # print(faceDistance)
                # print(matches)

                # To find the best face match we have to choose the index which has the lowest element in the array
                matchIndex = np.argmin(faceDistance)
                # This will return the lowest face distance available in the array and the lowest face 
                # distance is the true match 
                # For ex: if it see the Barack Obama face it will return [0] as the other face distance 
                # value will definetely will be higher than the others and if it sees Bill Gates face it will return [1]
                # print(matchIndex)
                # z = faceDistance[matchIndex]
                # print(z)
                
#Checks if a face is less than the given value. The lower the value the more strict it will be in finding the same face
                if faceDistance[matchIndex]< 0.50:
                    frame_name = images_name[matchIndex].upper()
                    frame_email = email_add[matchIndex]

                    Mark_Attendance(frame_name, frame_email)
                    # print(frame_name)
                    top, right, bottom, left = faceLocFrame#define co-ordinates with the faces found in the webcam
                    #we *4 because earlier we decreased the size so that the box will perfectly fit the face
                    top, right, bottom, left = top*4, right*4, bottom*4, left*4

                    cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)#Make the GREEN box around face
                    cv2.rectangle(frame,(left,bottom-15),(right,bottom),(0,0,0),-1)#Make the BLACK label below the GREEN box
                    cv2.putText(frame, frame_name, (left,bottom), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)#Text in the BLACK BOX
                else: #If no face is matched 
                    frame_name = 'Unknown'
                    # print(frame_name)
                    top, right, bottom, left = faceLocFrame
                    top, right, bottom, left = top*4, right*4, bottom*4, left*4

                    cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)
                    cv2.rectangle(frame,(left,bottom-15),(right,bottom),(0,0,0),-1)
                    cv2.putText(frame, 'Unknown', (left,bottom), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)

            cv2.imshow('Take Attendance', frame)
            key = cv2.waitKey(1)
            
            if key == ord('\x1b'):
                # known_images.clear()
                print("Attendance closed successfully.")
                messagebox.showinfo("Success", "Attendance closed successfully.\nPlease wait while we send emails to guardians of absent students.\nThis may take a while")
                with open(filename, 'r') as f: # open the attendance file
                    ab_File_data = f.readlines()

                    ab_Email_InFile = []
                    ab_Name_InFile = []
                    # abesntEmails = []
                    # abesntNames = []
                    
                    for lines in ab_File_data:
                        ab_entry = lines.split(',')
                        ab_Email_InFile.append(ab_entry[1]) #contains email
                        ab_Name_InFile.append(ab_entry[0]) #contains name

                    # print("PRESENT: ",ab_Email_InFile)

                    for mail, names in zip(ab_email, ab_name): 
                    #checks for name and email in the list with previously loaded imgs

                        if (mail not in ab_Email_InFile) and (names not in ab_Name_InFile):
                            # abesntEmails.append(mail) #append the mails which weren't found in an empty list
                            # abesntNames.append(names) #append the names which weren't found in an empty list
                            Absent_Alert(mail,"COETA Attendance Alert", f"Your ward {names} was ABSENT at {curr_time} lecture")
                            # print("ABSENT: ", mail)
                            # print("ABSENT: ", names)
                break
    
    # webCam.release()
    cv2.destroyAllWindows()

def Select_Attendance_Folder():#To select attendance folder
    global default_attendance_folder, face_list, known_encodings_list #Made it global to modify

    images_name.clear()#Clear previously stored names to avoid conflict

    file = filedialog.askdirectory()
    if file:
        messagebox.showwarning("Loading...",
        "Please wait till all the faces are loaded.\nThis depends on the number of faces you have in the selected directory\nPlease click OK to start")

        default_attendance_folder = os.path.abspath(file)#Gives the selected dir as a str
        # print(defaultAttendanceFolder)
        face_list = os.listdir(default_attendance_folder)
        Loaded_Imgs(default_attendance_folder)
        known_encodings_list = Find_Encodings(known_images)
        known_images.clear() #Clear previous encodings to avoid re-encoding of the same imgs
        try:
            print(f'{len(known_encodings_list)} face encodings found')
            messagebox.showinfo("Faces found",
            f"Loading completed successfully\nFound {len(known_encodings_list)} faces in directory\n{default_attendance_folder}")
        #   print(filepath)
        except Exception as e:
            print(e)
            messagebox.showerror("No Face found", f"ERROR:{e}\nPlease select a folder with only visible Faces")


create_default_attendance_folder = "C:\\Face Attendance for Students\\known"
# createDefaultNewFaceFolder = "C:\\Face Attendance for Students\\New Saved Faces"
if not os.path.exists(create_default_attendance_folder):
        os.makedirs(create_default_attendance_folder)

default_attendance_folder = 'C:\\Face Attendance for Students\\known'
default_new_face_folder = "C:\\Face Attendance for Students\\New Saved Faces"
known_images = []
images_name = []
email_add = []
face_list = os.listdir(default_attendance_folder) # Contains all the files in a directory

curr_time = time.strftime("DATE=%d-%m-%Y TIME=%I %p")
home = os.path.expanduser('~')
filename = f"{home}\\Documents\\Attendance\\Attendance {curr_time}.csv"

# print(Face_list)
Loaded_Imgs(default_attendance_folder)
known_encodings_list = Find_Encodings(known_images)
print(f'{len(known_encodings_list)} face encodings found') 
# messagebox.showinfo("Known Faces found", f"Found {len(known_encodingsList)} faces in directory\n{defaultAttendanceFolder}")

webCam = cv2.VideoCapture(0)# (0) represents default webcam