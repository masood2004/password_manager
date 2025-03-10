import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import re

# Constants
FONT = ("Arial", 16)
BG_COLOR = "#2E3440"
FG_COLOR = "#D8DEE9"
BUTTON_COLOR = "#5E81AC"
ENTRY_COLOR = "#4C566A"
TEXT_COLOR = "#ECEFF4"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list.extend([random.choice(letters) for char in range(nr_letters)])
    password_list.extend([random.choice(symbols) for char in range(nr_symbols)])
    password_list.extend([random.choice(numbers) for char in range(nr_numbers)])

    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_username_input.get()
    password = password_input.get()
    updated_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if (website == "") or (password == ""):
        messagebox.showerror(title="Input Error", message="You have left some fields empty.")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror(title="Input Error", message="Please enter a valid email address.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} \nPassword: {password} \nIs it ok to save?")

        if is_ok:

            try:
                with open("passwords.txt", 'a') as pass_list:
                    pass_list.write(f"{website} | {email} | {password}\n")
            except FileNotFoundError:
                with open("passwords.txt", 'w') as pass_list:
                    pass_list.write(f"{website} | {email} | {password}\n")
            try:
                with open("passwords.json", 'r') as pass_list:
                    # Reading old data
                    data = json.load(pass_list)
            except FileNotFoundError:
                with open("passwords.json", 'w') as data_file:
                    json.dump(updated_data, data_file, indent=4)
            else:
                # Updating the old data with new data
                data.update(updated_data)
                with open("passwords.json", 'w') as data_file:
                    # Writing new data
                    json.dump(data, data_file, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website = website_input.get()
    if website != "":
        try:
            with open("passwords.txt", 'r') as pass_list:
                for line in pass_list:
                    if website in line:
                        _, email, password = line.strip().split(" | ")
                        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
                        return
            messagebox.showinfo(title="Not Found", message=f"No details for {website} found.")
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No passwords saved yet.")
    else:
        messagebox.showerror(title="Field Missing", message="Please the website's name!")

# ---------------------------- CLEAR ALL ------------------------------- #
def clear_all():
    website_input.delete(0, END)
    email_username_input.delete(0, END)
    password_input.delete(0, END)

# ---------------------------- TOGGLE PASSWORD VISIBILITY ------------------------------- #
def toggle_password_visibility():
    if password_input.cget('show') == '':
        password_input.config(show='*')
        show_password_button.config(text="Show Password")
    else:
        password_input.config(show='')
        show_password_button.config(text="Hide Password")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Local Password Manager")
window.config(padx=50, pady=50, bg=BG_COLOR)
window.resizable(False, False)

canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
lock_img = PhotoImage(file="images/logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", font=FONT, bg=BG_COLOR, fg=FG_COLOR)
website_label.grid(row=1, column=0, pady=5)

email_username_label = Label(text="Email / Username:", font=FONT, bg=BG_COLOR, fg=FG_COLOR)
email_username_label.grid(row=2, column=0, pady=5)

password_label = Label(text="Password:", font=FONT, bg=BG_COLOR, fg=FG_COLOR)
password_label.grid(row=3, column=0, pady=5)

# Entries
website_input = Entry(width=34, font=FONT, bg=ENTRY_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
website_input.grid(row=1, column=1, pady=5)
website_input.focus()

email_username_input = Entry(width=51, font=FONT, bg=ENTRY_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
email_username_input.grid(row=2, column=1, columnspan=2, pady=15)
email_username_input.insert(0, "hmasood3288@gmail.com")

password_input = Entry(width=33, font=FONT, bg=ENTRY_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, show="*")
password_input.grid(row=3, column=1, pady=15)

# Buttons
search_button = Button(text="Search", width=15, font=FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, command=search_password)
search_button.grid(row=1, column=2)

password_button = Button(text="Generate Password", font=FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, command=generate_password)
password_button.grid(row=3, column=2, pady=5)

show_password_button = Button(text="Show Password", width=14, font=FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, command=toggle_password_visibility)
show_password_button.grid(row=4, column=2, pady=5)

add_button = Button(text="Add", width=50, font=FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, command=save)
add_button.grid(row=5, column=1, columnspan=2, pady=5)

clear_button = Button(text="Clear All", width=50, font=FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, command=clear_all)
clear_button.grid(row=6, column=1, columnspan=2, pady=5)

window.mainloop()