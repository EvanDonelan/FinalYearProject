# admin_interface.py
import tkinter as tk
from tkinter import Label, Button, Entry, messagebox, Toplevel, ttk
import sqlite3

# Database initialization
conn = sqlite3.connect("user_database.db")
cursor = conn.cursor()

# Function to open a new window for admin tasks
def open_admin_window():
    admin_window = Toplevel()
    admin_window.title("Admin Interface")

    # Create a treeview to display user data
    tree = ttk.Treeview(admin_window)
    tree["columns"] = ("ID", "Username", "Password")
    tree.heading("#0", text="ID")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")

    # Fetch data from the database and populate the treeview
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        tree.insert("", "end", values=user)

    tree.pack(expand=True, fill=tk.BOTH)

# Function to handle admin login button click
def admin_login_button_click(admin_login_window):
    admin_username = admin_username_entry.get()
    admin_password = admin_password_entry.get()

    # Check if the provided credentials match the predefined admin
    if admin_username == "admin" and admin_password == "admin_password":
        messagebox.showinfo("Admin Login Successful", "Welcome, Admin!")
        open_admin_window()  # Open the admin interface window
        admin_login_window.destroy()  # Close admin login window
    else:
        messagebox.showerror("Admin Login Failed", "Invalid admin credentials")

# Create the admin login window
admin_login_window = Toplevel()
admin_login_window.title("Admin Login")

admin_username_label = Label(admin_login_window, text="Admin Username:", font=("Arial", 12))
admin_username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
admin_username_entry = Entry(admin_login_window, font=("Arial", 12))
admin_username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

admin_password_label = Label(admin_login_window, text="Admin Password:", font=("Arial", 12))
admin_password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
admin_password_entry = Entry(admin_login_window, show="*", font=("Arial", 12))
admin_password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

admin_login_button = Button(admin_login_window, text="Login", command=lambda: admin_login_button_click(admin_login_window), font=("Arial", 12))
admin_login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Hide the admin login window initially
admin_login_window.withdraw()

# Run the GUI main loop
admin_login_window.mainloop()  # Only for testing the admin login window; should be opened from main.py
