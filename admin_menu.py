# admin_menu.py
import tkinter as tk

class AdminMenu(tk.Toplevel):
    def __init__(self, callback):
        super().__init__()
        self.title("Admin Menu")
        self.geometry("400x200")


        label = tk.Label(self, text="Welcome, Admin!", font=("Arial", 16))
        label.pack(pady=20)

        logout_button = tk.Button(self, text="Logout", command=self.logout, font=("Arial", 12))
        logout_button.pack()

        userDb_button = tk.Button(self, text="Users database", command=self.userDb, font=("Arial", 12))
        userDb_button.pack()

        exerciseDb_button = tk.Button(self, text="Exercise database", command=self.exerciseDb, font=("Arial", 12))
        exerciseDb_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.callback = callback

    def logout(self):
        self.destroy()
        self.callback("Logged out")

    def userDb(self):
        self.destroy()

    def exerciseDb(self):
        self.destroy()

    def on_close(self):
        self.destroy()
        self.callback("Closed admin menu")

if __name__ == "__main__":
    root = tk.Tk()
    AdminMenu(root, lambda message: print(message))
    root.mainloop()
