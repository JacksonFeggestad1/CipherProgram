import numpy as np

def position_cipher_1(input_str):
    input_arr = input_str.split()
    result = ""
    word_count = 1
    for word in input_arr:
        letter_count = 1
        for letter in word:
            num = ord(letter)
            if (num >= 97 and num <= 122):
                result += f'{chr((num - 97 + word_count + letter_count)%26 + 97)}'
            elif(num >= 65 and num <= 90):
                result += f'{chr((num - 65 + word_count + letter_count)%26 + 65)}'
            else:
                result += letter
            letter_count += 1
        result += " "
        word_count += 1
    return result