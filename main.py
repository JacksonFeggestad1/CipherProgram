from tkinter import *
from typing import Callable
from PIL import Image, ImageTk
from ciphers import *
from deciphers import *
from gui_functions import *

CIPHER_MODE: int = 0
NEED_KEY: bool = False
CIPHER_DECIPHER: bool = True    # True = Cipher; False = Decipher

ciphers: list[Callable] = [position_cipher_1, cipher_by_cases_1, position_cipher_2, block_cipher_1, block_cipher_2, block_cipher_3, block_cipher_4, block_cipher_5]
deciphers: list[Callable] = [position_decipher_1, decipher_by_cases_1, position_decipher_2, block_decipher_1, block_decipher_2, block_decipher_3, block_decipher_4, block_decipher_5]
cipher_options: list[str] = ["Staircase Cipher", "Cipher in Parts", "Cycle Cipher", "Snowball Cipher", "Shuffle Cipher", "Block Cipher III", "Block Cipher IV", "Block Cipher V"]

'''Helper is needed to assign new values to CIPHER_MODE and NEED_KEY'''
def update_helper(left_frame: Frame, central_frame: Frame, selection_str: str, key_field: Text, key_label: Label, key_info_display: Tool_Tip, info_icon: Label,
                  options_gui_elements: list[Checkbutton], output_field: Text, error_types: list[str], error_texts: list[str], error_label: Label) -> None:
    global CIPHER_MODE, NEED_KEY, cipher_options
    CIPHER_MODE, NEED_KEY = update_selection(left_frame, central_frame, selection_str, CIPHER_MODE, NEED_KEY, key_field, key_label, key_info_display, info_icon, options_gui_elements, output_field, cipher_options, error_types, error_texts, error_label)
    return

def toggle_cipher_helper(central_frame: Frame, toggle_button: Button, toggle_label: Label, error_label: Label) -> None:
    global CIPHER_DECIPHER
    CIPHER_DECIPHER = toggle_cipher_decipher(central_frame, toggle_button, toggle_label, CIPHER_DECIPHER, error_label)

