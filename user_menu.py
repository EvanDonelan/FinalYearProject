# user_menu.py
import tkinter as tk

class UserMenu(tk.Toplevel):
    def __init__(self, callback, username):
        super().__init__()
        self.title(f"User Menu - {username}")
        self.geometry("400x200")


        label = tk.Label(self, text=f"Welcome, {username}!", font=("Arial", 16))
        label.pack(pady=20)

        squat_button = tk.Button(self, text="Squat", command=self.squat, font=("Arial", 12))
        squat_button.pack()

        deadlift_button = tk.Button(self, text="Deadlift", command=self.deadlift, font=("Arial", 12))
        deadlift_button.pack()

        bicep_button = tk.Button(self, text="Bicep Curl", command=self.bicep, font=("Arial", 12))
        bicep_button.pack()

        bench_button = tk.Button(self, text="Bench Press", command=self.bench, font=("Arial", 12))
        bench_button.pack()

        logout_button = tk.Button(self, text="Logout", command=self.logout, font=("Arial", 12))
        logout_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.callback = callback

    def logout(self):
        self.destroy()
        self.callback("Logged out")

    def squat(self):
        self.destroy()
        self.callback("Squat selected!")

    def deadlift(self):
        self.destroy()
        self.callback("Deadlift selected!")

    def bicep(self):
        self.destroy()
        self.callback("Bicep curl selected!")

    def bench(self):
        self.destroy()
        self.callback("Bench press selected!")

    def on_close(self):
        self.destroy()
        self.callback("Closed user menu")

if __name__ == "__main__":
    root = tk.Tk()
    UserMenu(root, lambda message: print(message))
    root.mainloop()
