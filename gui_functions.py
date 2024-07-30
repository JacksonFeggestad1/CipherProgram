from tkinter import DISABLED, ACTIVE, END

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

def update_selection(selection_str, CIPHER_MODE, NEED_KEY, key_field, key_label, spaces_option, output_field, cipher_options, error_messages):
    hide_errors(error_messages)

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