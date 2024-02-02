# camera_gui.py
import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import mediapipe as mp
import math

class CameraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Feed with Exercise Overlay")

        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)

        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Create a label for displaying the camera feed
        self.camera_label = Label(root)
        self.camera_label.pack(side="left", padx=10)

        # Create buttons for exercises
        self.create_exercise_buttons()

        # Start the camera update function
        self.update_camera()

    def create_exercise_buttons(self):
        # Create buttons for each exercise
        squat_button = Button(self.root, text="Squat", command=lambda: self.highlight_joints_for_exercise("Squat"))
        squat_button.pack(side="top", pady=5)

        bicep_curl_button = Button(self.root, text="Bicep Curl", command=lambda: self.highlight_joints_for_exercise("Bicep Curl"))
        bicep_curl_button.pack(side="top", pady=5)

        deadlift_button = Button(self.root, text="Deadlift", command=lambda: self.highlight_joints_for_exercise("Deadlift"))
        deadlift_button.pack(side="top", pady=5)

        bench_press_button = Button(self.root, text="Bench Press", command=lambda: self.highlight_joints_for_exercise("Bench Press"))
        bench_press_button.pack(side="top", pady=5)

    def highlight_joints_for_exercise(self, exercise):

        print(f"Selected Exercise: {exercise}")

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame)
            if results.pose_landmarks:
                self.draw_skeleton(frame, results.pose_landmarks.landmark)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.camera_label.config(image=photo)
            self.camera_label.photo = photo
        self.camera_label.after(10, self.update_camera)

    def draw_skeleton(self, frame, landmarks):
        for connection in self.mp_pose.POSE_CONNECTIONS:
            start_idx, end_idx = connection
            start_point = landmarks[start_idx]
            end_point = landmarks[end_idx]
            if start_point.visibility and end_point.visibility:
                start_x, start_y = int(start_point.x * frame.shape[1]), int(start_point.y * frame.shape[0])
                end_x, end_y = int(end_point.x * frame.shape[1]), int(end_point.y * frame.shape[0])

                # Draw line
                cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

                # Draw circles at joint locations
                cv2.circle(frame, (start_x, start_y), 5, (0, 0, 255), -1)
                cv2.circle(frame, (end_x, end_y), 5, (0, 0, 255), -1)

    def on_close(self):
        self.cap.release()
        self.pose.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    camera_gui = CameraGUI(root)
    root.protocol("WM_DELETE_WINDOW", camera_gui.on_close)
    root.mainloop()
