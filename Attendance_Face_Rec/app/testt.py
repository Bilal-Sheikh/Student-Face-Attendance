import tkinter as tk
from PIL import Image, ImageTk
import cv2

# Create the main window
root = tk.Tk()
root.title("Main Window")

# Define a function to create a new window and display video from the webcam
def show_webcam():
    # Create a new Toplevel window
    new_window = tk.Toplevel(root)
    new_window.resizable(0, 0)
    new_window.title("Webcam")

    # Add grab_set to prevent the user from interacting with the main window
    new_window.grab_set()

    # Create a label for displaying the video stream
    label = tk.Label(new_window)
    label.pack()

    # Create a button to stop the video stream
    def stop_stream():
        cap.release()
        new_window.destroy()

    # Add the "Stop Camera" button
    stop_button = tk.Button(new_window, text="Stop Camera", command=stop_stream, bg="red")
    stop_button.pack(side="bottom", pady=10)

    # Open the video stream from the default camera
    cap = cv2.VideoCapture(0)

    # Read frames from the video stream and display them in the Tkinter window
    def update():
        ret, frame = cap.read()
        if ret:
            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to a Tkinter-compatible image
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)

            # Update the label with the new image
            label.configure(image=photo)
            label.image = photo # Store the photo object as an attribute of the label widget

        # Schedule the next update
        label.after(10, update)

    # Start the video stream update loop
    update()


# Add a button to the main window that shows the webcam
tk.Button(root, text="Show Webcam", command=show_webcam).pack()

# Start the main event loop
root.mainloop()
