from tkinter import *
from ciphers import position_cipher_1, cipher_by_cases_1, position_cipher_2

CIPHER_MODE = 0
NEED_KEY = False

ciphers = [position_cipher_1, cipher_by_cases_1, position_cipher_2]
cipher_options = ["Staircase Cipher", "Cipher in Parts", "Cycle Cipher"]

def activate_cipher():
    global output_field, key_error, key_field, input_field, CIPHER_MODE, NEED_KEY
    output_field.delete('1.0','end')
    key_error.grid_remove()

    if NEED_KEY:
        key = key_field.get('1.0','end')[:-1]

        if not key.isnumeric():
            key_error.grid()
        else:
            output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end'), int(key)))

    else:
        output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end')))

def update_selection(selection_str):
    global CIPHER_MODE, key_field, key_label, key_error, NEED_KEY
    key_error.grid_remove()

    output_field.delete('1.0','end')
    CIPHER_MODE = cipher_options.index(selection_str)

    if CIPHER_MODE in [0,1]:
        NEED_KEY = False
    elif CIPHER_MODE in [2]:
        NEED_KEY = True

    if NEED_KEY:
        key_field.grid()
        key_label.grid()
    else:
        key_field.grid_remove()
        key_label.grid_remove()
    return

root = Tk()
root.geometry("800x300")
root.minsize(800, 300)
root.maxsize(800, 300)

#-------------Frames--------------
left_frame = Frame(root)
central_frame = Frame(root)
right_frame = Frame(root)

#-------Populate Left Frame-------
input_field = Text(left_frame, height=3, width=30)
input_field.insert(END, "Enter your input here.")

input_label = Label(left_frame, text="Input", font=("Impact",12))

key_field = Text(left_frame, height=2, width = 20)
key_field.insert(END, "Enter your key here.")

key_label = Label(left_frame, text="Key", font=("Impact", 10))

key_error = Label(left_frame, text="Key Must Be Numeric", font=("Impact",10), fg='#f00')

#-------Position Left Frame-------

left_frame.grid(row = 1, column = 0)

input_label.grid(row = 1, column = 0)

key_label.grid(row = 3, column = 0)
key_error.grid(row=5, column = 0)

input_field.grid(row = 2, column = 0)
key_field.grid(row = 4, column = 0)

#------Populate Central Frame-----
cipher_frame = Frame(central_frame)

cipher_button = Button(cipher_frame, text="Activate Cipher", command=activate_cipher)

exit_button = Button(central_frame, text = "Exit", command=root.quit)

encrypt_decrypt_mode_label = Label(central_frame, text = "Mode: Encrypt")

selected_cipher = StringVar()
selected_cipher.set(cipher_options[0])
cipher_selection = OptionMenu(cipher_frame, selected_cipher, *cipher_options, command=lambda x: update_selection(x))


#------Position Central Frame-----

central_frame.grid(row = 1, column = 1)

encrypt_decrypt_mode_label.grid(row = 0,column = 0, padx = (100,100))

cipher_frame.grid(row=1, column = 0, padx = (30, 30), pady = (50, 20))

cipher_button.grid(row = 0, column = 0)
exit_button.grid(row=5, column = 0)

cipher_selection.grid(row = 0, column = 1)

#-------Populate Right Frame------

output_label = Label(right_frame, text="Output", font=("Impact", 12))

output_field = Text(right_frame, height=3, width=30)
output_field.insert(END, "Your output here.")

output_save_frame = Frame(right_frame)

copy_button = Button(output_save_frame, text = "Copy Output to Clipboard")

#-------Position Right Frame------

right_frame.grid(row = 1, column = 2)

output_label.grid(row = 1, column = 0)

output_field.grid(row = 2, column = 0)

#-----------Title-----------------
title_label = Label(root, text="Welcom to Ed's \nCipher Machine!", font=("Impact", 30))
title_label.grid(row = 0, column = 1)


#------Make Things Invisible------
key_field.grid_remove()
key_label.grid_remove()
key_error.grid_remove()

root.mainloop()