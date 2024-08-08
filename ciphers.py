import numpy as np
from cipher_helpers import *

# options = [spaces, grammar, capitals]

# ------------- Ciphers --------------

def position_cipher_1(input_str: str, options: list[int]) -> str:
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
                result.append(f'{chr((num - 97 + word_count + letter_count)%26 + 97)}')
            elif(num >= 65 and num <= 90):
                result.append(f'{chr((num - 65 + word_count + letter_count)%26 + 65)}')
            else:
                letter_count -= 1
                if options[1] == 0:
                    result.append(letter)
            letter_count += 1
        result.append(' ')
        word_count += 1
    return ''.join(result)

def cipher_by_cases_1(input_str: str, options: list[int]) -> str:
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
                    result.append(f'{chr((num-letter_counter-word_counter-97)%26 + 97)}')
                elif (num >= 65 and num <= 90):
                    result.append(f'{chr((num-letter_counter-word_counter-65)%26 + 65)}')
                else:
                    letter_counter -= 1
                    if options[1] == 0:
                        result.append(letter)
            elif word_counter % 2 == 0:
                if (num >= 97 and num <= 122):
                    result.append(f'{chr((num+letter_counter+word_counter-97)%26 + 97)}')
                elif (num >= 65 and num <= 90):
                    result.append(f'{chr((num+letter_counter+word_counter-65)%26 + 65)}')
                else:
                    letter_counter -= 1
                    if options[1] == 0:
                        result.append(letter)
            letter_counter += 1
        result.append(" ")
        word_counter += 1
    return ''.join(result)

def position_cipher_2(input_str: str, key_str: str, options:list[int]) -> str:
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
                result.append(f'{chr((num-97+counter+loop_counter)%26+97)}')
            elif (num >= 65 and num <= 90):
                result.append(f'{chr((num-65+counter+loop_counter)%26+65)}')
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

def block_cipher_1(input_str: str, key_str: str, options: list[int]) -> str:
    '''Add way to re_add spaces to result at the end'''
    if options[0]==0:
        spaces_locations: list[int] = [int(num) for num in np.cumsum([len(word) for word in input_str.split()]) + np.cumsum([0]+[1]*(len(input_str.split())-1))][:-1]
    
    blocks: list[str]; num_blocks: np.ndarray[int]; key_str_num: np.ndarray[int]
    blocks, num_blocks, key_str_num = blockify(input_str, key_str)
    result: list[str] = []
    
    prev_block: np.ndarray[int]|None = None
    for arr in zip(num_blocks, blocks):
        if prev_block is None:
            if len(arr[1]) < len(key_str):
                prev_block = (arr[0][:len(arr[1])] + key_str_num[:len(arr[1])]) % 26
                result.append(chr_str(prev_block))
            else:
                prev_block = (arr[0] + key_str_num) % 26
                result.append(chr_str(prev_block))
        else:
            if len(arr[1]) < len(key_str):
                prev_block = (arr[0][:len(arr[1])] + key_str_num[:len(arr[1])] + prev_block[:len(arr[1])]) % 26
                result.append(chr_str(prev_block))
            else:
                prev_block = (arr[0] + key_str_num + prev_block) % 26
                result.append(chr_str(prev_block))
    
    if options[0] == 0:
        temp: list[str] = list(''.join(result))
        for loc in spaces_locations:
            temp.insert(loc, ' ')
        return ''.join(temp)
    else:
        return ''.join(result)


def block_cipher_2(input_str: str, key: str, options:list[int]) -> str:
    '''Add way to re_add spaces to result at the end'''
    if options[0]==0:
        spaces_locations: list[int] = [int(num) for num in np.cumsum([len(word) for word in input_str.split()]) + np.cumsum([0]+[1]*(len(input_str.split())-1))][:-1]

    blocks: list[str]; num_blocks: np.ndarray[int]; key_str_num: np.ndarray[int]
    blocks, num_blocks, key_str_num = blockify(input_str, key)
    result: list[str] = []
    prev_block: np.ndarray[int]|None = None

    for arr in zip(num_blocks, blocks):
        if prev_block is None:
            if len(arr[1]) < len(key):
                result.append(chr_str((block_permutation(arr[0][:len(arr[1])]) + key_str_num[:len(arr[1])]) % 26))
            else:
                result.append(chr_str((block_permutation(arr[0]) + key_str_num) % 26))
        else:
            if len(arr[1]) < len(key):
                result.append(chr_str((block_permutation(arr[0][:len(arr[1])]) + key_str_num[:len(arr[1])] + prev_block[:len(arr[1])]) % 26))
            else:
                result.append(chr_str((block_permutation(arr[0]) + key_str_num + prev_block) % 26))
        prev_block = arr[0]

    if options[0] == 0:
        temp: list[str] = list(''.join(result))
        for loc in spaces_locations:
            temp.insert(loc, ' ')
        return ''.join(temp)
    else:
        return ''.join(result)
    
def block_cipher_3(input_str: str, key: str, options: list[int]) -> str:
    if options[0]==0:
        spaces_locations: list[int] = [int(num) for num in np.cumsum([len(word) for word in input_str.split()]) + np.cumsum([0]+[1]*(len(input_str.split())-1))][:-1]

    blocks: list[str]; num_blocks: np.ndarray[int]; key_str_num: np.ndarray[int]
    blocks, num_blocks, key_str_num = blockify(input_str, key)
    result: list[str] = []
    prev_block: np.ndarray[int]|None = None

    for arr in zip(num_blocks, blocks):
        if prev_block is None:
            if len(arr[1]) < len(key):
                prev_block = (block_permutation(arr[0][:len(arr[1])]) + key_str_num[:len(arr[1])]) % 26
                result.append(chr_str(prev_block))
            else:
                prev_block = (block_permutation(arr[0]) + key_str_num) % 26
                result.append(chr_str(prev_block))
        else:
            if len(arr[1]) < len(key):
                prev_block = (block_permutation(arr[0][:len(arr[1])]) + prev_block[:len(arr[1])]) % 26
                result.append(chr_str(prev_block))
            else:
                prev_block = (block_permutation(arr[0]) + prev_block) % 26
                result.append(chr_str(prev_block))

    if options[0] == 0:
        temp: list[str] = list(''.join(result))
        for loc in spaces_locations:
            temp.insert(loc, ' ')
        return ''.join(temp)
    else:
        return ''.join(result)
