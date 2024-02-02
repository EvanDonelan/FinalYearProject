# main.py
import tkinter as tk
from login_Page import LoginPage
import CameraAndGui
import Admin_management

class AppManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Application")
        self.login_page = LoginPage(self.root, self.show_main_application)
        self.root.withdraw()  # Hide the main application window initially

    def show_main_application(self, username):
        # Destroy login page
        self.login_page.destroy()

        # Create camera and GUI components
        self.camera_gui = CameraAndGui.CameraGUI(self.root)

        # Create buttons and GUI components
        self.create_gui_components()

        # Show the main application window
        self.root.deiconify()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        # Your existing code for releasing resources
        self.root.destroy()

if __name__ == "__main__":
    app_manager = AppManager()
    app_manager.run()
