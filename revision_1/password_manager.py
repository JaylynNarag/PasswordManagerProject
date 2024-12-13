import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import sys

def show_password_manager():
    global password_window # Global - Make sure window stays open + gets called : BAD PRACTICE? 
    password_window = tk.Toplevel()
    password_window.title("Password Manager")
    password_window.state('zoomed') # Fit window - dynamic?
    
    # LAYOUT 
    top_menu_frame = tk.Frame(password_window, relief=tk.RAISED, bd=1) # Hold title and options
    top_menu_frame.pack(side='top', fill='x')
    main_content_frame = tk.Frame(password_window)
    main_content_frame.pack(fill='both', expand=True)

    # Top bar layout
    password_label = tk.Label(top_menu_frame, text="Password Manager", font=("Arial", 12), padx=20)
    password_label.pack(side='left')
    options_label = tk.Label(top_menu_frame, text="Options", font=("Arial", 12), padx=20)
    options_label.pack(side='right')

    # Search and action buttons
    search_frame = tk.Frame(main_content_frame)
    search_frame.pack(fill='x', padx=10, pady=5)
    search_entry = tk.Entry(search_frame, width=50)
    search_entry.pack(side='left', padx=10)
    search_icon_button = tk.Button(search_frame, text="🔍", command=lambda: search_passwords(search_entry.get()), width=3)
    search_icon_button.pack(side='left')

    # Sorting options
    sort_menu_frame = tk.Frame(search_frame)
    sort_menu_frame.pack(side='right')
    sort_label = tk.Label(sort_menu_frame, text="Sort by:")
    sort_label.pack(side='left')
    sort_options = ["Title", "Email", "Username", "Password", "URL", "Notes"]
    sort_var = tk.StringVar(value="Title")
    sort_menu = ttk.Combobox(sort_menu_frame, textvariable=sort_var, values=sort_options, state='readonly', width=10)
    sort_menu.pack(side='left', padx=5)
    
    # Buttons
    editbuttons_label = tk.Label(search_frame, text="Edit : ")
    editbuttons_label.pack(side='left', padx=5)
    add_button = tk.Button(search_frame, text="+", command=add_password, width=2)
    add_button.pack(side='left', padx=5)
    edit_button = tk.Button(search_frame, text="✓", command=edit_password, width=2)
    edit_button.pack(side='left', padx=5)
    delete_button = tk.Button(search_frame, text="X", command=delete_password, width=2)
    delete_button.pack(side='left', padx=5)

    # Table view for passwords
    tree_frame = tk.Frame(main_content_frame) # Put treeview within main frame layout
    tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
    passwords_db = ttk.Treeview(tree_frame, columns=("Title", "Email", "Username", "Password", "URL", "Notes"), show="headings", height=20) # Actual treeview - Should include date?
    passwords_db.heading("Title", text="Title")
    passwords_db.heading("Email", text="Email")
    passwords_db.heading("Username", text="Username")
    passwords_db.heading("Password", text="Password")
    passwords_db.heading("URL", text="URL")
    passwords_db.heading("Notes", text="Notes")
    passwords_db.column("Title", width=150, anchor="center")
    passwords_db.column("Email", width=150, anchor="center")
    passwords_db.column("Username", width=150, anchor="center")
    passwords_db.column("Password", width=150, anchor="center")
    passwords_db.column("URL", width=150, anchor="center")
    passwords_db.column("Notes", width=200, anchor="center")
    passwords_db.pack(fill='both', expand=True)

    # Just for resizing
    password_window.columnconfigure(0, weight=1)
    password_window.rowconfigure(2, weight=1)

    # Load values
    load_passwords(passwords_db)

    # Closing window exits program completely so program doesn't still run BC login/signup page hidden
    password_window.protocol("WM_DELETE_WINDOW", close_pwmanager)

def load_passwords(passwords_db):
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

        # Passwords table - Maybe add date, way to search by recent
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                username VARCHAR(255),
                email VARCHAR(255),
                password VARCHAR(255) NOT NULL,
                url VARCHAR(255),
                notes LONGTEXT
            )
        ''')

        mydb.commit()
        mydb.close()
    
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", "Error creating database: " + str(err)) # Error box if not working

def close_pwmanager():
    # Closing password manager completely when window closed by user bc root window hidden
    sys.exit()

def search_passwords(query):
    # Placeholder
    # Replace with actual DB query based on search term, should be dynamic? Search as user types?
    messagebox.showinfo("Search", f"Searching for: {query}")

def advanced_search():
    # Placeholder
    # Use linear and binary search here? or in search_passwords function
    messagebox.showinfo("Advanced Search", "Advanced Search Window")

def add_password():
    # Placeholder
    # Adding new password records
    messagebox.showinfo("Add Password", "Add Password Window")

def edit_password():
    # Placeholder
    # UI for editing existing password records - maybe in actual treeview then update into DB table? or in new window
    messagebox.showinfo("Edit Password", "Edit Password Window")

def delete_password():
    # Placeholder
    # Delete selected rows
    messagebox.showinfo("Delete Password", "Delete Password Confirmation")