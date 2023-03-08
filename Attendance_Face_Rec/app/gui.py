#GUI designing starts

from tkinter import *
from app.final import *

root = Tk()

#To always open the window in the center of the screen
root.geometry(f"{700}x{500}+{(root.winfo_screenwidth()//2)-(700//2)}+{(root.winfo_screenheight()//2)-(500//2)}")
root.resizable(0,0)#Not resizable
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
fg="gray96", font="copperplate 25 bold", padx=10, pady=10).pack(side=TOP, fill=X,)

takefaceButton = Button(root, text="Take Attendance", font="copperplate 10 bold", bg="gray40",
fg="gray80", padx=10, pady=10, command=lambda:Take_Face(email_add, images_name)).pack(side=LEFT, anchor="nw", pady=50, padx=160)
                        #Lambda to pass parameters for method

savefaceButton = Button(root, text="Save Face", font="copperplate 10 bold", bg="gray40",
fg="gray80", padx=10, pady=10, command=Save_Face).pack(side=LEFT, anchor="nw", pady=50)

messagebox.showinfo("Known Faces found", f"Found {len(known_encodings_list)} faces in directory\n\n{default_attendance_folder}")

root.mainloop()