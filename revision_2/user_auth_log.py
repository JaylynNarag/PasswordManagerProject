import tkinter as tk
from tkinter import messagebox
import re # RegEx for email, passwords
import password_manager
import mysql.connector
from tkinter import messagebox
# AES ENCRYPTION AND DECRYPTION FOR PASSWORD - STORE IN DB
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os

def connect_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="login_test",
        password="LoginTest123",
        database="PasswordManager"
    )

def sign_up_code(username, email_address, password, confirm_password):
    # Signup system
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" # Regex taken from: https://regex101.com/library/SOgUIV
    
    # ENTRY: CHECKS THEN ENTERED INTO DATABASE TABLES
    if not username or not email_address or not password or not confirm_password:
        messagebox.showerror("Input Error", "All fields are required!")
        return False
    if not re.match(email_pattern, email_address):
        messagebox.showerror("Input Error", "Invalid email entered!")
        return False
    if password != confirm_password:
        messagebox.showerror("Input Error", "Passwords do not match!")
        return False
    else:
        try:
            mydb = connect_database()
            cursor = mydb.cursor()
            cursor.execute(
                "INSERT INTO users (username, email_address, password) VALUES (%s, %s, %s)",
                (username, email_address, password)
            )
            mydb.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            return True
        except mysql.connector.IntegrityError:
            messagebox.showerror("Signup Error", "Username already exists!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", "Error: " + str(err))
        finally:
            mydb.close()
        # After successful login:
        password_manager.show_password_manager()

def log_in_code():
    # Login system
    # After successful login:
    password_manager.show_password_manager()

# Created AES, need to use it with login code to allow user to see password manager and their unique password records
# def encrypt_passwords(password):
#     # Salt - One way, IV - ensure uniqueness
#     salt = os.urandom(16) # string of size random bits
#     init_vector = os.urandom(16)

#     # Derive key from password - KDF - KEY DERIVATION FUNCTION
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=100000,
#         backend=default_backend()
#     )
#     key = kdf.derive(password.encode())

#     cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
#     encryptor = cipher.encryptor()
#     encrypted_card = encryptor.update(password.encode()) + encryptor.finalize()

#     return salt, iv, encrypted_card