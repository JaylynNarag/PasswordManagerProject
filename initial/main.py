import tkinter as tk
from tkinter import ttk, messagebox # TTK = widget
import mysql.connector # Connect to MySQL

import user_login
import password_manager

# Main Window - Should open with Login/Signup page
global root
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
        cursor.execute("CREATE SCHEMA IF NOT EXISTS PasswordManager")
        cursor.execute("USE PasswordManager")

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                fivewords VARCHAR(255) NOT NULL UNIQUE
            )
        ''')

        mydb.commit()
        mydb.close()
    
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", "Error creating database: " + str(err)) # Error box if not working

# Password Manager FIRST WINDOW - Signup or Login, all labels packed on same line to make it more readable (less lines)
def show_homepage():
    title_label = tk.Label(root, text="Welcome to password manager!", font=("Arial", 20)).pack(pady=20)

    signup_button = tk.Button(root, text="Sign Up", font=("Arial", 12), width=15, command=show_signuplogin)
    signup_button.pack(pady=10)
    login_button = tk.Button(root, text="Login", font=("Arial", 12), width=15, command=show_signuplogin)
    login_button.pack(pady=10)

def show_signuplogin():
    for widget in root.winfo_children(): # TO REMOVE HOMEPAGE WIDGETS SO DOESNT SHOW UP WHEN MAKING NEW WIDGETS
        widget.destroy()
    
    # SIGNUP/LOGIN layout : Notebook for tabs view
    tabbed_window = ttk.Notebook(root)
    tabbed_signup = ttk.Frame(tabbed_window)
    tabbed_login = ttk.Frame(tabbed_window)
    tabbed_window.add(tabbed_signup, text="Signup")
    tabbed_window.add(tabbed_login, text="Login")
    tabbed_window.pack(expand=True, fill="both")

    # !!SIGNUP TABBED PAGE LAYOUT!!
    tabbed_window.add(tabbed_signup, text='Signup')
    tabbed_window.pack(expand=True, fill="both")

    tk.Label(tabbed_signup, text="Username", font=("Arial", 12)).pack(pady=10)
    username_entry = tk.Entry(tabbed_signup, font=("Arial",12), width=30)
    username_entry.pack(pady=5)

    tk.Label(tabbed_signup, text="Email Address", font=("Arial", 12)).pack(pady=10)
    email_entry = tk.Entry(tabbed_signup, font=("Arial",12), width=30)
    email_entry.pack(pady=5)

    tk.Label(tabbed_signup, text="Password", font=("Arial", 12)).pack(pady=10)
    password_entry = tk.Entry(tabbed_signup, font=("Arial", 12), width=30, show="*") # ONLY SHOW ASTERISKS WHEN TYPING PASSWORDS, MAYBE ADD BUTTON TO PRESS TO SHOW?
    password_entry.pack(pady=5)

    tk.Label(tabbed_signup, text="Confirm Password", font=("Arial", 12)).pack(pady=10)
    confirmpassword_entry = tk.Entry(tabbed_signup, font=("Arial", 12), width=30, show="*") # ONLY SHOW ASTERISKS WHEN TYPING PASSWORDS, MAYBE ADD BUTTON TO PRESS TO SHOW?
    confirmpassword_entry.pack(pady=5)

    # CHANGE!!! MAKE IT SO THAT WHEN USER_LOGIN LOGIN/SIGNUP LOGIC DONE, CHANGE SO THAT THE LAMBDA OPENS THAT INSTEAD
    submit_button = tk.Button(tabbed_signup, text="Submit", font=("Arial", 12), command=lambda: user_login.sign_up_logic())
    submit_button.pack(pady=5)

    # !!LOGIN TABBED PAGE LAYOUT!!
    tk.Label(tabbed_login, text="Username", font=("Arial", 12)).pack(pady=10)
    username_entry = tk.Entry(tabbed_login, font=("Arial", 12), width=30)
    username_entry.pack(pady=5)

    tk.Label(tabbed_login, text="Password", font=("Arial", 12)).pack(pady=10)
    password_entry = tk.Entry(tabbed_login, font=("Arial", 12), width=30, show="*") # ONLY SHOW ASTERISKS WHEN TYPING PASSWORDS, MAYBE ADD BUTTON TO PRESS TO SHOW?
    password_entry.pack(pady=5)

    # CHANGE!!! MAKE IT SO THAT WHEN USER_LOGIN LOGIN/SIGNUP LOGIC DONE, CHANGE SO THAT THE LAMBDA OPENS THAT INSTEAD
    submit_button = tk.Button(tabbed_login, text="Submit", font=("Arial", 12), command=lambda: user_login.log_in_logic())
    submit_button.pack(pady=5)

create_database()
show_homepage()
root.mainloop()