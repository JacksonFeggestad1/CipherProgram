from tkinter import *
from ciphers import position_cipher_1

CIPHER_MODE = 0

ciphers = [position_cipher_1]
cipher_options = ["Staircase Cipher"]

def activate_cipher():
    output_field.delete('1.0','end')
    output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end')))

def update_selection(selection_str):
    CIPHER_MODE = cipher_options.index(selection_str)

root = Tk()
root.geometry("800x300")
root.minsize(800, 300)
root.maxsize(800, 300)

#-------------Labels--------------
title_label = Label(root, text="Welcom to Ed's \nCipher Machine!", font=("Impact", 30))
input_label = Label(root, text="Input", font=("Impact",12))
output_label = Label(root, text="Output", font=("Impact", 12))

#-----------Text Fields-----------
input_field = Text(root, height=3, width=30)
input_field.insert(END, "Enter your input here")

output_field = Text(root, height=3, width=30)
output_field.insert(END, "Your output here")

#------------Buttons--------------
cipher_button = Button(root, text="Activate Cipher", command=activate_cipher)

#-----------Drop Down-------------
selected_cipher = StringVar()
selected_cipher.set(cipher_options[0])
cipher_selection = OptionMenu(root, selected_cipher, *cipher_options, command=lambda x: update_selection(x))

#---------Grid Positioning--------
title_label.grid(row = 0, column = 1)
input_label.grid(row = 1, column = 0)
output_label.grid(row = 1, column = 2)

input_field.grid(row = 2, column = 0)
output_field.grid(row = 2, column = 2)

cipher_button.grid(row = 2, column = 1)

cipher_selection.grid(row = 3, column = 1)

root.mainloop()