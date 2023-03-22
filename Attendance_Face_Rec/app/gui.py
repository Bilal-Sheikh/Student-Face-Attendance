#GUI designing starts

from tkinter import *
from code_ import *

# def Select_Attendance_Folder():#To select attendance folder
#     global default_attendance_folder, face_list, known_encodings_list #Made it global to modify

#     images_name.clear() #Clear previously stored names to avoid conflict
#     email_add.clear()
#     known_images.clear() #Clear previous encodings to avoid re-encoding of the same imgs

#     file = filedialog.askdirectory()
#     if file:
#         messagebox.showwarning("Loading...",
#         "Please wait till all the faces are loaded.\nThis depends on the number of faces you have in the selected directory\nPlease click OK to start")

#         default_attendance_folder = os.path.abspath(file)#Gives the selected dir as a str
#         print(default_attendance_folder)
        
#         face_list = os.listdir(default_attendance_folder)
#         Loaded_Imgs(default_attendance_folder, face_list)
#         known_encodings_list = Find_Encodings(known_images)
        
#         # known_images.clear() #Clear previous encodings to avoid re-encoding of the same imgs
        
#         try:
#             print(f'{len(known_encodings_list)} face encodings found')
#             messagebox.showinfo("Faces found",
#             f"Loading completed successfully\nFound {len(known_encodings_list)} faces in directory\n{default_attendance_folder}")
#             print(images_name)
#         #   print(filepath)
#         except Exception as e:
#             print(e)
#             messagebox.showerror("No Face found", f"ERROR:{e}\nPlease select a folder with only visible Faces")

def Open_Attendance_Sheet(): # Opens Attendance sheet directory
    home = os.path.expanduser('~')
    attendance_folder_path = f"{home}\\Documents\\Attendance"
    subprocess.Popen(f'''explorer "{attendance_folder_path}"''')

def Open_New_Saved_Faces_Folder(): # Opens New Saved folder directory
    newSavedFaces_folder_path = 'C:\\Face Attendance for Students\\New Saved Faces'
    subprocess.Popen(f'''explorer "{newSavedFaces_folder_path}"''')


root = Tk()

# To always open the window in the center of the screen
root.geometry(f"{1000}x{700}+{(root.winfo_screenwidth()//2)-(1000//2)}+{(root.winfo_screenheight()//2)-(700//2)}")
root.resizable(0,0) # Not resizable
root.title(f"Student Face Attendance: {default_attendance_folder}")
root.wm_iconbitmap("Student.ico")
root.configure(bg="grey25")

menuBar = Menu(root)
options = Menu(menuBar, tearoff=0)
options.add_command(label="Select another Attendance Folder", command=Select_Attendance_Folder)
options.add_command(label="Open Attendance sheet", command=Open_Attendance_Sheet)
options.add_command(label="Open New Saved Faces folder", command=Open_New_Saved_Faces_Folder)
menuBar.add_cascade(label="Options", menu=options)
root.config(menu=menuBar)

welcomeMsg = Label(root, text="Welcome to Students Face Attendance", bg="gray40",
                   fg="gray96", font="copperplate 25 bold", padx=10, pady=10).pack(
                   side=TOP, fill=X)

output = Text(root, height=15, background="black", fg="white",
               font=("copperplate 10 bold", 15), borderwidth=3, relief="solid").pack(
               side=BOTTOM, fill=X)

takefaceButton = Button(root, text="Take Attendance", font="copperplate 10 bold", bg="gray40",
                        fg="gray80", padx=10, pady=10, command=lambda:Take_Face(email_add, images_name)).pack(
                        side=LEFT, anchor="nw", pady=50, padx=160)
                                    # Lambda to pass parameters for method

savefaceButton = Button(root, text="Save Face", font="copperplate 10 bold", bg="gray40",
                        fg="gray80", padx=10, pady=10, command=Save_Face).pack(
                        side=LEFT, anchor="nw", pady=50)

messagebox.showinfo("Known Faces found", f"Found {len(known_encodings_list)} faces in directory\n\n{default_attendance_folder}")

root.mainloop()