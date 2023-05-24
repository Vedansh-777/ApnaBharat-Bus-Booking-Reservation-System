import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter

customtkinter.set_appearance_mode("dark")


class Login(customtkinter.CTk):
    width = 1240
    height = 1080

    def __init__(self):
        super().__init__()

        # OPENING WINDOW SIZE
        self.title("Login")
        self.geometry(f"{1240}x{720}")
        self.bg_image = customtkinter.CTkImage(Image.open("Image/Background_gradient.jpg"), size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # LOGIN FRAME INSIDE WINDOW
        # TEXT: "Welcome!\nUnified Travelling & Transport System"
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=15)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(
            self.login_frame,
            text="Welcome!\n",
            font=customtkinter.CTkFont(size=24, weight="bold", slant="roman", family="Helvetica"),
        )
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))

        # TEXT: LOGIN PAGE
        self.login_label_2 = customtkinter.CTkLabel(self.login_frame, text="Login Page", font=customtkinter.CTkFont(size=40, weight="bold"))
        self.login_label_2.grid(row=1, column=0, padx=30, pady=(50, 15))

        # TEXT: USERNAME
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=300, placeholder_text="Username")
        self.username_entry.grid(row=2, column=0, padx=30, pady=(15, 15))

        # TEXT: PASSWORD
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=300, show="*", placeholder_text="Password")
        self.password_entry.grid(row=3, column=0, padx=30, pady=(0, 15))

        # TEXT: LOGIN BUTTON TEXT
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=4, column=0, padx=30, pady=(15, 15))

        # TEXT to register
        self.login_label_3 = customtkinter.CTkLabel(
            self.login_frame, text="Register now if you don't have an account.", font=customtkinter.CTkFont(size=12, weight="normal")
        )
        self.login_label_3.grid(row=6, column=0, padx=30, pady=(20, 5))

        # TEXT: Register BUTTON TEXT
        self.register_button = customtkinter.CTkButton(self.login_frame, text="Register", command=self.register_event, width=200)
        self.register_button.grid(row=7, column=0, padx=30, pady=(0, 15))

    def login_event(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if not entered_username or not entered_password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        if self.check_credentials(entered_username, entered_password):
            self.destroy()
            print("Login successful!")
        else:
            print("Error")
            messagebox.showerror("Error", "Incorrect Username or Password")

    def register_event(self):
        def register():
            username = entry_username.get()
            password = entry_password.get()

            if not username or not password:
                messagebox.showerror("Error", "Username and password are required.")
                return

            conn = sqlite3.connect("user_database.db")
            c = conn.cursor()

            # Create table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE, password TEXT)''')

            try:
                # Insert user data into the table
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
                print("Username:", username)
                print("Password:", password)
                window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")

            conn.close()

        window = tk.Toplevel(self)
        window.title("Registration")
        window.geometry("300x200")

        label_username = tk.Label(window, text="Username:")
        label_username.pack()

        entry_username = tk.Entry(window)
        entry_username.pack()

        label_password = tk.Label(window, text="Password:")
        label_password.pack()

        entry_password = tk.Entry(window, show="*")
        entry_password.pack()

        btn_register = tk.Button(window, text="Register", command=register)
        btn_register.pack()

    def check_credentials(self, username, password):
        conn = sqlite3.connect("user_database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()

        conn.close()

        if result:
            return True

        return False


if __name__ == "__main__":
    app = Login()
    app.mainloop()
