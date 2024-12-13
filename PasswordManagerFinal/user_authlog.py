import tkinter as tk
from tkinter import messagebox
import re # RegEx for email, passwords
import password_manager
import mysql.connector
from tkinter import messagebox
# AES ENCRYPTION AND DECRYPTION FOR PASSWORD - STORE IN DB IN SIGN UP, DECRYPTED AND CHECKED IN LOGIN
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Ran into multiple mutual top level imports, need to make everything separate - DO NOT TRY TO CALL ROOT WINDOW FROM MAIN.PY, errors.

def connect_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="login_test",
        password="LoginTest123",
        database="PasswordManager"
    )

class password_encrypt:
    def __init__(self, iterations = 100000):
        self.iterations = iterations
        self.backend = default_backend
    
    def encrypt_pass(self, password):
        # Salt - One way, IV - ensure uniqueness
        salt = os.urandom(16) # string of size random bits
        iv = os.urandom(16)

        # Derive key from password - KDF - KEY DERIVATION FUNCTION
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        
        # Actual encrypt
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_pw = encryptor.update(password.encode()) + encryptor.finalize()

        return salt, iv, encrypted_pw
    
    def decrypt_pass(self, encrypted_pw, password, salt, iv):
        # Derive key from password - KDF - KEY DERIVATION FUNCTION
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())

        # Actual decrypt
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_pw = decryptor.update(encrypted_pw) + decryptor.finalize()

        return decrypted_pw.decode()

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
    
    try:
        mydb = connect_database()
        cursor = mydb.cursor()
        # Encrypting the password user entered by using class
        encrypting_pw = password_encrypt()
        salt, iv, encrypted_pw = encrypting_pw.encrypt_pass(password)

        cursor.execute(
            "INSERT INTO users (username, email_address, salt, iv, password) VALUES (%s, %s, %s, %s, %s)",
            (username, email_address, salt.hex(), iv.hex(), encrypted_pw.hex())
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

def log_in_code(username, password):
    # Login system
    # ENTRY: CHECKS IN DATABASE TABLE
    if not username or not password:
        messagebox.showerror("Input Error", "All fields are required!")
        return False
    
    try:
        mydb = connect_database()
        cursor = mydb.cursor()
        cursor.execute("SELECT user_id, password, salt, iv FROM users WHERE username = %s", (username,)) # GETS ALL RELEVANT ENCRYPTION DETAILS WHERE THE USERNAME MATCHES IN DB TABLE, must enter as tuple otherwise error shows up
        result_check = cursor.fetchone()

        if not result_check:
            messagebox.showerror("Login Error", "Username not found!")
            return False

        # Decrypting entered password        
        user_id, encrypted_pw, salt, iv = result_check # USER ID TO BE USED FOR PASSWORD MANAGER TO SHOW USERS PASSWORDS ONLY FROM THE DATABASE
        salt = bytes.fromhex(salt) # ALL MUST BE BYTES OR ERROR SHOWS UP, should've specified in parameters of class possibly?
        iv = bytes.fromhex(iv)
        encrypted_pw = bytes.fromhex(encrypted_pw)
        decrypting_pw = password_encrypt()
        decrypted_pw = None # Gives value to avoid UnboundLocalError - not associated with a value
        try:
            decrypted_pw = decrypting_pw.decrypt_pass(encrypted_pw, password, salt, iv)
        except Exception: # Error occurs, can't decrypt so wrong password entered
            messagebox.showerror("Login Error", "Incorrect password! Please try again")
            return False
        messagebox.showinfo("Success", "Login was successful! Redirecting you to the password manager...")
        return user_id
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", "Error: " + str(err))
        return False
    finally:
        mydb.close()