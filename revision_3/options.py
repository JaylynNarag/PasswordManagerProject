import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import main

# OPTIONS TO CHOOSE BETWEEN SEARCH OR SORT ALGORITHMS IN NEW BOX AND OPTION TO LOG OUT WHICH RESETS PROGRAM - TO BE USED IN SORT BY AND ADVANCED SEARCH
class OptionsWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Options")
        self.window.geometry("400x300")

        # Option: Reset Program
        tk.Label(self.window, text="Reset Program:", font=("Arial", 12)).pack(pady=10)
        reset_button = tk.Button(self.window, text="Reset", font=("Arial", 10), command=self.reset_program)
        reset_button.pack(pady=5)

        # Option: Change Sort Algorithm
        tk.Label(self.window, text="Sort Algorithm:", font=("Arial", 12)).pack(pady=10)
        self.sort_var = tk.StringVar(value="Merge Sort")
        sort_options = ["Merge Sort", "Bubble Sort", "Quick Sort"]
        self.sort_menu = ttk.Combobox(self.window, textvariable=self.sort_var, values=sort_options, state="readonly")
        self.sort_menu.pack(pady=5)

        # Option: Change Search Algorithm
        tk.Label(self.window, text="Search Algorithm:", font=("Arial", 12)).pack(pady=10)
        self.search_var = tk.StringVar(value="Linear Search")
        search_options = ["Linear Search", "Binary Search"]
        self.search_menu = ttk.Combobox(self.window, textvariable=self.search_var, values=search_options, state="readonly")
        self.search_menu.pack(pady=5)

        # Save Settings Button
        save_button = tk.Button(self.window, text="Save Settings", font=("Arial", 10), command=self.save_settings)
        save_button.pack(pady=10)

    def reset_program(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?")
        if confirm:
            messagebox.showinfo("Log Out", "Logging you out now...")
            main()

    def save_settings(self):
        sort_algorithm = self.sort_var.get()
        search_algorithm = self.search_var.get()
        messagebox.showinfo("Settings Saved", f"Sort Algorithm: {sort_algorithm}\nSearch Algorithm: {search_algorithm}") 
