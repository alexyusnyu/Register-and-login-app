import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Create a connection to the SQLite database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create a table to store user information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()


def show_error_message(message):
    error_window = tk.Toplevel(window)
    error_window.title("Error")
    error_window.configure(bg="black")

    error_label = tk.Label(error_window, text=message, font=("Arial", 14), fg="red", bg="black")
    error_label.pack(padx=20, pady=10)

    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy, font=("Arial", 14), bg="red", fg="white")
    ok_button.pack(pady=10)


def register():
    username = username_entry.get()
    password = password_entry.get()

    if len(username) < 3 or len(password) < 3:
        show_error_message("Username and password must contain more than 3 characters")
    else:
        # Check if the username is already taken
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            status_var.set("Username already taken")
            status_label.config(fg="red")
        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            status_var.set("Registration successful")
            status_label.config(fg="green")

        # Clear the entry fields after registration
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')


def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the user exists in the database
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        status_var.set("Login successful")
        status_label.config(fg="green")
        open_main_app_window()
    else:
        status_var.set("Invalid username or password")
        status_label.config(fg="red")

    # Clear the entry fields after login
    username_entry.delete(0, 'end')
    password_entry.delete(0, 'end')


def open_main_app_window():
    main_app_window = tk.Toplevel(window)
    main_app_window.title("Main App")
    main_app_window.configure(bg="black")

    # Load the image
    image = Image.open("image.png")
    image = image.resize((400, 400), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)

    image_label = tk.Label(main_app_window, image=photo, bg="black")
    image_label.pack(padx=10, pady=10)
    image_label.image = photo

    logout_button = tk.Button(main_app_window, text="Logout", command=lambda: close_main_app_window(main_app_window),
                             font=("Arial", 14), bg="#007BFF", fg="white")
    logout_button.pack(pady=10)

    # Create a label to display database information
    database_label = tk.Label(main_app_window, text="Database Information", font=("Arial", 14, "bold"), bg="black", fg="white")
    database_label.pack(pady=10)

    # Retrieve all rows from the database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Create a Treeview to display the users
    user_tree = ttk.Treeview(main_app_window, columns=("ID", "Username"), show="headings", selectmode="browse")
    user_tree.heading("ID", text="ID")
    user_tree.heading("Username", text="Username")
    user_tree.pack(pady=10)

    for user in users:
        user_tree.insert("", "end", values=(user[0], user[1]))

    # Create a delete button to remove selected user
    delete_button = tk.Button(main_app_window, text="Delete User", command=lambda: delete_user(user_tree),
                              font=("Arial", 14), bg="#DC3545", fg="white")
    delete_button.pack(pady=10)


def delete_user(user_tree):
    selected_item = user_tree.selection()

    if selected_item:
        user_id = user_tree.item(selected_item, "values")[0]
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        messagebox.showinfo("User Deleted", "User has been deleted successfully.")
        user_tree.delete(selected_item)
    else:
        messagebox.showwarning("No User Selected", "Please select a user to delete.")


def close_main_app_window(main_app_window):
    messagebox.showinfo("Logout", "Logged out successfully")
    main_app_window.destroy()


# Create the main window
window = tk.Tk()
window.title("Register and Login app")
window.configure(bg="black")

# Set window size and position
window_width = 400
window_height = 300
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

# Make the window responsive
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# Add Background Image
background_image = Image.open("background_image.png")
background_image = background_image.resize((window_width, window_height), Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create and position the username label and entry field
username_label = tk.Label(window, text="Username:", font=("Arial", 14), bg="black", fg="white")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(window, font=("Arial", 14), bg="black", fg="white")
username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Create and position the password label and entry field
password_label = tk.Label(window, text="Password:", font=("Arial", 14), bg="black", fg="white")
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(window, show="*", font=("Arial", 14), bg="black", fg="white")
password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Create and position the register button
register_button = tk.Button(window, text="Register", command=register, font=("Arial", 14), bg="#28A745", fg="white")
register_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

# Create and position the login button
login_button = tk.Button(window, text="Login", command=login, font=("Arial", 14), bg="#007BFF", fg="white")
login_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

# Create and position the status label
status_var = tk.StringVar()
status_label = tk.Label(window, textvariable=status_var, font=("Arial", 12), fg="white", bg="black")
status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Start the main loop
window.mainloop()

# Close the database connection
conn.close()
