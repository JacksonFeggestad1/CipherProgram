from tkinter import DISABLED, ACTIVE, END, Toplevel, Label, LEFT, SOLID, Text, IntVar, Checkbutton, Tk, Widget, Event
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


key_info: list[str] = ["No Key Needed.", "No Key Needed.", "The key should be an integer.\nLarge key values will have a minimal\neffect on small plaintexts.", "Key should be an integer.", "Key should be a word\nof length four or greater."]

def activate_cipher(CIPHER_MODE: int, NEED_KEY: bool, output_field: Text, input_field: Text, key_field: Text, ciphers: list[Callable], options_vars: list[IntVar], error_types: list[str], error_texts: list[str], error_label: Label) -> None:
    output_field.delete('1.0','end')
    hide_errors(error_label)

    options_vars: list[int] = [var.get() for var in options_vars]

    if NEED_KEY:
        key: str = key_field.get('1.0','end')[:-1]

        is_valid: bool; error_message: int 
        is_valid, error_message = validate_key(CIPHER_MODE, key)
        if is_valid:
            output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end'), key, options_vars))
        else:
            raise_error(0, error_message, error_types, error_texts, error_label)

    else:
        output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end'),options_vars))
        return
    return

def update_selection(selection_str: str, CIPHER_MODE: int, NEED_KEY: bool, key_field: Text, key_label: Label, key_info_display: Tool_Tip, info_icon: Label, 
                     options_gui_elements: list[Checkbutton], output_field: Text, cipher_options: list[str], error_types: list[str], error_texts: list[str], error_label: Label) -> tuple[int, bool]:
    hide_errors(error_label)

    output_field.delete('1.0','end')
    key_field.delete('1.0','end')
    CIPHER_MODE = cipher_options.index(selection_str)

    key_info_display.update_text(key_info[CIPHER_MODE])

    if CIPHER_MODE in [0,1]:
        NEED_KEY = False
    elif CIPHER_MODE in [2,3,4]:
        NEED_KEY = True

    if NEED_KEY:
        key_field.grid()
        key_label.grid()
        info_icon.grid()
    else:
        key_field.grid_remove()
        key_label.grid_remove()
        info_icon.grid_remove()

    for elem in options_gui_elements:
        elem.deselect()
        elem.config(state=ACTIVE)
    
    # Configuring cipher options
    if CIPHER_MODE in [0,1]:
        options_gui_elements[0].config(state=DISABLED)
    elif CIPHER_MODE in [2]:
        options_gui_elements[0].config(state=ACTIVE)
    elif CIPHER_MODE in [3, 4]:
        options_gui_elements[1].select()
        options_gui_elements[1].config(state=DISABLED)
        options_gui_elements[2].select()
        options_gui_elements[2].config(state=DISABLED)


    return CIPHER_MODE, NEED_KEY

def copy_output_to_clipboard(root: Tk, output_field: Text, error_label: list[Label]) -> None:
    hide_errors(error_label)
    root.clipboard_clear()
    root.clipboard_append(output_field.get('1.0', 'end'))
    return

def save_output_as_file(file_name: Text, output_field: Text, error_types: list[str], error_texts: list[str], error_label: Label) -> None:
    hide_errors(error_label)

    file_name_str: str = file_name.get('1.0','end')[:-1]
    file: TextIOWrapper = open(file_name_str, "w")
    if file.closed:
        raise_error(1,1,error_types, error_texts, error_label)
        return 
    file.write(output_field.get('1.0','end'))
    file.close()
    return

def input_to_output_copy(input_field: Text, output_field: Text, error_label: list[Label]) -> None:
    hide_errors(error_label)

    input_field.delete('1.0','end')
    input_field.insert(END, output_field.get('1.0','end')[:-1])
    output_field.delete('1.0','end')
    return

def hide_errors(error_label: Label) -> None:
    error_label.grid_remove()
    return

def raise_error(error_type: int, error_message: int, error_types: list[str], error_texts: list[str], error_label: Label) -> None:
    error_label.config(text=f'{error_types[error_type]}\n\n{error_texts[error_message]}')
    error_label.grid()
    return

def validate_key(CIPHER_MODE: int, key: str) -> tuple[bool, int]:
    if CIPHER_MODE in [0,1]:
        return True, -1
    elif CIPHER_MODE in [2, 3]:
        return key.isnumeric(), 0
    elif CIPHER_MODE in [4]:
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
