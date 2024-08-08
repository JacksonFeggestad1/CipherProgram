import numpy as np
import re

def blockify(input_str: str, key: str) -> tuple[list[str], np.ndarray[int], np.ndarray[int]]:
    '''Strip out all non_alphabetic characters'''
    plaintext: str = ''.join(input_str.split()).lower()
    plaintext = ''.join(re.split(r"[^a-z]+", plaintext))
    
    blocks: list[str] = [plaintext[i: i+len(key)] for i in range(0,len(plaintext), len(key))]

    num_blocks: np.ndarray[int] = np.asarray(list(ord_str(plaintext)) + [0]*(len(key) - len(blocks[-1]))).reshape((-1,len(key)))
    if key.isnumeric():
        key_str_num: np.ndarray[int] = np.asarray([int(c) for c in key])
    else:
        key_str_num: np.ndarray[int] = np.asarray([ord(c)-97 for c in key])

    return blocks, num_blocks, key_str_num


def block_permutation(input_str: np.ndarray[int]) -> np.ndarray:
    input_length: int = len(input_str)
    result: np.ndarray[int] = np.zeros((input_length),dtype=int)
    input: list[int] = list(input_str)

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

    return result

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