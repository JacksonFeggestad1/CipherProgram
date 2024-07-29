import numpy as np

def position_cipher_1(input_str, options):
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
                letter_count -= 1
                if options[1] == 0:
                    result += letter
            letter_count += 1
        result += " "
        word_count += 1
    return result

def cipher_by_cases_1(input_str, options):
    input_arr = input_str.split()
    result = ""
    word_counter = 1
    for word in input_arr:
        letter_counter = 1
        for letter in word:
            num = ord(letter)
            if num % 2 == 1:
                if (num >= 97 and num <= 122):
                    result += f'{chr((num-letter_counter-word_counter-97)%26 + 97)}'
                elif (num >= 65 and num <= 90):
                    result += f'{chr((num-letter_counter-word_counter-65)%26 + 65)}'
                else:
                    letter_counter -= 1
                    if options[1] == 0:
                        result += letter
            elif num % 2 == 0:
                if (num >= 97 and num <= 122):
                    result += f'{chr((num+letter_counter+word_counter-97)%26 + 97)}'
                elif (num >= 65 and num <= 90):
                    result += f'{chr((num+letter_counter+word_counter-65)%26 + 65)}'
                else:
                    letter_counter -= 1
                    if options[1] == 0:
                        result += letter
            letter_counter += 1
        result += " "
        word_counter += 1
    return result

def position_cipher_2(input_str, key, options):
    input_arr = input_str.split()
    result = ""
    counter, prev_counter, loop_counter = 1, 1, 1
    for word in input_arr:
        for letter in word:
            num = ord(letter)
            prev_counter = counter
            if (num >= 97 and num <= 122):
                result += f'{chr((num-97+counter+loop_counter)%26+97)}'
            elif (num >= 65 and num <= 90):
                result += f'{chr((num-65+counter+loop_counter)%26+65)}'
            else:
                if options[1] == 0:
                    result += letter
                counter -= 1
            counter = (counter + 1) % key
            if counter == 0 and prev_counter != 0:
                loop_counter += 1
        if options[0] == 0:
            result += " "
    return result