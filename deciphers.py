import numpy as np
from cipher_helpers import *

# options = [spaces, grammar, capitals]

def position_decipher_1(input_str: str, options: list[int]) -> str:
    input_arr: list[str] = input_str.split()
    result: list[str] = []
    word_count: int = 1
    word: str
    for word in input_arr:
        if options[2] == 1:
            word = word.lower()
        letter_count: int = 1
        letter: str
        for letter in word:
            num: int = ord(letter)
            if (num >= 97 and num <= 122):
                result.append(f'{chr((num - 97 - word_count - letter_count)%26 + 97)}')
            elif(num >= 65 and num <= 90):
                result.append(f'{chr((num - 65 - word_count - letter_count)%26 + 65)}')
            else:
                letter_count -= 1
                if options[1] == 0:
                    result.append(letter)
            letter_count += 1
        result.append(' ')
        word_count += 1
    return ''.join(result)

def decipher_by_cases_1(input_str: str, options: list[int]) -> str:
    input_arr: list[str] = input_str.split()
    result: list[str] = []
    word_counter:int = 1
    word: str
    for word in input_arr:
        if options[2] == 1:
            word = word.lower()
        letter_counter: int = 1
        letter: str
        for letter in word:
            num: int = ord(letter)
            if word_counter % 2 == 1:
                if (num >= 97 and num <= 122):
                    result.append(f'{chr((num+letter_counter+word_counter-97)%26 + 97)}')
                elif (num >= 65 and num <= 90):
                    result.append(f'{chr((num+letter_counter+word_counter-65)%26 + 65)}')
                else:
                    letter_counter -= 1
                    if options[1] == 0:
                        result.append(letter)
            elif word_counter % 2 == 0:
                if (num >= 97 and num <= 122):
                    result.append(f'{chr((num-letter_counter-word_counter-97)%26 + 97)}')
                elif (num >= 65 and num <= 90):
                    result.append(f'{chr((num-letter_counter-word_counter-65)%26 + 65)}')
                else:
                    letter_counter -= 1
                    if options[1] == 0:
                        result.append(letter)
            letter_counter += 1
        result.append(" ")
        word_counter += 1
    return ''.join(result)

def position_decipher_2(input_str: str, key_str:str, options: list[int]) -> str:
    key: int = int(key_str)
    input_arr:list[str] = input_str.split()
    result: list[str] = []
    counter: int; prev_counter: int; loop_counter: int
    counter, prev_counter, loop_counter = 1, 1, 1
    word: str
    for word in input_arr:
        if options[2] == 1:
            word = word.lower()
        letter: str
        for letter in word:
            num: int = ord(letter)
            prev_counter: int = counter
            if (num >= 97 and num <= 122):
                result.append(f'{chr((num-97-counter-loop_counter)%26+97)}')
            elif (num >= 65 and num <= 90):
                result.append(f'{chr((num-65-counter-loop_counter)%26+65)}')
            else:
                if options[1] == 0:
                    result.append(letter)
                counter -= 1
            counter = (counter + 1) % key
            if counter == 0 and prev_counter != 0:
                loop_counter += 1
        if options[0] == 0:
            result.append(" ")
    return ''.join(result)

def block_decipher_1(input_str: str, key:str, options: list[int]) -> str:

    return

def block_decipher_2(input_str: str, key:str, options: list[int]) -> str:

    return

def block_decipher_3(input_str: str, key:str, options: list[int]) -> str:

    return