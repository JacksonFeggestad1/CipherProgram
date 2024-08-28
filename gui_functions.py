from tkinter import DISABLED, ACTIVE, END, Toplevel, Label, LEFT, SOLID, Text, IntVar, Checkbutton, Tk, Widget, Event, Button, Frame
from typing import Callable
from io import TextIOWrapper


# Tool Tip class taken from https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
class Tool_Tip(object):
    def __init__(self, widget: Widget, text: str) -> None:
        self.widget: Widget = widget
        self.tipwindow: Toplevel | None = None
        self.x:int = 0
        self.y:int = 0
        self.text: str = text
        return
    
    def show_tip(self) -> None:
        if self.tipwindow or not self.text:
            return
        x:int; y:int
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + self.widget.winfo_rooty() + 27
        self.tipwindow = Toplevel(self.widget)
        tw: Toplevel = self.tipwindow
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x,y))
        label: Label = Label(tw, text=self.text, justify=LEFT, background="#ffffe0", relief=SOLID, borderwidth=1,font=("tahoma","8","normal"))
        label.pack(ipadx=1)
        return
    
    def hide_tip(self) -> None:
        tw: Toplevel = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
        return
    
    def update_text(self, _text: str) -> None:
        self.text = _text
        return


key_info: list[str] = ["No Key Needed.", "No Key Needed.", "The key should be an integer.\nLarge key values will have a minimal\neffect on small plaintexts.", "Key should be an integer.", "Key should be a word\nof length four or greater.",
                        "Key should be a word\nof length four or greater.", "Key should be a word\nof length four or greater.", "Key should be a word\nof length four or greater."]

def activate_cipher(CIPHER_MODE: int, NEED_KEY: bool, CIPHER_DECIPHER: bool, central_frame: Frame, output_field: Text, input_field: Text, key_field: Text, ciphers: list[Callable], deciphers: list[Callable],
                    options_vars: list[IntVar], error_types: list[str], error_texts: list[str], error_label: Label) -> None:
    output_field.delete('1.0','end')
    set_error_visibility(central_frame, error_label, False)

    options_vars: list[int] = [var.get() for var in options_vars]

    if NEED_KEY:
        key: str = key_field.get('1.0','end')[:-1]

        is_valid: bool; error_message: int 
        is_valid, error_message = validate_key(CIPHER_MODE, key)
        if is_valid:
            if CIPHER_DECIPHER:
                output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end'), key, options_vars))
            else:
                output_field.insert(END, deciphers[CIPHER_MODE](input_field.get('1.0','end'), key, options_vars))
        else:
            raise_error(central_frame, 0, error_message, error_types, error_texts, error_label)
    else:
        if CIPHER_DECIPHER:
            output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end'),options_vars))
        else:
            output_field.insert(END, deciphers[CIPHER_MODE](input_field.get('1.0','end'),options_vars))
    return

def update_selection(left_frame: Frame, central_frame: Frame, selection_str: str, CIPHER_MODE: int, NEED_KEY: bool, key_field: Text, key_label: Label, key_info_display: Tool_Tip, info_icon: Label, 
                     options_gui_elements: list[Checkbutton], output_field: Text, cipher_options: list[str], error_types: list[str], error_texts: list[str], error_label: Label) -> tuple[int, bool]:
    set_error_visibility(central_frame, error_label, False)

    output_field.delete('1.0','end')
    key_field.delete('1.0','end')
    CIPHER_MODE = cipher_options.index(selection_str)

    key_info_display.update_text(key_info[CIPHER_MODE])

    if CIPHER_MODE in [0,1]:
        NEED_KEY = False
    elif CIPHER_MODE in [2,3,4,5,6,7]:
        NEED_KEY = True

    if NEED_KEY:
        set_key_visibility(left_frame, key_field, key_label, info_icon, True)
    else:
        set_key_visibility(left_frame, key_field, key_label, info_icon, False)

    for elem in options_gui_elements:
        elem.deselect()
        elem.config(state=ACTIVE)
    
    # Configuring cipher options
    if CIPHER_MODE in [0,1]:
        options_gui_elements[0].config(state=DISABLED)
    elif CIPHER_MODE in [2]:
        options_gui_elements[0].config(state=ACTIVE)


    return CIPHER_MODE, NEED_KEY

