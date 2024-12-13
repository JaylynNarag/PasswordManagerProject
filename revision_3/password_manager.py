import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import sys
import datetime
import options

def show_password_manager(user_id):
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
    options_button = tk.Button(top_menu_frame, text="Options", font=("Arial", 12), command=lambda: options.OptionsWindow(password_window))
    options_button.pack(side='right')

    # Search and action buttons
    search_frame = tk.Frame(main_content_frame)
    search_frame.pack(fill='x', padx=10, pady=5)
    search_entry = tk.Entry(search_frame, width=50)
    search_entry.pack(side='left', padx=10)

    # Dynamic search by binding
    search_entry.bind("<KeyRelease>", lambda event: search_passwords(search_entry.get(), passwords_db, user_id))
    search_icon_button = tk.Button(search_frame, text="🔍", command=lambda: search_passwords(passwords_db, user_id, search_entry.get()), width=3)  # Pass passwords_db and user_id
    search_icon_button.pack(side='left')

    # Sorting options
    sort_menu_frame = tk.Frame(search_frame)
    sort_menu_frame.pack(side='right')
    sort_label = tk.Label(sort_menu_frame, text="Sort by:")
    sort_label.pack(side='left')
    sort_options = ["Title", "Email", "Username", "Password", "URL", "Date", "Notes"]
    sort_var = tk.StringVar(value="Title")
    sort_menu = ttk.Combobox(sort_menu_frame, textvariable=sort_var, values=sort_options, state='readonly', width=10)
    sort_menu.pack(side='left', padx=5)

    # Buttons
    editbuttons_label = tk.Label(search_frame, text="Edit : ")
    editbuttons_label.pack(side='left', padx=5)
    add_button = tk.Button(search_frame, text="+", command=lambda: add_password(user_id, passwords_db), width=2)  # Pass user_id to save in DB
    add_button.pack(side='left', padx=5)
    edit_button = tk.Button(search_frame, text="✓", command=lambda: edit_password(user_id, passwords_db), width=2)
    edit_button.pack(side='left', padx=5)
    delete_button = tk.Button(search_frame, text="X", command=lambda: delete_password(user_id, passwords_db), width=2)
    delete_button.pack(side='left', padx=5)

    # Table view for passwords
    tree_frame = tk.Frame(main_content_frame) # Put treeview within main frame layout
    tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
    passwords_db = ttk.Treeview(tree_frame, columns=("Title", "Email", "Username", "Password", "URL", "Date Saved", "Notes"), show="headings", height=20) # Actual treeview
    passwords_db.heading("Title", text="Title")
    passwords_db.heading("Email", text="Email")
    passwords_db.heading("Username", text="Username")
    passwords_db.heading("Password", text="Password")
    passwords_db.heading("URL", text="URL")
    passwords_db.heading("Date Saved", text="Date Saved")
    passwords_db.heading("Notes", text="Notes")
    passwords_db.column("Title", width=150, anchor="center")
    passwords_db.column("Email", width=150, anchor="center")
    passwords_db.column("Username", width=150, anchor="center")
    passwords_db.column("Password", width=150, anchor="center")
    passwords_db.column("URL", width=150, anchor="center")
    passwords_db.column("Date Saved", width=150, anchor="center")
    passwords_db.column("Notes", width=200, anchor="center")
    passwords_db.pack(fill='both', expand=True)

    # Just for resizing
    password_window.columnconfigure(0, weight=1)
    password_window.rowconfigure(2, weight=1)

    # Load values
    load_passwords(passwords_db, user_id)
    # Closing window exits program completely so program doesn't still run BC login/signup page hidden
    password_window.protocol("WM_DELETE_WINDOW", close_pwmanager)

