import tkinter as tk
from tkinter import ttk, messagebox

selected_sort_algorithm = ["Merge Sort"] # Make it default sorting algorithm

class OptionsWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Options")
        self.window.geometry("400x300")

        # Option: Change Search Algorithm
        tk.Label(self.window, text="Search Algorithm:", font=("Arial", 12)).pack(pady=10)
        self.search_var = tk.StringVar(value="Linear Search")
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
        messagebox.showinfo("Settings Saved", f"Sort Algorithm: {selected_sort_algorithm[0]}") # Confirm settings - make it clearer to user? Maybe remove - unnecessary

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