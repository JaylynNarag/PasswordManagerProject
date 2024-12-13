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

    # Search layouts
    search_frame = tk.Frame(main_content_frame)
    search_frame.pack(fill='x', padx=10, pady=5)
    search_entry = tk.Entry(search_frame, width=50)
    search_entry.pack(side='left', padx=10)
    # Dynamic search by binding
    search_entry.bind("<KeyRelease>", lambda event: search_passwords(search_entry.get(), passwords_db, user_id))
    # Search icon button reposition
    search_icon_button = tk.Button(search_frame, text="🔍", command=lambda: advanced_search(user_id, passwords_db), width=3)
    search_icon_button.pack(side='left')
    # Refresh button for treeview
    refresh_button = tk.Button(search_frame, text="↻", command=lambda: load_passwords(passwords_db, user_id), width=3)
    refresh_button.pack(side='left')

    # Sorting options
    sort_menu_frame = tk.Frame(search_frame) # Want them in same layout area
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
    passwords_db.grid(row=0, column=0, sticky="nsew")  # Align Treeview to the left of the frame

    # Create and place the vertical scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=passwords_db.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")  # Align scrollbar to the right of the Treeview

    # Configure Treeview to use the scrollbar
    passwords_db.configure(yscrollcommand=scrollbar.set)

    # Make the Treeview expand properly
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    # Just for resizing
    password_window.columnconfigure(0, weight=1)
    password_window.rowconfigure(2, weight=1)

    # Load values
    load_passwords(passwords_db, user_id)
    # For sort algorithms in option.py, switch between
    sort_menu.bind("<<ComboboxSelected>>", lambda event: sort_passwords(sort_var.get(), passwords_db, user_id)) # Gets the column that the sort variable specifies to sort by, always sorting by that field

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
        
        # Alternate row colours for readability bc its hard to see on pure white bg
        for i, row in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"  # Assign alternating tags
            passwords_db.insert("", "end", values=row, tags=(tag,))  # Apply tag to row

        # Configure tags for alternating colors - if even, lightblue, if odd, white
        passwords_db.tag_configure("even", background="lightgray")  # Color for even rows
        passwords_db.tag_configure("odd", background="white")

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

        query = query.strip()

        # Avoid executing the search if the query is empty
        if not query:
            load_passwords(passwords_db, user_id)  # Load all records if query is empty
            return

        # SQL query with LIKE for partial matches
        cursor.execute(
            """
            SELECT title, email, username, password, url, saved_date, notes 
            FROM passwords 
            WHERE user_id = %s 
            AND (
                title LIKE %s OR email LIKE %s OR username LIKE %s OR 
                password LIKE %s OR url LIKE %s OR saved_date LIKE %s OR notes LIKE %s
            )
            """,
            (
                user_id, 
                f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", 
                f"%{query}%", f"%{query}%", f"%{query}%"
            )
        )
        rows = cursor.fetchall()

        # Update the Treeview with the search results
        passwords_db.delete(*passwords_db.get_children())
        if rows:
            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                passwords_db.insert("", "end", values=row, tags=(tag,))

            # Configure tags for alternating colors
            passwords_db.tag_configure("even", background="lightgray")
            passwords_db.tag_configure("odd", background="white")
        else:
            # Display a message in the UI if no results are found
            passwords_db.insert("", "end", values=("No matches found", "", "", "", "", "", ""), tags=("info",))
            passwords_db.tag_configure("info", background="lightyellow")

        mydb.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error searching passwords: {str(err)}")

    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")

def advanced_search(user_id, passwords_db):
    # Advanced search window - should open up in password manager window and show entries
    advancedsearch_window = tk.Toplevel(password_window)
    advancedsearch_window.title("Advanced Search")
    searchq_label = tk.Label(advancedsearch_window, text="Search Query:")
    searchq_label.grid(row=0, column=0, padx=5, pady=5) # Sticking with pack or grid? Will go back and fix after implementing algorithms - toplevel separate window so should be fine?
    searchq_entry = tk.Entry(advancedsearch_window)
    searchq_entry.grid(row=0, column=1, padx=5, pady=5)

    # Checkbox for fields
    fields = ["Title", "Email", "Username", "Password", "URL", "Date Saved", "Notes"]
    selected_fields = []
    for i, field in enumerate(fields):
        field_vars = tk.BooleanVar(value=True) # Pick all fields of table as default
        # Checkbutton for fields that user wants to search from
        fields_checkbutton = tk.Checkbutton(advancedsearch_window, text=field, variable=field_vars)
        fields_checkbutton.grid(row=i+1, column=0, columnspan=2, sticky="w")
        selected_fields.append(field_vars)

    def carryout_search():
        search_query = searchq_entry.get()
        # Get search fields that are selected in checkbuttons, index it w/ enumerate
        search_fields = [field for i, field in enumerate(fields) if selected_fields[i].get()]

        if not search_fields:
            messagebox.showerror("Input Error", "Please select at least one field to search through!")
            return
        if not search_query:
            messagebox.showerror("Input Error", "Please enter a search query! If searching for values 'None', please use the advanced search.") # Entering 'None' in nromal search returns only one record? Don't know if query is interfered with and causes error. Search for None in advanced search.
            return

        search_algo = options.get_search_algo() # options.py - SIMILAR TO SORT ALGORITHM OPTION

        if search_algo == "Linear Search":
            options.linear_search(search_query, passwords_db, user_id, search_fields)
        elif search_algo == "Binary Search":
            options.binary_search(search_query, passwords_db, user_id, search_fields)
        
        advancedsearch_window.destroy() # Don't want to keep it open when changes set

    search_button = tk.Button(advancedsearch_window, text="Search", command=carryout_search)
    search_button.grid(row=len(fields)+1, column=1, pady=10)

def sort_passwords(sort_column, passwords_db, user_id):
    # Get the selected sort algorithm from options
    sort_algo = options.get_sort_algo()
    # Get data from the treeview
    pass_word = [(passwords_db.item(item)['values'], item) for item in passwords_db.get_children()]

    # Sort based on selected sort algorithm in options
    if sort_algo == "Merge Sort":
        sorted_pass = options.merge_sort(pass_word, sort_column)
    elif sort_algo == "Bubble Sort":
        sorted_pass = options.bubble_sort(pass_word, sort_column)
    elif sort_algo == "Quick Sort":
        size = len(pass_word)
        options.quick_sort(pass_word, 0, size - 1, sort_column)
        sorted_pass = pass_word

    # Clear the treeview and repopulate with sorted data
    passwords_db.delete(*passwords_db.get_children())
    for i, (values, item) in enumerate(sorted_pass):  # Use enumerate to get index
        tag = "even" if i % 2 == 0 else "odd"  # Assign alternating tags
        passwords_db.insert("", "end", values=values, iid=item, tags=(tag,))

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
