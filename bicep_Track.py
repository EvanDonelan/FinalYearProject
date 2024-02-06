import cv2
import tkinter as tk
from tkinter import Label
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

        # Initialize rep counter and flags
        self.rep_count = 0
        self.reached_top = False
        self.reached_bottom = False
        self.rep_label = Label(root, text=f"Reps: {self.rep_count}")
        self.rep_label.pack(side="bottom")

        # Start the camera update function
        self.update_camera()

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame)
            if results.pose_landmarks:
                self.draw_bicep_curl_joints(frame, results.pose_landmarks.landmark)
                self.update_reps(results.pose_landmarks.landmark)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.camera_label.config(image=photo)
            self.camera_label.photo = photo
        self.camera_label.after(10, self.update_camera)

    def draw_bicep_curl_joints(self, frame, landmarks):
        left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]

        # Draw lines connecting the joints
        if left_shoulder.visibility and left_elbow.visibility:
            cv2.line(frame, (int(left_shoulder.x * frame.shape[1]), int(left_shoulder.y * frame.shape[0])),
                     (int(left_elbow.x * frame.shape[1]), int(left_elbow.y * frame.shape[0])), (255, 255, 0), 2)
        if right_shoulder.visibility and right_elbow.visibility:
            cv2.line(frame, (int(right_shoulder.x * frame.shape[1]), int(right_shoulder.y * frame.shape[0])),
                     (int(right_elbow.x * frame.shape[1]), int(right_elbow.y * frame.shape[0])), (255, 255, 0), 2)
        if left_elbow.visibility and left_wrist.visibility:
            cv2.line(frame, (int(left_elbow.x * frame.shape[1]), int(left_elbow.y * frame.shape[0])),
                     (int(left_wrist.x * frame.shape[1]), int(left_wrist.y * frame.shape[0])), (255, 255, 0), 2)
        if right_elbow.visibility and right_wrist.visibility:
            cv2.line(frame, (int(right_elbow.x * frame.shape[1]), int(right_elbow.y * frame.shape[0])),
                     (int(right_wrist.x * frame.shape[1]), int(right_wrist.y * frame.shape[0])), (255, 255, 0), 2)

        # Draw circles at bicep curl joints
        if left_shoulder.visibility:
            cv2.circle(frame, (int(left_shoulder.x * frame.shape[1]), int(left_shoulder.y * frame.shape[0])), 5, (255, 0, 0), -1)
        if right_shoulder.visibility:
            cv2.circle(frame, (int(right_shoulder.x * frame.shape[1]), int(right_shoulder.y * frame.shape[0])), 5, (255, 0, 0), -1)
        if left_elbow.visibility:
            cv2.circle(frame, (int(left_elbow.x * frame.shape[1]), int(left_elbow.y * frame.shape[0])), 5, (0, 255, 0), -1)
        if right_elbow.visibility:
            cv2.circle(frame, (int(right_elbow.x * frame.shape[1]), int(right_elbow.y * frame.shape[0])), 5, (0, 255, 0), -1)
        if left_wrist.visibility:
            cv2.circle(frame, (int(left_wrist.x * frame.shape[1]), int(left_wrist.y * frame.shape[0])), 5, (0, 0, 255), -1)
        if right_wrist.visibility:
            cv2.circle(frame, (int(right_wrist.x * frame.shape[1]), int(right_wrist.y * frame.shape[0])), 5, (0, 0, 255), -1)

    def update_reps(self, landmarks):
        left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]

        # Calculate the angles
        left_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Check if the arm has reached the bottom point (fully extended) and top point (maximally flexed)
        if 120 <= left_angle <= 180 and 120 <= right_angle <= 180:
            self.reached_bottom = True
        if 35 <= left_angle <= 90 and 35 <= right_angle <= 90:
            self.reached_top = True

        # Increment rep count when both top and bottom points are reached
        if self.reached_bottom and self.reached_top:
            self.rep_count += 1
            self.rep_label.config(text=f"Reps: {self.rep_count}")
            # Reset flags for the next rep
            self.reached_bottom = False
            self.reached_top = False

    def calculate_angle(self, shoulder, elbow, wrist):
        # Calculate the angle using the law of cosines
        shoulder_x, shoulder_y = shoulder.x, shoulder.y
        elbow_x, elbow_y = elbow.x, elbow.y
        wrist_x, wrist_y = wrist.x, wrist.y

        # Calculate the vectors
        vector1 = [elbow_x - shoulder_x, elbow_y - shoulder_y]
        vector2 = [elbow_x - wrist_x, elbow_y - wrist_y]

        # Calculate the dot product
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

        # Calculate the magnitudes
        magnitude1 = (vector1[0] ** 2 + vector1[1] ** 2) ** 0.5
        magnitude2 = (vector2[0] ** 2 + vector2[1] ** 2) ** 0.5

        # Calculate the cosine of the angle
        cosine_angle = dot_product / (magnitude1 * magnitude2)

        # Calculate the angle in radians
        angle_rad = math.acos(cosine_angle)

        # Convert the angle to degrees
        angle_deg = math.degrees(angle_rad)

        return angle_deg

    def on_close(self):
        self.cap.release()
        self.pose.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    camera_gui = CameraGUI(root)
    root.protocol("WM_DELETE_WINDOW", camera_gui.on_close)
    root.mainloop()
