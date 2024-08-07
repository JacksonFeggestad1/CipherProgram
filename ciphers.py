import numpy as np
import re

# options = [spaces, grammar, capitals]

def position_cipher_1(input_str: str, options: list[int]) -> str:
    input_arr: list[str] = input_str.split()
    result: str = ""
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

def cipher_by_cases_1(input_str: str, options: list[int]) -> str:
    input_arr: list[str] = input_str.split()
    result: str = ""
    word_counter:int = 1
    word: str
    for word in input_arr:
        if options[2] == 1:
            word = word.lower()
        letter_counter: int = 1
        letter: str
        for letter in word:
            num: int = ord(letter)
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

def position_cipher_2(input_str: str, key_str: str, options:list[int]) -> str:
    key: int = int(key_str)
    input_arr:list[str] = input_str.split()
    result:str = ""
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

def block_cipher_1(input_str: str, key_str: str, options: list[int]) -> str:
    '''Add way to re_add spaces to result at the end'''
    if options[0]==0:
        spaces_locations: list[int] = [int(num) for num in np.cumsum([len(word) for word in input_str.split()]) + np.cumsum([0]+[1]*(len(input_str.split())-1))][:-1]
    '''Strip out all non_alphabetic characters'''
    plaintext: str = ''.join(input_str.split()).lower()
    plaintext = ''.join(re.split(r"[^a-z]+", plaintext))
    
    blocks: list[str] = [plaintext[i: i+len(key_str)] for i in range(0,len(plaintext), len(key_str))]
    prev_block: np.ndarray|None = None

    num_blocks: np.ndarray[int] = np.asarray(list(ord_str(plaintext)) + [0]*(len(key_str) - len(blocks[-1]))).reshape((-1,len(key_str)))

    result: list[str] = []
    key_str_num: np.ndarray[int] = np.asarray([int(c) for c in key_str])

    for arr in zip(num_blocks, blocks):
        if prev_block is None:
            if len(arr[1]) < len(key_str):
                result.append(chr_str((arr[0][:len(arr[1])] + key_str_num[:len(arr[1])]) % 26))
            else:
                result.append(chr_str((arr[0] + key_str_num) % 26))
        else:
            if len(arr[1]) < len(key_str):
                result.append(chr_str((arr[0][:len(arr[1])] + key_str_num[:len(arr[1])] + prev_block[:len(arr[1])]) % 26))
            else:
                result.append(chr_str((arr[0] + key_str_num + prev_block) % 26))
        prev_block = arr[0]
    
    if options[0] == 0:
        temp: list[str] = list(''.join(result))
        for loc in spaces_locations:
            temp.insert(loc, ' ')
        return ''.join(temp)
    else:
        return ''.join(result)


def block_cipher_2(input_str: str, key: str, options:list[int]) -> str:

    return ""

def block_permutation(input_str: str) -> str:
    input_length: int = len(input_str)
    result: list[str] = ['0']*len(input_str)
    input: list[str] = list(input_str)

    if input_length % 4 == 0:
        for i in range(0, input_length, 4):
            result[i] = input[i+1]
            result[i+1] = input[i+3]
            result[i+2] = input[i]
            result[i+3] = input[i+2]
    else:
        for i in range(0, (input_length//4)*4, 4):
            result[i] = input[i+1]
            result[i+1] = input[i+3]
            result[i+2] = input[i]
            result[i+3] = input[i+2]
        
        if input_length % 4 == 1:
            result[-1] = input[-1]
        elif input_length % 4 == 2:
            result[-1] = input[-2]
            result[-2] = input[-1]
        elif input_length % 4 == 3:
            result[-1] = input[-3]
            result[-2] = input[-1]
            result[-3] = input[-2]

    return ''.join(result)

def ord_str(input_str: str) -> np.ndarray[int]:
    result: np.ndarray[int] = np.zeros(len(input_str), dtype=int)
    counter: int = 0
    for char in input_str:
        result[counter] = ord(char)-97
        counter += 1
    return result

def chr_str(input_nums: np.ndarray[int]) -> str:
    result: list[str] = []
    for num in input_nums:
        result.append(chr(num+97))
    return ''.join(result)

if __name__ == "__main__":
    print('\n'.join([block_permutation(string) for string in ["1234", "12345", "123456", "1234567", "12345678"]]))