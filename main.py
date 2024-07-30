from tkinter import *
from ciphers import *
from gui_functions import *

CIPHER_MODE = 0
NEED_KEY = False

ciphers = [position_cipher_1, cipher_by_cases_1, position_cipher_2]
cipher_options = ["Staircase Cipher", "Cipher in Parts", "Cycle Cipher"]

def activate_cipher_helper():
    global CIPHER_MODE, NEED_KEY, output_field, input_field, key_field, ciphers, spaces_var, grammar_var, capital_var, error_messages
    activate_cipher(CIPHER_MODE, NEED_KEY, output_field, input_field, key_field, ciphers, spaces_var, grammar_var, capital_var, error_messages)
    return 

def update_helper(selection_str):
    global CIPHER_MODE, NEED_KEY, key_field, key_label, spaces_option, output_field, cipher_options, error_messages
    CIPHER_MODE, NEED_KEY = update_selection(selection_str, CIPHER_MODE, NEED_KEY, key_field, key_label, spaces_option, output_field, cipher_options, error_messages)
    return

def copy_output_to_clipboard_helper():
    global root, output_field, error_messages
    copy_output_to_clipboard(root, output_field, error_messages)
    return

def save_output_as_file_helper():
    global file_name, output_field, error_messages
    save_output_as_file(file_name, output_field, error_messages)
    return

def input_to_output_copy_helper():
    global input_field, output_field, error_messages
    input_to_output_copy(input_field, output_field, error_messages)
    return

root = Tk()
root.geometry("950x400")
root.minsize(950, 400)
root.maxsize(950, 400)

#-------------Frames--------------
left_frame = Frame(root)
central_frame = Frame(root)
right_frame = Frame(root)

#-------Populate Left Frame-------
input_field = Text(left_frame, height=10, width=40)
input_field.insert(END, "Enter your input here.")

input_label = Label(left_frame, text="Input", font=("Impact",16))

key_field = Text(left_frame, height=2, width = 20)
key_field.insert(END, "Enter your key here.")

key_label = Label(left_frame, text="Key", font=("Impact", 13))

key_error = Label(left_frame, text="Key Must Be Numeric", font=("Impact",13), fg='#f00')

#-------Position Left Frame-------

left_frame.grid(row = 1, column = 0)

#    <<<<<Left Frame>>>>>

input_label.grid(row = 1, column = 0)

key_label.grid(row = 3, column = 0)
key_error.grid(row=5, column = 0)

input_field.grid(row = 2, column = 0)
key_field.grid(row = 4, column = 0)

#------Populate Central Frame-----
cipher_frame = Frame(central_frame)

cipher_button = Button(cipher_frame, text="Activate Cipher", command=activate_cipher_helper)

exit_button = Button(central_frame, text = "Exit", command=root.quit)

encrypt_decrypt_mode_label = Label(central_frame, text = "Mode: Encrypt")

selected_cipher = StringVar()
selected_cipher.set(cipher_options[0])
cipher_selection = OptionMenu(cipher_frame, selected_cipher, *cipher_options, command=lambda x: update_helper(x))

options_frame = Frame(central_frame)

spaces_var = IntVar()
spaces_option = Checkbutton(options_frame, text = "Ignore Spaces", variable=spaces_var, state=DISABLED)

grammar_var = IntVar()
grammar_option = Checkbutton(options_frame, text = "Ignore Grammatical Symbols", variable=grammar_var)

capital_var = IntVar()
capital_option = Checkbutton(options_frame, text = "Ignore Capitalization", variable = capital_var)

#------Position Central Frame-----

central_frame.grid(row = 1, column = 1)

#    <<<<<Central Frame>>>>>

encrypt_decrypt_mode_label.grid(row = 0,column = 0, padx = (100,100))

cipher_frame.grid(row=1, column = 0, padx = (30, 30), pady = (50, 20))

options_frame.grid(row = 2, column = 0)

exit_button.grid(row=3, column = 0, pady = (30, 0))

#    <<<<<Cipher Frame>>>>>

cipher_button.grid(row = 0, column = 0)

cipher_selection.grid(row = 0, column = 1)

#    <<<<<Options Frame>>>>>

spaces_option.grid(row = 0, column = 0)

grammar_option.grid(row = 1, column = 0)

capital_option.grid(row = 2, column = 0)

#-------Populate Right Frame------

output_label = Label(right_frame, text="Output", font=("Impact", 16))

output_field = Text(right_frame, height=10, width=40)
output_field.insert(END, "Your output here.")

output_save_frame = Frame(right_frame)

copy_button = Button(output_save_frame, text = "Copy Output\nto Clipboard", command = copy_output_to_clipboard_helper)

file_save_frame = Frame(output_save_frame)

file_name = Text(file_save_frame, height=1, width=10)
file_name.insert(END, "File Name")

file_save_button = Button(file_save_frame, text = "Save Output to File", command=save_output_as_file_helper)

file_error_label = Label(output_save_frame, text = "Invalid File Name", fg="#f00")

output_to_input_button = Button(output_save_frame, text = "Copy Output\nto Input", command = input_to_output_copy_helper)

#-------Position Right Frame------

right_frame.grid(row = 1, column = 2)

#    <<<<<Right Frame>>>>>
output_label.grid(row = 1, column = 0)

output_field.grid(row = 2, column = 0)

output_save_frame.grid(row = 3, column = 0)

#    <<<<<Output Save Frame>>>>>
copy_button.grid(row = 0, column = 0)

output_to_input_button.grid(row = 0, column = 1)

file_save_frame.grid(row = 0, column = 2)

#    <<<<<File Save Frame>>>>>
file_name.grid(row = 0, column = 0)

file_save_button.grid(row = 1, column = 0)

file_error_label.grid(row = 2, column = 0)

#-----------Title-----------------
title_label = Label(root, text="Welcom to Ed's \nCipher Machine!", font=("Impact", 30))
title_label.grid(row = 0, column = 1)


#------Make Things Invisible------
key_field.grid_remove()
key_label.grid_remove()
key_error.grid_remove()
file_error_label.grid_remove()

error_messages = [key_error, file_error_label]

def hide_errors():
    global error_messages
    for m in error_messages:
        m.grid_remove()

root.mainloop()