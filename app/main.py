import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, Toplevel, messagebox, Listbox, END, ANCHOR
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


def register():
    username = username_entry.get()
    password = password_entry.get()

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
    main_app_window = Toplevel(window)
    main_app_window.title("Main App")

    # Load the image
    image = Image.open("image.png")
    image = image.resize((400, 400), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)

    image_label = Label(main_app_window, image=photo)
    image_label.pack(padx=10, pady=10)
    image_label.image = photo

    logout_button = Button(main_app_window, text="Logout", command=close_main_app_window, font=("Arial", 14))
    logout_button.pack(pady=10)

    # Create a label to display database information
    database_label = Label(main_app_window, text="Database Information", font=("Arial", 14, "bold"))
    database_label.pack(pady=10)

    # Retrieve all rows from the database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Create a listbox to display the users
    listbox = Listbox(main_app_window, width=50)
    listbox.pack(pady=10)

    for user in users:
        listbox.insert(END, f"ID: {user[0]}, Username: {user[1]}")

    # Create a delete button to remove selected user
    delete_button = Button(main_app_window, text="Delete User", command=lambda: delete_user(listbox),
                           font=("Arial", 14))
    delete_button.pack(pady=10)


def delete_user(listbox):
    selected_user = listbox.get(ANCHOR)

    if selected_user:
        user_id = selected_user.split(":")[1].strip()
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        messagebox.showinfo("User Deleted", "User has been deleted successfully.")
        listbox.delete(ANCHOR)
    else:
        messagebox.showwarning("No User Selected", "Please select a user to delete.")


def close_main_app_window(main_app_window=None):
    messagebox.showinfo("Logout", "Logged out successfully")
    main_app_window.destroy()


# Create the main window
window = Tk()
window.title("Register and Login app by slayer1649")

# Create and position the username label and entry field
username_label = Label(window, text="Username:", font=("Arial", 14))
username_label.grid(row=0, column=0, padx=10, pady=5)
username_entry = Entry(window, font=("Arial", 14))
username_entry.grid(row=0, column=1, padx=10, pady=5)

# Create and position the password label and entry field
password_label = Label(window, text="Password:", font=("Arial", 14))
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry = Entry(window, show="*", font=("Arial", 14))
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Create and position the register button
register_button = Button(window, text="Register", command=register, font=("Arial", 14))
register_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

# Create and position the login button
login_button = Button(window, text="Login", command=login, font=("Arial", 14))
login_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

# Create and position the status label
status_var = StringVar()
status_label = Label(window, textvariable=status_var, font=("Arial", 12), fg="black")
status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Start the main loop
window.mainloop()

# Close the database connection
conn.close()