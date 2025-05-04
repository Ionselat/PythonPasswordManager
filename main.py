from random import randint, choice, shuffle
from tkinter import *
from tkinter import messagebox
import json
import os

FONT_NAME = "Courier"
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
#FILE_PATH = "D:/Code/Python/100DaysOfCode/day29PasswordManager/"
FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(0, randint(4, 8))]
    password_symbols = [choice(symbols) for _ in range(0, 2)]
    password_numbers = [choice(numbers) for _ in range(0, 2)]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0,"end")
    password_entry.insert(0,password)
    password_entry.clipboard_clear()
    password_entry.clipboard_append(password)

# ---------------------------- WRITE JSON TO FILE ------------------------------- #
def writeJsonFile(data):
    with open(FILE_PATH + "\\data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
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
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty")
    else:
        try:
            with open(FILE_PATH + "\\data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
                #Updating old data with new data
                data.update(new_data)
        except FileNotFoundError:
            writeJsonFile(new_data)

        else:
            data.update(data)
            writeJsonFile(data)
            
        finally:
            website_entry.delete(0,"end")
            password_entry.delete(0,"end")

# ---------------------------- CUSTOM EXCEPTIONS ------------------------------- #
class DataNotAccepted(Exception):
    pass

# ---------------------------- SEARCH PASSWORDS ------------------------------- #
def find_password():
    website = website_entry.get()
    email = email_entry.get()
    entries_found = 0
    
    try:
        if len(website) == 0 or len(email) == 0:
            raise DataNotAccepted ("Data Not Accepted")
    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found")
    except DataNotAccepted:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left website or email fields empty")
    else:
        with open(FILE_PATH + "\\data.json", "r") as data_file:
            #Reading old data
            data = json.load(data_file)
            #Search Websites For Matching Entry
            for website_name in data:
                if website_name.lower() == website.lower():
                    entries_found += 1
                    if data[website_name]["email"] == email:
                        password = data[website_name]["password"]
                        messagebox.showinfo(website_name, f"Email: {email}\nPassword: {password}")
            if entries_found == 0:
                messagebox.showerror("Error", "No details for the website exists")
    
# ---------------------------- UI SETUP ------------------------------- # 
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady= 50)
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file=FILE_PATH + "\\logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)
website_label = Label(text="Website:", font=(FONT_NAME, 10))
website_label.grid(column=0, row=1)
email_label = Label(text="Email/email:", font=(FONT_NAME, 10))
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=(FONT_NAME, 10))
password_label.grid(column=0, row=3)

website_entry = Entry(width=31)
email_entry = Entry(width=31)
password_entry = Entry(width=31)
website_entry.grid(column=1, row=1)
search_button = Button(text="Search", command=find_password, width=15)
search_button.grid(column=2, row=1)
email_entry.grid(column=1, row=2)
password_entry.grid(column=1, row=3)
website_entry.focus()
email_entry.insert(0,"ionselat@gmail.com")
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
add_button = Button(text="Add", font=(FONT_NAME, 10),width=38, command=save_password)
add_button.grid(column=1,row=4, columnspan=2)

window.mainloop()