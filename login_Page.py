# login_page.py
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
import sqlite3
from user_menu import UserMenu
from admin_menu import AdminMenu

class LoginPage(tk.Toplevel):
    def __init__(self, root, callback):
        super().__init__(root)
        self.title("Login Page")
        self.callback = callback

        # Initialize the database connection
        self.conn = sqlite3.connect("user_database.db")
        self.cursor = self.conn.cursor()

        # Create a table for user information if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        # Create labels, entry widgets, and login/register buttons
        Label(self, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = Entry(self, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        Label(self, text="Password:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = Entry(self, show="*", font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        login_button = Button(self, text="Login", command=self.login, font=("Arial", 12))
        login_button.grid(row=2, column=0, columnspan=2, pady=5)

        register_button = Button(self, text="Register", command=self.register, font=("Arial", 12))
        register_button.grid(row=3, column=0, columnspan=2, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check for hardcoded admin credentials
        if username == "EvanDonelan" and password == "admin":
            self.show_admin_menu()
            self.destroy()
        else:
            # Authenticate regular user against the database
            if self.authenticate_user_db(username, password):
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                self.show_user_menu(username)
                self.destroy()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Add user to the database
        self.add_user_to_db(username, password)

    def authenticate_user_db(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def add_user_to_db(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Registration Successful", "User registered successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Failed", "Username already exists.")

    def show_admin_menu(self):
        AdminMenu(self.callback)

    def show_user_menu(self, username):
        UserMenu(self.callback, username)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root, lambda username: print(f"Logged in as {username}"))
    root.mainloop()
