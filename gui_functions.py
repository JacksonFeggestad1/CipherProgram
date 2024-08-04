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


key_info: list[str] = ["No Key Needed.", "No Key Needed.", "The key should be an integer.\nLarge key values will have a minimal\neffect on small plaintexts."]

def activate_cipher(CIPHER_MODE: int, NEED_KEY: bool, output_field: Text, input_field: Text, key_field: Text, ciphers: list[Callable], options_vars: list[IntVar], error_messages: list[Label]) -> None:
    output_field.delete('1.0','end')
    hide_errors(error_messages)

    options_vars: list[int] = [var.get() for var in options_vars]

    if NEED_KEY:
        key: str = key_field.get('1.0','end')[:-1]

        if validate_key(CIPHER_MODE, key):
            output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end'), int(key), options_vars))
        else:
            error_messages[0].grid()

    else:
        output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end'),options_vars))
        return
    return

def update_selection(selection_str: str, CIPHER_MODE: int, NEED_KEY: bool, key_field: Text, key_label: Label, key_info_display: Tool_Tip, info_icon: Label, 
                     options_gui_elements: list[Checkbutton], output_field: Text, cipher_options: list[str], error_messages: list[Label]) -> tuple[int, bool]:
    hide_errors(error_messages)

    output_field.delete('1.0','end')
    key_field.delete('1.0','end')
    CIPHER_MODE = cipher_options.index(selection_str)

    key_info_display.update_text(key_info[CIPHER_MODE])

    if CIPHER_MODE in [0,1]:
        NEED_KEY = False
    elif CIPHER_MODE in [2]:
        NEED_KEY = True

    if NEED_KEY:
        key_field.grid()
        key_label.grid()
        info_icon.grid()
    else:
        key_field.grid_remove()
        key_label.grid_remove()
        info_icon.grid_remove()

    if CIPHER_MODE in [0,1]:
        options_gui_elements[0].deselect()
        options_gui_elements[0].config(state=DISABLED)
    elif CIPHER_MODE in [2]:
        options_gui_elements[0].config(state=ACTIVE)


    return CIPHER_MODE, NEED_KEY

def copy_output_to_clipboard(root: Tk, output_field: Text, error_messages: list[Label]) -> None:
    hide_errors(error_messages)
    root.clipboard_clear()
    root.clipboard_append(output_field.get('1.0', 'end'))
    return

def save_output_as_file(file_name: Text, output_field: Text, error_messages: list[Label]) -> None:
    hide_errors(error_messages)

    file_name_str: str = file_name.get('1.0','end')[:-1]
    file: TextIOWrapper = open(file_name_str, "w")
    if file.closed:
        error_messages[1].grid()
        return 
    file.write(output_field.get('1.0','end'))
    file.close()
    return

def input_to_output_copy(input_field: Text, output_field: Text, error_messages: list[Label]) -> None:
    hide_errors(error_messages)

    input_field.delete('1.0','end')
    input_field.insert(END, output_field.get('1.0','end')[:-1])
    output_field.delete('1.0','end')
    return

def hide_errors(error_messages: list[Label]) -> None:
    for m in error_messages:
        m.grid_remove()
    return

def validate_key(CIPHER_MODE: int, key: str) -> bool:
    if CIPHER_MODE in [0,1]:
        return True
    elif CIPHER_MODE in [2]:
        return key.isnumeric()

def create_tool_tip(widget: Widget, text: str) -> Tool_Tip:
    tool_tip: Tool_Tip = Tool_Tip(widget, text)
    def enter(event: Event) -> None:
        tool_tip.show_tip()
    def leave(event: Event) -> None:
        tool_tip.hide_tip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    return tool_tip