def load_passwords(passwords_db, user_id):
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="login_test",
            password="LoginTest123",
            database="PasswordManager"
        )
        cursor = mydb.cursor()

        # GET passwords belonging only to logged-in user via user ID (Foreign Key)
        cursor.execute("SELECT title, email, username, password, url, saved_date, notes FROM passwords WHERE user_id = %s", (user_id,)) # Tuple again
        rows = cursor.fetchall()

        # Populate Treeview with all relevant passwords
        passwords_db.delete(*passwords_db.get_children())  # Clear existing rows - might be populated from last time
        for row in rows:
            passwords_db.insert("", "end", values=row)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", "Error loading passwords: " + str(err))
        mydb.close()

def close_pwmanager(): # Closing WHOLE password manager completely when window closed
    sys.exit()

def search_passwords(query, passwords_db, user_id):
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="login_test",
            password="LoginTest123",
            database="PasswordManager"
        )
        cursor = mydb.cursor()

        # SQL query with LIKE for partial matches
        cursor.execute(
            "SELECT title, email, username, password, url, saved_date, notes FROM passwords WHERE user_id = %s AND (title LIKE %s OR email LIKE %s OR username LIKE %s OR password LIKE %s OR url LIKE %s OR notes LIKE %s)",
            (user_id, f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")
        )
        rows = cursor.fetchall()

        # Update the treeview wth the search results
        passwords_db.delete(*passwords_db.get_children())
        for row in rows:
            passwords_db.insert("", "end", values=row)
        mydb.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", "Error searching passwords: " + str(err))

def advanced_search():
    # Placeholder
    # Advanced search options
    messagebox.showinfo("Advanced Search", "Advanced Search Window")

def add_password(user_id, passwords_db):
    def submit_password():
        title = title_entry.get()
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        url = url_entry.get()
        notes = notes_entry.get("1.0", tk.END) # Include so newlines don't get added
        saved_date = datetime.date.today() # Today's date - Should've added this as normal entry

        if not title or not password:
            messagebox.showerror("Input Error", "Title and password fields are required!")
            return

        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                port="3306",
                user="login_test",
                password="LoginTest123",
                database="PasswordManager"
            )
            cursor = mydb.cursor()

        # Insert into DB
            cursor.execute(
                "INSERT INTO passwords (user_id, title, email, username, password, url, saved_date, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (user_id, title, email, username, password, url, saved_date, notes)
            )
            mydb.commit()
            mydb.close()

            # Refresh the passwords treeview
            load_passwords(passwords_db, user_id)

            # Close the add password window
            add_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", "Error adding password: " + str(err))

    add_window = tk.Toplevel(password_window)
    add_window.title("Add New Password")

     # Create and pack labels and entry widgets for each field
    title_label = tk.Label(add_window, text="Title:")
    title_label.grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(add_window)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    email_label = tk.Label(add_window, text="Email:")
    email_label.grid(row=1, column=0, padx=5, pady=5)
    email_entry = tk.Entry(add_window)
    email_entry.grid(row=1, column=1, padx=5, pady=5)

    username_label = tk.Label(add_window, text="Username:")
    username_label.grid(row=2, column=0, padx=5, pady=5)
    username_entry = tk.Entry(add_window)
    username_entry.grid(row=2, column=1, padx=5, pady=5)

    password_label = tk.Label(add_window, text="Password:")
    password_label.grid(row=3, column=0, padx=5, pady=5)
    password_entry = tk.Entry(add_window)
    password_entry.grid(row=3, column=1, padx=5, pady=5)

    url_label = tk.Label(add_window, text="URL:")
    url_label.grid(row=4, column=0, padx=5, pady=5)
    url_entry = tk.Entry(add_window)
    url_entry.grid(row=4, column=1, padx=5, pady=5)

    notes_label = tk.Label(add_window, text="Notes:")
    notes_label.grid(row=5, column=0, padx=5, pady=5)
    notes_entry = tk.Text(add_window, height=5)  # Multi-line notes
    notes_entry.grid(row=5, column=1, padx=5, pady=5)

    submit_button = tk.Button(add_window, text="Submit", command=submit_password)
    submit_button.grid(row=6, column=1, pady=10)

