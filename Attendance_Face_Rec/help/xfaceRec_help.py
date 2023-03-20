import cv2
import face_recognition


imgSteve = face_recognition.load_image_file('C:\\Users\\Bilal Sheikh\\Desktop\\Coding Stuff\\Github\\Final Year Project\\Attendance_Face_Rec\\known\\Steve Jobs(123@steve).jpg')
imgSteve = cv2.cvtColor(imgSteve,cv2.COLOR_BGR2RGB)
imgTim = face_recognition.load_image_file('C:\\Users\\Bilal Sheikh\\Desktop\\Coding Stuff\\Github\\Final Year Project\\Attendance_Face_Rec\\known\\Tim Cook(iphone@tim).jpg')
imgTim = cv2.cvtColor(imgTim,cv2.COLOR_BGR2RGB)

faceLocBill = face_recognition.face_locations(imgSteve)[0] # Detect coordinates of faces. [0] is used cause it returns a list of 1 element and we need 1st element at index [0]
encodeBill = face_recognition.face_encodings(imgSteve)[0]# [0] is used because it retuns an array of 1 element so we need 1st element hence the value [0] 
cv2.rectangle(imgSteve,(faceLocBill[3],faceLocBill[0]),(faceLocBill[1],faceLocBill[2]),(0,255,0),2) # Green color rectangle around the face
cv2.rectangle(imgSteve,(faceLocBill[3],faceLocBill[2]-15),(faceLocBill[1],faceLocBill[2]),(0,0,0),-1) # Black color rectangle as a lable for the text
cv2.putText(imgSteve, 'Steve Jobs', (faceLocBill[3],faceLocBill[2]), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1) # White color text

faceLocJeff = face_recognition.face_locations(imgTim)[0]
encodeJeff = face_recognition.face_encodings(imgTim)[0]
cv2.rectangle(imgTim,(faceLocJeff[3],faceLocJeff[0]),(faceLocJeff[1],faceLocJeff[2]),(0,255,0),2)
cv2.rectangle(imgTim,(faceLocJeff[3],faceLocJeff[2]-15),(faceLocJeff[1],faceLocJeff[2]),(0,0,0),-1)
cv2.putText(imgTim, 'Tim Cook', (faceLocJeff[3],faceLocJeff[2]), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)

#(1stparam,2ndparam) 1st must be a list of encoded faces and 2nd must be a single face
result = face_recognition.compare_faces([encodeBill], encodeJeff, tolerance=0.4)
faceDis = face_recognition.face_distance([encodeBill],encodeJeff) #is same as setting tolerance=0.4 typically the best for look-a-likes
print(result)

cv2.imshow('Steve Jobs',imgSteve)# (1st param,2nd param) 1st shows the name defined in '' on top of dialog box of img
cv2.imshow('Tim Cook',imgTim)
cv2.waitKey(0) # delay value is in miliseconds i.e, (5000) is 5 sec (10000) is 10 sec and (0) is infinite(until a key is pressed)
