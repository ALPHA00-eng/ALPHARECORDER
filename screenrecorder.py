import cv2
import numpy as np
import pyautogui
import keyboard
import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import threading

# Global variables
capture_mode = 'desktop'
is_recording = False
output = None
fps = 10.0  # Lower FPS for low-end PCs

# Functions for screen recording
def start_recording():
    global is_recording, output
    if not is_recording:
        screen_size = (pyautogui.size().width, pyautogui.size().height)
        fourcc = cv2.VideoWriter_fourcc(*"H264")  # Use H.264 codec for better compatibility
        output = cv2.VideoWriter("screen_record.mp4", fourcc, fps, screen_size)
        is_recording = True
        threading.Thread(target=record_screen, daemon=True).start()
        status_label.config(text="Recording started", fg="#5DFF5D")  # Green color
    else:
        messagebox.showwarning("Warning", "Recording is already running.")

def stop_recording():
    global is_recording, output
    if is_recording:
        is_recording = False
        output.release()
        status_label.config(text="Recording stopped", fg="#FF5D5D")  # Red color
    else:
        messagebox.showwarning("Warning", "No recording in progress.")

def toggle_capture_mode():
    global capture_mode
    capture_mode = 'game' if capture_mode == 'desktop' else 'desktop'
    mode_label.config(text=f"Capture Mode: {capture_mode.capitalize()}")
    status_label.config(text=f"Switched to {capture_mode} mode", fg="#5D85FF")  # Blue color

# Screen recording loop
def record_screen():
    while is_recording:
        if capture_mode == 'desktop':
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif capture_mode == 'game':
            img = pyautogui.screenshot()  # Replace this with specialized game capture logic if needed
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Write the frame to the output file
        output.write(frame)
        time.sleep(1/fps)

def set_hotkeys():
    start_stop_hotkey = simpledialog.askstring("Hotkey", "Enter hotkey for start/stop recording:")
    toggle_mode_hotkey = simpledialog.askstring("Hotkey", "Enter hotkey for toggling capture mode:")
    if start_stop_hotkey and toggle_mode_hotkey:
        keyboard.add_hotkey(start_stop_hotkey, start_recording)
        keyboard.add_hotkey(toggle_mode_hotkey, toggle_capture_mode)
        messagebox.showinfo("Success", f"Hotkeys set!\nStart/Stop: {start_stop_hotkey}\nToggle Mode: {toggle_mode_hotkey}")
    else:
        messagebox.showwarning("Warning", "Invalid hotkeys entered.")

# Build the GUI
root = tk.Tk()
root.title("Screen Recorder")
root.geometry("400x300")
root.configure(bg="#1E1E2F")  # Dark background

# Font styles
font_large = ("Helvetica", 16, "bold")
font_medium = ("Helvetica", 12)

# Create a frame for better organization
frame = tk.Frame(root, bg="#1E1E2F")
frame.pack(pady=20)

# Labels
mode_label = tk.Label(frame, text=f"Capture Mode: {capture_mode.capitalize()}", font=font_large, bg="#1E1E2F", fg="white")
mode_label.pack(pady=10)

status_label = tk.Label(frame, text="Recording stopped", font=font_medium, bg="#1E1E2F", fg="#FF5D5D")  # Red color for stopped
status_label.pack(pady=10)

# Button styling
button_style = {
    "font": font_medium,
    "bg": "#4C4C66",
    "fg": "white",
    "activebackground": "#6A6A85",
    "activeforeground": "white",
    "relief": "flat",
    "bd": 0,
    "width": 20,
    "height": 2
}

# Create buttons
def create_button(text, command):
    button = tk.Button(frame, text=text, command=command, **button_style)
    button.pack(pady=5)
    return button

# Buttons
create_button("Start Recording", start_recording)
create_button("Stop Recording", stop_recording)
create_button("Toggle Capture Mode", toggle_capture_mode)
create_button("Set Hotkeys", set_hotkeys)

# Run the GUI
root.mainloop()

# Release resources on exit
if output is not None:
    output.release()
cv2.destroyAllWindows()
