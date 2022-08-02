import cv2
import face_recognition


imgBill = face_recognition.load_image_file('C:\\Users\\Bilal Sheikh\\Desktop\\Coding Stuff\\Python\\practise\\xAttendance_Face_Rec\\known\\Bill Gates.jpg')
imgBill = cv2.cvtColor(imgBill,cv2.COLOR_BGR2RGB)
imgJeff = face_recognition.load_image_file('C:\\Users\\Bilal Sheikh\\Desktop\\Coding Stuff\\Python\\practise\\xAttendance_Face_Rec\\known\\Jeff Bezos.jpg')
imgJeff = cv2.cvtColor(imgJeff,cv2.COLOR_BGR2RGB)
 
faceLocBill = face_recognition.face_locations(imgBill)[0] # Detect coordinates of faces. [0] is used cause it returns a list of 1 element and we need 1st element at index [0]
encodeBill = face_recognition.face_encodings(imgBill)[0]# [0] is used because it retuns an array of 1 element so we need 1st element hence the value [0] 
cv2.rectangle(imgBill,(faceLocBill[3],faceLocBill[0]),(faceLocBill[1],faceLocBill[2]),(0,255,0),2) # Green color rectangle around the face
cv2.rectangle(imgBill,(faceLocBill[3],faceLocBill[2]-15),(faceLocBill[1],faceLocBill[2]),(0,0,0),-1) # Black color rectangle as a lable for the text
cv2.putText(imgBill, 'Bill Gates', (faceLocBill[3],faceLocBill[2]), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1) # White color text

faceLocJeff = face_recognition.face_locations(imgJeff)[0]
encodeJeff = face_recognition.face_encodings(imgJeff)[0]
cv2.rectangle(imgJeff,(faceLocJeff[3],faceLocJeff[0]),(faceLocJeff[1],faceLocJeff[2]),(0,255,0),2)
cv2.rectangle(imgJeff,(faceLocJeff[3],faceLocJeff[2]-15),(faceLocJeff[1],faceLocJeff[2]),(0,0,0),-1)
cv2.putText(imgJeff, 'Jeff Bezos', (faceLocJeff[3],faceLocJeff[2]), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)

#(1stparam,2ndparam) 1st must be a list of encoded faces and 2nd must be a single face
result = face_recognition.compare_faces([encodeBill], encodeJeff, tolerance=0.4)
faceDis = face_recognition.face_distance([encodeBill],encodeJeff) #is same as setting tolerance=0.4 typically the best for look-a-likes
print(faceDis)

cv2.imshow('Bill Gates',imgBill)# (1st param,2nd param) 1st shows the name defined in '' on top of dialog box of img
cv2.imshow('Jeff Bezos',imgJeff)
cv2.waitKey(0) # delay value is in miliseconds i.e, (5000) is 5 sec (10000) is 10 sec and (0) is infinite(until a key is pressed)


