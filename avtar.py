# take your pic with the use of webcame and create avtar..

'''install this libraries

1.) OpenCV (for image processing and webcam access):
pip install opencv-python
pip install opencv-python-headless  # Optional, for non-GUI OpenCV usage

2.) NumPy (required by OpenCV for numerical operations):
pip install numpy

3.) Pillow (for image processing and working with tkinter):
pip install pillow

4.) Tkinter (standard library for GUI development in Python):
sudo apt-get install python3-tk

Steps to Install : 
Open your terminal or command prompt.
Run the commands above to install the required libraries.

After Installation : 
Once the libraries are installed, run your script with:

python avtar.py
'''

import cv2
import numpy as np
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, Frame
from PIL import Image, ImageTk

def cartoonify_image(image):
    """Apply cartoon effect to an image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    color = cv2.bilateralFilter(image, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def capture_avatar():
    """Capture image from webcam with a larger video size."""
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    captured_frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to access the camera.")
            break

        # Show the video feed in a window
        cv2.imshow("Capture Avatar - Press 'c' to Capture, 'q' to Quit", frame)
        key = cv2.waitKey(1)

        if key == ord('c'):  # Capture the frame
            captured_frame = frame
            break
        elif key == ord('q'):  # Quit without capturing
            break
    
    cap.release()
    cv2.destroyAllWindows()

    if captured_frame is not None:
        cartoon = cartoonify_image(captured_frame)
        cv2.imwrite("avatar_temp.png", cartoon)
        show_avatar("avatar_temp.png")
        messagebox.showinfo("Capture Complete", "Avatar captured successfully!")

def show_avatar(image_path):
    """Display the avatar in the GUI."""
    img = Image.open(image_path)
    img = img.resize((300, 300))
    img = ImageTk.PhotoImage(img)
    avatar_label.config(image=img)
    avatar_label.image = img

def save_avatar():
    """Save the avatar with a custom file name."""
    file_name = file_name_entry.get()
    if not file_name.strip():
        messagebox.showerror("Error", "Please enter a valid file name.")
        return
    file_path = f"{file_name}.png"
    try:
        img = Image.open("avatar_temp.png")
        img.save(file_path)
        messagebox.showinfo("Save Complete", f"Avatar saved as {file_path}")
    except FileNotFoundError:
        messagebox.showerror("Error", "No avatar found. Please capture one first.")

def load_existing_image():
    """Load an existing image from the disk and process it."""
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image = cv2.imread(file_path)
        cartoon = cartoonify_image(image)
        cv2.imwrite("avatar_temp.png", cartoon)
        show_avatar("avatar_temp.png")
        messagebox.showinfo("Processing Complete", "Avatar created from the selected image!")

# Create GUI
root = Tk()
root.title("Avatar Creator")
root.geometry("500x600")
root.configure(bg="#333333")  # Dark background color for the main window

# Title Frame
title_frame = Frame(root, bg="#444444", height=50)
title_frame.pack(fill="x")
title_label = Label(title_frame, text="Avatar Creator", bg="#4a4444", fg="white", font=("Arial", 18))
title_label.pack(pady=10)

# Avatar display
avatar_label = Label(root, text="Avatar will appear here", width=40, height=15, bg="#1e1e1e", relief="groove")
avatar_label.pack(pady=20)

# Buttons with dark theme styling
capture_button = Button(root, text="Capture Avatar (Fullscreen)", command=capture_avatar, bg="#2196F3", fg="white", font=("Arial", 12), width=20)
capture_button.pack(pady=10)

load_button = Button(root, text="Load Existing Image", command=load_existing_image, bg="#2196F3", fg="white", font=("Arial", 12), width=20)
load_button.pack(pady=10)

# File name entry and save button
file_name_label = Label(root, text="Enter File Name:", bg="#333333", fg="white", font=("Arial", 12))
file_name_label.pack(pady=5)

file_name_entry = Entry(root, width=30, font=("Arial", 12))
file_name_entry.pack(pady=5)

save_button = Button(root, text="Save Avatar", command=save_avatar, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
save_button.pack(pady=10)

exit_button = Button(root, text="Exit", command=root.quit, bg="#f44336", fg="white", font=("Arial", 12), width=20)
exit_button.pack(pady=20)

root.mainloop()