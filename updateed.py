import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import json
import json.decoder


#---------------------

def save_credentials():
    with open("credentials.json", "w") as file:
        json.dump(users, file)

# def read_credentials():
#     if os.path.exists("credentials.json"):
#         with open("credentials.json", "r") as file:
#             return json.load(file)
#     else:
#         return {}


def read_credentials():
    if os.path.exists("credentials.json"):
        try:
            with open("credentials.json", "r") as file:
                return json.load(file)
        except json.decoder.JSONDecodeError:
            return {}
    else:
        return {}

users = read_credentials()

# User data storage
files = {}

#----------------------

# Function to register a new user
def register():
    username = entry_username.get()
    password = entry_password.get()

    if username in users:
        messagebox.showerror("Error", "Username already exists.")
    else:
        users[username] = password
        files[username] = []
        save_credentials()  # Add this line to save the credentials after registering a new user
        messagebox.showinfo("Success", "User registered successfully.")
        login_window()

# Function to login
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username in users and users[username] == password:
        messagebox.showinfo("Success", "Login successful.")
        ClipZip_window(username)
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Function to create login window
def login_window():
    window = tk.Toplevel(root)
    window.title("Login")

    global entry_username, entry_password
    username_label = tk.Label(window, text="Username:")
    entry_username = tk.Entry(window)
    password_label = tk.Label(window, text="Password:")
    entry_password = tk.Entry(window, show="*")

    login_button = tk.Button(window, text="Login", command=login)
    register_button = tk.Button(window, text="Register", command=register)

    username_label.pack()
    entry_username.pack()
    password_label.pack()
    entry_password.pack()
    login_button.pack()
    register_button.pack()

# Functions for ClipZip actions
def new_file(username):
    file_name = simpledialog.askstring("New File", "Enter file name:")
    if file_name:
        files[username].append(file_name)
        update_file_list(username)
        text_area.delete("1.0", tk.END)

def delete_file(username):
    selected_file = file_list.get(tk.ACTIVE)
    if selected_file:
        files[username].remove(selected_file)
        update_file_list(username)

def save_file(username):
    selected_file = file_list.get(tk.ACTIVE)
    if selected_file:
        content = text_area.get("1.0", tk.END)
        with open(f"{username}_{selected_file}.txt", "w") as file:
            file.write(content)
        messagebox.showinfo("Success", "File saved successfully.")

def load_file(username):
    selected_file = file_list.get(tk.ACTIVE)
    if selected_file:
        text_area.delete("1.0", tk.END)
        with open(f"{username}_{selected_file}.txt", "r") as file:
            content = file.read()
        text_area.insert(tk.END, content)

def save_file_as(username):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        content = text_area.get("1.0", tk.END)
        with open(file_path, "w") as file:
            file.write(content)
        messagebox.showinfo("Success", "File saved successfully.")

def exit_application():
    root.destroy()

def update_file_list(username):
    file_list.delete(0, tk.END)
    for file in files[username]:
        file_list.insert(tk.END, file)

# Function to create ClipZip window
def ClipZip_window(username):
    ClipZip = tk.Toplevel(root)
    ClipZip.title(f"{username}'s ClipZip")

    global file_list, text_area
    file_list = tk.Listbox(ClipZip)
    text_area = tk.Text(ClipZip)

    file_list.pack(side=tk.LEFT, fill=tk.Y)
    text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    menu = tk.Menu(ClipZip)
    ClipZip.config(menu=menu)

    file_menu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=lambda: new_file(username))
    file_menu.add_command(label="Delete", command=lambda: delete_file(username))
    file_menu.add_command(label="Save", command=lambda: save_file(username))
    file_menu.add_command(label="Load", command=lambda: load_file(username))
    file_menu.add_command(label="Save As", command=lambda: save_file_as(username))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_application)

    update_file_list(username)

# Main window
root = tk.Tk()
root.withdraw()
login_window()
root.mainloop()