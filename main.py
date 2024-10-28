from tkinter import Canvas, PhotoImage, Tk, Label, Entry, StringVar, Button, messagebox
from random import randint, choice, shuffle
import pyperclip

# Constants for password generation
MIN_LETTERS = 8
MAX_LETTERS = 10
MIN_NUMBERS = 2
MAX_NUMBERS = 4
MIN_SYMBOLS = 2
MAX_SYMBOLS = 4


def main():
    """Main function to run the Password Manager application."""
    # Initialize the main window
    window = Tk()
    window.title("Password Manager")
    window.config(pady=20, padx=20)

    # Create and place a canvas with a logo image
    canvas = Canvas(width=200, height=200)
    image_path = "logo.png"
    photo = PhotoImage(file=image_path)
    canvas.create_image(100, 100, image=photo)
    canvas.grid(row=0, column=1)

    # Create labels for website, email, and password
    website_label = Label(text="Website: ")
    website_label.grid(row=1, column=0, sticky='w')  # Align to the west (left)
    email_label = Label(text='Email/UserName: ')
    email_label.grid(row=2, column=0, sticky='w')
    password_label = Label(text='Password: ')
    password_label.grid(row=3, column=0, sticky='w')

    # Entry fields for user input
    web = StringVar()
    website_entry = Entry(window, textvariable=web, width=35)
    website_entry.grid(row=1, column=1, columnspan=2)
    website_entry.focus()

    email_entry = Entry(width=35)
    email_entry.grid(row=2, column=1, columnspan=2)
    email_entry.insert(0, 'your@email.com')

    password_entry = Entry(width=25)
    password_entry.grid(row=3, column=1)

    def generate_random_choices(choices, count):
        """Generate a list of random choices from a given list."""
        return [choice(choices) for _ in range(count)]

    def generate_pw():
        """Generate a random password and copy it to the clipboard."""
        password_entry.delete(0, 'end')

        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        numbers = '0123456789'
        symbols = '!#$%&()*+'

        # Generate random letters, numbers, and symbols
        password_letters = generate_random_choices(letters, randint(MIN_LETTERS, MAX_LETTERS))
        password_symbols = generate_random_choices(symbols, randint(MIN_SYMBOLS, MAX_SYMBOLS))
        password_numbers = generate_random_choices(numbers, randint(MIN_NUMBERS, MAX_NUMBERS))

        # Combine and shuffle the password components
        password_list = password_letters + password_symbols + password_numbers
        shuffle(password_list)

        # Create the final password string
        password = ''.join(password_list)
        password_entry.insert(0, password)
        pyperclip.copy(password)  # Copy the password to clipboard

    # Button to generate a password
    generate_pw_button = Button(text='Generate', width=10, command=generate_pw)
    generate_pw_button.grid(row=3, column=2)

    def save_to_file(website, email, password):
        """Append the given credentials to the data file."""
        password_unit = f'{website} | {email} | {password}\n'
        with open(file='data.txt', mode='a') as datafile:
            datafile.write(password_unit)

    def delete_field_data():
        """Clear the input fields."""
        website_entry.delete(0, 'end')
        password_entry.delete(0, 'end')

    def save():
        """Save the credentials and show a success message or handle missing fields."""
        website = website_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if not website or not email or not password:
            result = messagebox.askyesno(
                message='Are you sure you want to continue without filling in all fields?',
                icon='question', title='Confirm'
            )
            if result:
                save_to_file(website, email, password)
                messagebox.showinfo(message='New password created successfully.')
                delete_field_data()
        else:
            save_to_file(website, email, password)
            messagebox.showinfo(message='New password created successfully.')
            delete_field_data()

    # Button to save the credentials
    add_button = Button(text='Add', width=36, command=save)
    add_button.grid(row=4, column=1, columnspan=2)

    # Start the Tkinter event loop
    window.mainloop()


if __name__ == "__main__":
    main()
