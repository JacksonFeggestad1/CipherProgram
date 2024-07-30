from tkinter import DISABLED, ACTIVE, END, Toplevel, Label, LEFT, SOLID

key_info = ["No Key Needed.", "No Key Needed.", "The key should be an integer.\nLarge key values will have a minimal\neffect on small plaintexts."]

def activate_cipher(CIPHER_MODE, NEED_KEY, output_field, input_field, key_field, ciphers, spaces_var, grammar_var, capital_var, error_messages):
    output_field.delete('1.0','end')
    hide_errors(error_messages)

    options = [spaces_var.get(), grammar_var.get(), capital_var.get()]

    if NEED_KEY:
        key = key_field.get('1.0','end')[:-1]

        if not key.isnumeric():
            error_messages[0].grid()
        else:
            output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end'), int(key), options))
            return

    else:
        output_field.insert(END, ciphers[CIPHER_MODE](input_field.get('1.0','end'),options))
        return
    return

def update_selection(selection_str, CIPHER_MODE, NEED_KEY, key_field, key_label, key_info_display, info_icon, spaces_option, output_field, cipher_options, error_messages):
    hide_errors(error_messages)

    output_field.delete('1.0','end')
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
        spaces_option.deselect()
        spaces_option.config(state=DISABLED)
    elif CIPHER_MODE in [2]:
        spaces_option.config(state=ACTIVE)


    return CIPHER_MODE, NEED_KEY

def copy_output_to_clipboard(root, output_field, error_messages):
    hide_errors(error_messages)
    root.clipboard_clear()
    root.clipboard_append(output_field.get('1.0', 'end'))
    return

def save_output_as_file(file_name, output_field, error_messages):
    hide_errors(error_messages)

    file_name_str = file_name.get('1.0','end')[:-1]
    file = open(file_name_str, "w")
    if file.closed:
        error_messages[1].grid()
        return 
    file.write(output_field.get('1.0','end'))
    file.close()
    return

def input_to_output_copy(input_field, output_field, error_messages):
    hide_errors(error_messages)

    input_field.delete('1.0','end')
    input_field.insert(END, output_field.get('1.0','end')[:-1])
    output_field.delete('1.0','end')
    return

def hide_errors(error_messages):
    for m in error_messages:
        m.grid_remove()
    return

def validate_key(CIPHER_MODE, key):
    if CIPHER_MODE in [0,1]:
        return True
    elif CIPHER_MODE in [2]:
        return key.is_numeric()

# Tool Tip class taken from https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
class Tool_Tip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.text = text
        return
    
    def show_tip(self):
        if self.tipwindow or not self.text:
            return
        
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x,y))
        label = Label(tw, text=self.text, justify=LEFT, background="#ffffe0", relief=SOLID, borderwidth=1,font=("tahoma","8","normal"))
        label.pack(ipadx=1)
        return
    
    def hide_tip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
        return
    
    def update_text(self, _text):
        self.text = _text
        return

def create_tool_tip(widget, text):
    tool_tip = Tool_Tip(widget, text)
    def enter(event):
        tool_tip.show_tip()
    def leave(event):
        tool_tip.hide_tip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    return tool_tip