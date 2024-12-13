import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
# AVOID USING ROOT OR CALLING PASSWORD_MANAGER VARIABLES, MUTUAL TOPLEVEL IMPORT CAUSES PROBLEMS, BELIEVES THIRD PARTY MODULE BEING IMPLEMENTED? CIRCULAR PROBLEM, SHOULD'VE FIXED

selected_sort_algorithm = ["Merge Sort"] # Make it default sorting algorithm - merge sort (I implemented first before other sortss)
selected_search_algorithm = ["Linear Search"] # Make it default search algorithm - (linear search implemented first, should test time against binary search)

class OptionsWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Options")
        self.window.geometry("400x300")

        # Option: Change Search Algorithm
        tk.Label(self.window, text="Search Algorithm:", font=("Arial", 12)).pack(pady=10)
        # FIRST element of list = default search algo already set, linear search used automatically
        self.search_var = tk.StringVar(value=selected_search_algorithm[0])
        search_options = ["Linear Search", "Binary Search"]
        self.search_menu = ttk.Combobox(self.window, textvariable=self.search_var, values=search_options, state="readonly")
        self.search_menu.pack(pady=5)

        # Option: Change Sort Algorithm
        tk.Label(self.window, text="Sort Algorithm:", font=("Arial", 12)).pack(pady=10)
        # FIrst element of list = default sort algo, merge sort used automatically
        self.sort_var = tk.StringVar(value=selected_sort_algorithm[0])
        sort_options = ["Merge Sort", "Bubble Sort", "Quick Sort"]
        self.sort_menu = ttk.Combobox(self.window, textvariable=self.sort_var, values=sort_options, state="readonly")
        self.sort_menu.pack(pady=5)

        # Save Settings Button
        save_button = tk.Button(self.window, text="Save Settings", font=("Arial", 10), command=self.save_settings)
        save_button.pack(pady=10)

    def save_settings(self):
        selected_sort_algorithm[0] = self.sort_var.get()
        selected_search_algorithm[0] = self.search_var.get()
        messagebox.showinfo("Settings Saved", f"Search algorithm set to: {selected_search_algorithm[0]}\nSort algorithm set to: {selected_sort_algorithm[0]}")  # Confirm settings message - make it clearer to user? Maybe remove - unnecessary
        self.window.destroy()

#// !!SORT ALGORITHMS!! - INCLUDES MERGE SORT, BUBBLE SORT, QUICK SORT, MAYBE INCLUDE HEAPSORT AND RADIX SORT? SHOULD BE CALLED BY PASSWORD_MANAGER.PY WHENEVER SORT BY DROPDOWN MENU USED //
def get_sort_algo():
    # Sort algorithm to be used
    return selected_sort_algorithm[0]

# // Merge sort - followed similar implementation here: https://www.w3schools.com/dsa/dsa_algo_mergesort.php //
def merge_sort(pass_word, sort_column):
    if len(pass_word) <= 1: # !!BASE CASE!!
        return pass_word

    mid = len(pass_word) // 2 # DIVIDE AND CONQUER - Halfing by finding middle record
    left_half = pass_word[:mid]
    right_half = pass_word[mid:]

    # Sorting the halves by, RECURSIVE - calls itself
    left_half = merge_sort(left_half, sort_column)
    right_half = merge_sort(right_half, sort_column)

    return merge(left_half, right_half, sort_column) # Merge halves, result used in password_manager.py!!

def merge(left, right, sort_column):
    merged = [] # To store result to be returned to password_manager.py!!
    left_index = 0
    right_index = 0
    sort_index = ["Title", "Email", "Username", "Password", "URL", "Date", "Notes"].index(sort_column)  # Get the index of the field specified by user e.g. SORT BY: Title

    while left_index < len(left) and right_index < len(right):
        if left[left_index][0][sort_index] <= right[right_index][0][sort_index]:  # Compare the values of the records in specified fields
            merged.append(left[left_index])
            left_index += 1 # Add element from left list if smaller, then move to next element
        else:
            merged.append(right[right_index])
            right_index += 1 # Add element from right list if smaller, then move to next element

    # Remaining elements from lists before finally getting whole result
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged

# // Bubble Sort // 
def bubble_sort(pass_word, sort_column):
    total_recs = len(pass_word) # How many password records in treeview
    sort_index = ["Title", "Email", "Username", "Password", "URL", "Date", "Notes"].index(sort_column)  # Get the index of the field specified by user e.g. SORT BY: Title

    for i in range(total_recs):
        for j in range(0, total_recs - i - 1): # Go through each unsorted element
            if pass_word[j][0][sort_index] > pass_word[j + 1][0][sort_index]: # Get password row's field and compare to the next password field
                pass_word[j], pass_word[j + 1] = pass_word[j + 1], pass_word[j] # Swap if greater
    return pass_word

# // Quick Sort - followed similar implementation here: https://www.geeksforgeeks.org/python-program-for-quicksort/ //
def partition(pass_word, low, high, sort_column):
    # low = start, high = end, rightmost = pivot
    pivot = pass_word[high]
    sort_index = ["Title", "Email", "Username", "Password", "URL", "Date", "Notes"].index(sort_column) # Get the index of the field specified by user e.g. SORT BY: Title
    i = low - 1

    # Go through all elements + compare
    for j in range(low, high): 
        if pass_word[j][0][sort_index] <= pivot[0][sort_index]: # element smaller than pivot, swap with the pointer#s element
            i += 1
            pass_word[i], pass_word[j] = pass_word[j], pass_word[i]

    pass_word[i + 1], pass_word[high] = pass_word[high], pass_word[i + 1]
    return i + 1