def edit_password(user_id, passwords_db):
    selected_item = passwords_db.selection()
    if not selected_item: # Only works when selecting in treeview
        messagebox.showwarning("No Selection", "Please select a password to edit.")
        return
    item_values = passwords_db.item(selected_item[0])['values']

    def submit_edit():
        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                port="3306",
                user="login_test",
                password="LoginTest123",
                database="PasswordManager"
            )
            cursor = mydb.cursor()

            # Update the password in the database
            cursor.execute(
                "UPDATE passwords SET title = %s, email = %s, username = %s, password = %s, url = %s, notes = %s WHERE user_id = %s AND title = %s",
                (title_entry.get(), email_entry.get(), username_entry.get(), password_entry.get(), url_entry.get(), notes_entry.get("1.0", tk.END), user_id, item_values[0])
            )
            mydb.commit()
            mydb.close()

            # Refresh the passwords treeview
            load_passwords(passwords_db, user_id)

            # Close the edit password window
            edit_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", "Error editing password: " + str(err))

    edit_window = tk.Toplevel(password_window)
    edit_window.title("Edit Password")

    # Create and pack labels and entry widgets for each field, pre-filled with existing data
    title_label = tk.Label(edit_window, text="Title:")
    title_label.grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(edit_window)
    title_entry.insert(0, item_values[0])  # Take filled title
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    email_label = tk.Label(edit_window, text="Email:")
    email_label.grid(row=1, column=0, padx=5, pady=5)
    email_entry = tk.Entry(edit_window)
    email_entry.insert(0, item_values[1])  # Take filled email
    email_entry.grid(row=1, column=1, padx=5, pady=5)

    username_label = tk.Label(edit_window, text="Username:")
    username_label.grid(row=2, column=0, padx=5, pady=5)
    username_entry = tk.Entry(edit_window)
    username_entry.insert(0, item_values[2])  # Take filled username
    username_entry.grid(row=2, column=1, padx=5, pady=5)

    password_label = tk.Label(edit_window, text="Password:")
    password_label.grid(row=3, column=0, padx=5, pady=5)
    password_entry = tk.Entry(edit_window)
    password_entry.insert(0, item_values[3])  # Take filled password
    password_entry.grid(row=3, column=1, padx=5, pady=5)

    url_label = tk.Label(edit_window, text="URL:")
    url_label.grid(row=4, column=0, padx=5, pady=5)
    url_entry = tk.Entry(edit_window)
    url_entry.insert(0, item_values[4])  # Take filled URL
    url_entry.grid(row=4, column=1, padx=5, pady=5)

    notes_label = tk.Label(edit_window, text="Notes:")
    notes_label.grid(row=5, column=0, padx=5, pady=5)
    notes_entry = tk.Text(edit_window, height=5)
    notes_entry.insert(tk.END, item_values[6])  # Take filled notes
    notes_entry.grid(row=5, column=1, padx=5, pady=5)

    submit_button = tk.Button(edit_window, text="Submit", command=submit_edit)
    submit_button.grid(row=6, column=1, pady=10)

def delete_password(user_id, passwords_db):
    selected_items = passwords_db.selection() # Can choose multiple to delete if selected with ctrl
    if not selected_items:
        messagebox.showwarning("No Selection", "Please select at least one password to delete.")
        return

    # Confirmation dialog
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected password(s)?"):
        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                port="3306",
                user="login_test",
                password="LoginTest123",
                database="PasswordManager"
            )
            cursor = mydb.cursor()

            for selected_item in selected_items:
                item_values = passwords_db.item(selected_item)['values']
                title_to_delete = item_values[0] # Deleting by title, user ID and password
                password_to_delete = item_values[3]

                # Delete the password from the database
                cursor.execute(
                    "DELETE FROM passwords WHERE user_id = %s AND title = %s AND password = %s",
                    (user_id, title_to_delete, password_to_delete)
                )

                # Delete from treeview
                passwords_db.delete(selected_item)

            mydb.commit()
            mydb.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", "Error deleting password(s): " + str(err))