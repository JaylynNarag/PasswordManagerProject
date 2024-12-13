import tkinter as tk
from tkinter import ttk, messagebox # TTK = widget
import mysql.connector # Connect to MySQL

import user_authlog
import password_manager

# Main Window - Should open with Login/Signup page
root = tk.Tk()
root.title("Password Manager")
root.state('zoomed') # Fit window - dynamic?

def create_database(): # Creates database in MySQL, schema = 'PasswordManager', tables = users (login) & passwords
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="login_test",
            password="LoginTest123"
        )
        cursor = mydb.cursor()

        # Create the schema
        cursor.execute("CREATE SCHEMA IF NOT EXISTS `PasswordManager`")
        cursor.execute("USE `PasswordManager`")

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                email_address VARCHAR(255) NOT NULL UNIQUE,
                salt VARCHAR(255) NOT NULL,
                iv VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')

        # Passwords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                entry_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                username VARCHAR(255),
                email VARCHAR(255),
                password VARCHAR(255) NOT NULL,
                url VARCHAR(255),
                saved_date date,
                notes LONGTEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        mydb.commit()
        mydb.close()
    
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", "Error creating database: " + str(err)) # Error box if not working
 
# Password Manager FIRST WINDOW - Signup or Login, all labels packed on same line - show packed elements under it
def show_homepage():
    title_label = tk.Label(root, text="Welcome to password manager!", font=("Arial", 20)).pack(pady=20)

    signup_button = tk.Button(root, text="Sign Up", font=("Arial", 12), width=15, command=lambda: show_signuplogin("signup"))
    signup_button.pack(pady=10)
    login_button = tk.Button(root, text="Login", font=("Arial", 12), width=15, command=lambda: show_signuplogin("login"))
    login_button.pack(pady=10)

def show_signuplogin(active_tab="signup"):
    for widget in root.winfo_children():
        widget.destroy()
    
    tabbed_window = ttk.Notebook(root)
    tabbed_signup = ttk.Frame(tabbed_window)
    tabbed_login = ttk.Frame(tabbed_window)
    tabbed_window.add(tabbed_signup, text="Signup")
    tabbed_window.add(tabbed_login, text="Login")
    tabbed_window.pack(expand=True, fill="both")
    if active_tab == "login":
        tabbed_window.select(tabbed_login) # Needed to be able to choose between tabs so homepage buttons work

    # !!SIGNUP TABBED PAGE LAYOUT!!
    def submitted_signup():
        username = usernamesignup_entry.get()
        email_address = email_entry.get()
        password = passwordsignup_entry.get()
        confirm_password = confirmpassword_entry.get()

        if user_authlog.sign_up_code(username, email_address, password, confirm_password):
            for widget in root.winfo_children():
                widget.destroy()
            show_signuplogin(active_tab="login")  # Switch to login page when sign up done by user

    tk.Label(tabbed_signup, text="Username", font=("Arial", 12)).pack(pady=10)
    usernamesignup_entry = tk.Entry(tabbed_signup, font=("Arial", 12), width=30)
    usernamesignup_entry.pack(pady=5)

    tk.Label(tabbed_signup, text="Email Address", font=("Arial", 12)).pack(pady=10)
    email_entry = tk.Entry(tabbed_signup, font=("Arial", 12), width=30)
    email_entry.pack(pady=5)

    tk.Label(tabbed_signup, text="Password", font=("Arial", 12)).pack(pady=10)
    passwordsignup_entry = tk.Entry(tabbed_signup, font=("Arial", 12), width=30, show="*")
    passwordsignup_entry.pack(pady=5)

    tk.Label(tabbed_signup, text="Confirm Password", font=("Arial", 12)).pack(pady=10)
    confirmpassword_entry = tk.Entry(tabbed_signup, font=("Arial", 12), width=30, show="*")
    confirmpassword_entry.pack(pady=5)

    submitsignup_button = tk.Button(tabbed_signup, text="Submit", font=("Arial", 12), command=submitted_signup) # Gets all entries and saves them to DB table when clicked
    submitsignup_button.pack(pady=5)

    # !!LOGIN TABBED PAGE LAYOUT!!
    def submitted_login():
        username = usernamelogin_entry.get()
        password = passwordlogin_entry.get()

        user_id = user_authlog.log_in_code(username, password) # Get user ID to populate treeview
        if user_id:
            root.withdraw()
            password_manager.show_password_manager(user_id)

    tk.Label(tabbed_login, text="Username", font=("Arial", 12)).pack(pady=10)
    usernamelogin_entry = tk.Entry(tabbed_login, font=("Arial", 12), width=30)
    usernamelogin_entry.pack(pady=5)

    tk.Label(tabbed_login, text="Password", font=("Arial", 12)).pack(pady=10)
    passwordlogin_entry = tk.Entry(tabbed_login, font=("Arial", 12), width=30, show="*")
    passwordlogin_entry.pack(pady=5)

    submitlogin_button = tk.Button(tabbed_login, text="Submit", font=("Arial", 12), command=submitted_login) # Gets all entries and saves them to DB table when clicked
    submitlogin_button.pack(pady=5)

create_database()
show_homepage()
root.mainloop()