def main() -> None:
    root: Tk = Tk()
    x:int; y:int
    x, y = 1000, 450
    root.geometry(f"{x}x{y}")
    root.minsize(880, 450)

    #-------------Frames--------------
    left_frame: Frame = Frame(root)
    central_frame: Frame = Frame(root)
    right_frame: Frame = Frame(root)

    #-------Populate Left Frame-------
    input_field: Text = Text(left_frame, height=10, width=33)
    input_field.insert(END, "Enter your input here.")

    input_label: Label = Label(left_frame, text="Input", font=("Impact",16))

    key_field: Text = Text(left_frame, height=2, width = 20)
    key_field.insert(END, "Enter your key here.")

    key_label_frame: Frame = Frame(left_frame)

    key_label: Label = Label(key_label_frame, text="Key", font=("Impact", 13))

    info_img: ImageTk = ImageTk.PhotoImage(Image.open("icons/info_icon.png"))
    info_icon: Label = Label(key_label_frame, image = info_img)
    key_info_display: Tool_Tip = create_tool_tip(info_icon, text = key_info[CIPHER_MODE])

    #-------Position Left Frame-------

    left_frame.grid(row = 1, column = 0, sticky='w',padx=20)

    #    <<<<<Left Frame>>>>>

    input_label.grid(row = 1, column = 0)

    key_label_frame.grid(row = 3, column = 0)

    input_field.grid(row = 2, column = 0)

    set_key_visibility(left_frame, key_field, key_label, info_icon, True)

    #------Populate Central Frame-----
    cipher_frame: Frame = Frame(central_frame)

    cipher_button: Button = Button(cipher_frame, text="Activate Cipher", command=lambda: activate_cipher(CIPHER_MODE, NEED_KEY, CIPHER_DECIPHER,central_frame, output_field, input_field, key_field, ciphers, deciphers, options_vars, error_types, error_texts, error_label))

    exit_button: Button = Button(central_frame, text = "Exit", command=root.quit)

    encrypt_decrypt_frame: Label = Label(central_frame)

    encrypt_decrypt_mode_label: Label = Label(encrypt_decrypt_frame, text = "Mode: Encrypt")

    encrypt_decrypt_toggle_button: Button = Button(encrypt_decrypt_frame, text = "Activate Decipher Mode", command = lambda: toggle_cipher_helper(central_frame, encrypt_decrypt_toggle_button, encrypt_decrypt_mode_label, error_label))

    selected_cipher: StringVar = StringVar()
    selected_cipher.set(cipher_options[0])
    cipher_selection: OptionMenu = OptionMenu(cipher_frame, selected_cipher, *cipher_options, command=lambda x: update_helper(left_frame, central_frame, x, key_field, key_label, key_info_display, info_icon, options_gui_elements,
                                                                                                                              output_field, error_types, error_texts, error_label))

    options_frame: Frame = Frame(central_frame)

    spaces_var: IntVar = IntVar()
    spaces_option: Checkbutton = Checkbutton(options_frame, text = "Ignore Spaces", variable=spaces_var, state=DISABLED)

    grammar_var: IntVar = IntVar()
    grammar_option: Checkbutton = Checkbutton(options_frame, text = "Ignore Grammatical Symbols", variable=grammar_var)

    capital_var: IntVar = IntVar()
    capital_option: Checkbutton = Checkbutton(options_frame, text = "Ignore Capitalization", variable = capital_var)

    options_gui_elements: list[Checkbutton] = [spaces_option, grammar_option, capital_option]
    options_vars: list[IntVar] = [spaces_var, grammar_var, capital_var]

    error_types: list[str] = ["Key Error", "File Error"]
    #---- Error Messages Here:
    error_texts: list[str] = ["Key must be a numeric value", "File could not be opened", "Key must be a word of\nlength four or greater."]

    error_label: Label = Label(central_frame, borderwidth = 1, background="#ffffe0", justify=CENTER, text = f'{error_types[0]}\n\n{error_texts[0]}', font=("tahoma","8"), fg="#f00000")
    #------Position Central Frame-----

    central_frame.grid(row = 1, column = 1)

    #    <<<<<Central Frame>>>>>

    encrypt_decrypt_frame.grid(row = 0,column = 0)

    cipher_frame.grid(row=1, column = 0, pady = (50, 20))

    options_frame.grid(row = 2, column = 0, padx = (20, 20))

    set_error_visibility(central_frame, error_label, True)

    exit_button.grid(row = 4, column = 0, pady = (30, 0))

    #    <<<<<Cipher Frame>>>>>

    cipher_button.grid(row = 0, column = 0)

    cipher_selection.grid(row = 0, column = 1)

    #    <<<<<Options Frame>>>>>

    spaces_option.grid(row = 0, column = 0)

    grammar_option.grid(row = 1, column = 0)

    capital_option.grid(row = 2, column = 0)

    #    <<<<<Cipher Toggle Frame>>>>>

    encrypt_decrypt_mode_label.grid(row = 0, column = 0)

    encrypt_decrypt_toggle_button.grid(row = 1, column = 0)

    #-------Populate Right Frame------

    output_label: Label = Label(right_frame, text="Output", font=("Impact", 16))

    output_field: Text = Text(right_frame, height=10, width=33)
    output_field.insert(END, "Your output here.")

    output_save_frame: Frame = Frame(right_frame)

    copy_button: Button = Button(output_save_frame, text = "Copy Output\nto Clipboard", command = lambda: copy_output_to_clipboard(root,central_frame, output_field, error_label))

    file_save_frame: Frame = Frame(output_save_frame)

    file_name: Text = Text(file_save_frame, height=1, width=10)
    file_name.insert(END, "File Name")

    file_save_button: Button = Button(file_save_frame, text = "Save Output to File", command=lambda: save_output_as_file(central_frame, file_name, output_field, error_types, error_texts, error_label))

    output_to_input_button: Button = Button(output_save_frame, text = "Copy Output\nto Input", command = lambda: input_to_output_copy(central_frame, input_field, output_field, error_label))

    #-------Position Right Frame------

    right_frame.grid(row = 1, column = 2, sticky='e',padx=20)

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

    #-----------Title-----------------
    title_label: Label = Label(root, text="Welcom to Ed's \nCipher Machine!", font=("Impact", 30))
    title_label.grid(row = 0, column = 1)


    #------Make Things Invisible------
    set_key_visibility(left_frame, key_field, key_label, info_icon, False)
    set_error_visibility(central_frame, error_label, False)

    root.columnconfigure(0,weight=1)
    root.columnconfigure(1,weight=1)
    root.columnconfigure(2,weight=1)

    root.mainloop()
    return

if __name__ == "__main__":
    main()