def copy_output_to_clipboard(root: Tk, central_frame: Frame, output_field: Text, error_label: Label) -> None:
    set_error_visibility(central_frame, error_label, False)
    root.clipboard_clear()
    root.clipboard_append(output_field.get('1.0', 'end'))
    return

def save_output_as_file(central_frame: Frame, file_name: Text, output_field: Text, error_types: list[str], error_texts: list[str], error_label: Label) -> None:
    set_error_visibility(central_frame, error_label, False)

    file_name_str: str = file_name.get('1.0','end')[:-1]
    file: TextIOWrapper = open(file_name_str, "w")
    if file.closed:
        raise_error(central_frame, 1,1,error_types, error_texts, error_label)
        return 
    file.write(output_field.get('1.0','end'))
    file.close()
    return

def input_to_output_copy(central_frame: Frame, input_field: Text, output_field: Text, error_label: Label) -> None:
    set_error_visibility(central_frame, error_label, False)

    input_field.delete('1.0','end')
    input_field.insert(END, output_field.get('1.0','end')[:-1])
    output_field.delete('1.0','end')
    return

def raise_error(central_frame: Frame, error_type: int, error_message: int, error_types: list[str], error_texts: list[str], error_label: Label) -> None:
    error_label.config(text=f'{error_types[error_type]}\n\n{error_texts[error_message]}')
    set_error_visibility(central_frame, error_label, True)
    return

def validate_key(CIPHER_MODE: int, key: str) -> tuple[bool, int]:
    if CIPHER_MODE in [0,1]:
        return True, -1
    elif CIPHER_MODE in [2,3]:
        return key.isnumeric(), 0
    elif CIPHER_MODE in [4,5,6,7]:
        for char in key:
            if (ord(char) > 122 and ord(char) < 97) and (ord(char) > 90 and ord(char) < 65):
                return False, 2
        return len(key) >= 4, 2


def create_tool_tip(widget: Widget, text: str) -> Tool_Tip:
    tool_tip: Tool_Tip = Tool_Tip(widget, text)
    def enter(event: Event) -> None:
        tool_tip.show_tip()
    def leave(event: Event) -> None:
        tool_tip.hide_tip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    return tool_tip

def toggle_cipher_decipher(central_frame: Frame, toggle_button: Button, toggle_label: Label, CIPHER_DECIPHER: bool, error_label: Label) -> bool:
    set_error_visibility(central_frame, error_label, False)
    if CIPHER_DECIPHER:
        toggle_button.config(text = "Activate Cipher Mode")
        toggle_label.config(text = "Mode: Decipher")
    else:
        toggle_button.config(text = "Activate Decipher Mode")
        toggle_label.config(text = "Mode: Cipher")
    return not CIPHER_DECIPHER

def set_key_visibility(left_frame: Frame, key_field: Text, key_label: Label, info_icon: Label, set_visible: bool) -> None:
    if set_visible:
        key_field.grid(row = 4, column = 0)
        key_label.grid(row = 0, column = 0)
        info_icon.grid(row = 0, column = 1)

        field_height: int = key_field.winfo_reqheight()
        label_height: int = key_label.winfo_reqheight()

        left_frame.rowconfigure(3, minsize=label_height)
        left_frame.rowconfigure(4, minsize=field_height)
    else:
        key_field.grid_remove()
        info_icon.grid_remove()
        key_label.grid_remove()
    return

def set_error_visibility(central_frame: Frame, error_label: Label, set_visible: bool) -> None:
    if set_visible:
        error_label.grid(row = 3, column = 0)

        label_height: int = error_label.winfo_reqheight()

        central_frame.rowconfigure(3, minsize=label_height)
    else:
        error_label.grid_remove()

    return