def quick_sort(pass_word, low, high, sort_column):
    if low < high:
        # Pivot element - smaller than pivot = left, greater than pivot = right
        piv_element = partition(pass_word, low, high, sort_column)
        quick_sort(pass_word, low, piv_element - 1, sort_column)
        quick_sort(pass_word, piv_element + 1, high, sort_column)

#// !!SEARCH ALGORITHMS!! - INCLUDES LINEAR SEARCH AND BINARY SEARCH - AUTOMATICALLY USES LINEAR SEARCH (BC THE DB IS INITIALLY UNORDERED WHEN LOADING IN TREEVIEW, USER SHOULD SWITCH TO BINARY TREE AFTER SORTING IN PASSWORD MANAGER WINDOW//
def get_search_algo():
    # Search algorithm to be used
    return selected_search_algorithm[0]

# // !!LINEAR SEARCH!! - GOES THROUGH EACH ROW AND SEARCHES //
def linear_search(query, passwords_db, user_id, search_fields):
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="login_test",
            password="LoginTest123",
            database="PasswordManager"
        )
        cursor = mydb.cursor()

        # Get all password records
        cursor.execute("SELECT title, email, username, password, url, saved_date, notes FROM passwords WHERE user_id = %s", (user_id,))
        all_passwords = cursor.fetchall()

        matching_passwords = []

        for row in all_passwords:  # Go through each row and find - add to matching passwords to be displayed in treeview - SEQUENTIAL = LINEAR SEARCH
            # Check if the query is present in ALL specified fields of a row
            if all(query.lower() in str(row[["Title", "Email", "Username", "Password", "URL", "Date Saved", "Notes"].index(field)]).lower() for field in search_fields):
                matching_passwords.append(row)

        # Update the treeview with the search results
        passwords_db.delete(*passwords_db.get_children())
        for i, row in enumerate(matching_passwords):
            tag = "even" if i % 2 == 0 else "odd"
            passwords_db.insert("", "end", values=row, tags=(tag,))

        # Alternate colors
        passwords_db.tag_configure("even", background="lightgray")
        passwords_db.tag_configure("odd", background="white")

        mydb.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", "Error searching passwords: " + str(err))

# // !!BINARY SEARCH!! - ITERATIVE, CHOSE ITERATIVE OVER RECURSIVE, IMPORTANT TO DISTINGUISH IN REPORT - DATA UNSORTED MESSES WITH THE ALGORITHM, FINDS RECORDS BUT WONT RETURN ALL OF THEM, WRONGLY IMPLEMENTED BUT ALGORITHM WORKS, DON'T KNOW HOW TO FIX WITHOUT SORTING WITH DROPDOWN BOX FIRST THEN USING RELEVANT FIELD //
def binary_search(query, passwords_db, user_id, search_fields):
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="login_test",
            password="LoginTest123",
            database="PasswordManager"
        )
        cursor = mydb.cursor()

        # Fetch all passwords for the user to search
        cursor.execute("SELECT title, email, username, password, url, saved_date, notes FROM passwords WHERE user_id = %s", (user_id,))
        all_passwords = cursor.fetchall()

        matching_passwords = []

        for field in search_fields:
            field_index = ["Title", "Email", "Username", "Password", "URL", "Date Saved", "Notes"].index(field)

            # Sort by the current field/fields chosen by user in advanced search
            sorted_passwords = sorted(all_passwords, key=lambda row: str(row[field_index]).lower())

            left, right = 0, len(sorted_passwords) - 1

            while left <= right:
                mid = (left + right) // 2
                if query.lower() in str(sorted_passwords[mid][field_index]).lower():
                    matching_passwords.append(sorted_passwords[mid])
                    # USE POINTERS ON EITHER SIDE OF MIDDLE INDEX TO FIND THE SEARCHED QUERY IN FIELDS, THEN ADD TO MATCHIN PASSWORD TO DISPLAY IN TREEVIEW
                    left_ptr = mid - 1
                    while left_ptr >= 0 and query.lower() in str(sorted_passwords[left_ptr][field_index]).lower():
                        matching_passwords.append(sorted_passwords[left_ptr])
                        left_ptr -= 1
                    right_ptr = mid + 1
                    while right_ptr < len(sorted_passwords) and query.lower() in str(sorted_passwords[right_ptr][field_index]).lower():
                        matching_passwords.append(sorted_passwords[right_ptr])
                        right_ptr += 1
                    break  # Move on to the next field
                elif query.lower() < str(sorted_passwords[mid][field_index]).lower():
                    right = mid - 1
                else:
                    left = mid + 1

        matching_passwords = list(set(matching_passwords))
        # Makes sure that query matches ALL search fields in the final result!! Otherwise returns wrong records
        final_matches = [row for row in matching_passwords if all(query.lower() in str(row[["Title", "Email", "Username", "Password", "URL", "Date Saved", "Notes"].index(field)]).lower() for field in search_fields)]

        # Update treeview, keep alternating colours
        passwords_db.delete(*passwords_db.get_children())
        for i, row in enumerate(final_matches):
            tag = "even" if i % 2 == 0 else "odd"
            passwords_db.insert("", "end", values=row, tags=(tag,))

        # Alternate colors
        passwords_db.tag_configure("even", background="lightgray")
        passwords_db.tag_configure("odd", background="white")

        mydb.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", "Error searching passwords: " + str(err))
