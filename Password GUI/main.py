from tkinter import *
from tkinter import messagebox  # have to import messagebox becuz it's not a class in tkinter, its a module
from random import choice, shuffle, randint
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(5, 8))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)  # copies password to my clipboard


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    # get website entry
    website = website_entry.get()

    # look through json file using email key
    if len(website) != 0:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
                email = data[website]['email']
                password = data[website]['password']
        except FileNotFoundError:
            messagebox.showwarning('File not found Error')

        except KeyError:
            if website[0] == '':
                messagebox.showerror('Please enter valid data to search')

            else:
                messagebox.showerror("Error", "The website you searched for is not added to our DataBase.")

        else:
            pyperclip.copy(password)
            message = f"Email/Username: {email}\nPassword: {password}\n\nNote: Your password is copied to clipboard."
            messagebox.showinfo(website, message)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title='Oops', message="Please don't leave any fields empty")  # creates popups
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)  # mode='r', # Reading old data

        except FileNotFoundError:
            with open('data.json', mode='w') as data_file:  # saving all the entries to a json
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)  # Update  # Updating old data with new data

            with open("data.json", mode='w') as data_file:
                json.dump(data, data_file, indent=4)  # mode='w', # Saving updated data

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Maru Password Manager')
window.config(padx=40, pady=40)

canvas = Canvas(height=200, width=200)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# website label
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

# email label
email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)

# password label
password_label = Label(text='Password:')
password_label.grid(row=3, column=0)

# website input
website_entry = Entry()
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()

# email input, width 35
email_entry = Entry()
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, 'example@email.com')  # Use 0 to insert at beginning, Use END to insert at end

# password Entry , width 21
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, columnspan=2, sticky="EW")

# Search Button
search_button = Button(text='Search', command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

# generate Password button
password_button = Button(text='Generate Password', command=generate_password)
password_button.grid(row=3, column=2)

# add button, width 36
add_button = Button(text='Add', width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
