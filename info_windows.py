from tkinter import *

def create_cipher_info_window(_master: Tk) -> None:
    cipher_info_window: Toplevel = Toplevel(_master)
    cipher_info_window.title("What is a cipher?")
    x:int; y:int
    x, y = 400, 400
    cipher_info_window.geometry(f"{x}x{y}")

    Label(cipher_info_window, text = "What is a cipher?", font=("Helvetica", 18, "bold")).grid(row = 0, column = 0)

    


    Button(cipher_info_window, text = "Back to the Program", command=cipher_info_window.destroy).grid(row = 5, column = 0)

    return