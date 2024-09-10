import numpy as np
import re
from sympy import Matrix

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

def is_grammatical(char: str) -> bool:
    return not ((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or (ord(char) <= 32) or (ord(char) == 127)) 

def get_trackers(input_str: str, options: list[int]) -> tuple[list[int]|None, list[tuple[str, int]]|None, list[int]|None]:
    spaces_tracker: list[int]|None = None
    grammar_tracker: list[tuple[str, int]]|None = None
    capitals_tracker: list[int]|None = None

    if options[0] == 0:
        spaces_tracker = [int(num) for num in np.cumsum([len(word) for word in input_str.split()]) + np.cumsum([0]+[1]*(len(input_str.split())-1))][:-1]
    if options[1] == 0:
        grammar_tracker = []
        for arr in zip(input_str, range(len(input_str))):
            if is_grammatical(arr[0]):
                grammar_tracker.append((arr[0], arr[1]))
    if options[2] == 0:
        capitals_tracker = []
        for i in range(len(input_str)):
            if ord(input_str[i]) >= 65 and ord(input_str[i]) <= 90:
                capitals_tracker.append(i)

    return spaces_tracker, grammar_tracker, capitals_tracker

def add_trackers(spaces_tracker: list[int]|None, grammar_tracker: list[tuple[str, int]]|None, capitals_tracker: list[int]|None, input_str: str, result: list[str]) -> str:
    if grammar_tracker is not None:
        for arr in grammar_tracker:
            result.insert(arr[1] - np.sum([char == ' ' for char in input_str[:arr[1]]]), arr[0])
    
    if spaces_tracker is not None:
        if grammar_tracker is None:
            for loc in spaces_tracker:
                result.insert(loc - np.sum([is_grammatical(char) for char in input_str[:loc]]), ' ')
        else:
            for loc in spaces_tracker:
                result.insert(loc, ' ')

    if capitals_tracker is not None:
        if grammar_tracker is None and spaces_tracker is None:
            for loc in capitals_tracker:
                index: int = loc - np.sum([is_grammatical(char) for char in input_str[:loc]],dtype=int) - np.sum([char == ' ' for char in input_str[:loc]],dtype=int)
                result[index] = result[index].upper() 
        elif grammar_tracker is None:
            for loc in capitals_tracker:
                index: int = loc - np.sum([is_grammatical(char) for char in input_str[:loc]],dtype=int)
                result[index] = result[index].upper() 
        elif spaces_tracker is None:
            for loc in capitals_tracker:
                index: int = loc - np.sum([char == ' ' for char in input_str[:loc]],dtype=int)
                result[index] = result[index].upper() 
        else:
            for loc in capitals_tracker:
                result[loc] = result[loc].upper() 
    
    return ''.join(result)

def sigma_1(input: np.ndarray[int]) -> np.ndarray[int]:
    result: np.ndarray[int] = np.zeros((len(input)),dtype=int)
    result[0] = input[0]
    for i in range(1,len(input)):
        result[i] = input[i] + input[i-1]
    return result

Mat: np.ndarray[int] = np.asarray([[]])
Mat_inv: np.ndarray[int] = np.asarray([[]])

def sigma_1_inverse(input: np.ndarray[int]) -> np.ndarray[int]:
    global Mat, Mat_inv
    if len(Mat[0,:]) != len(input):
        Mat = np.zeros((len(input), len(input)), dtype=int)
        Mat[0,0] = 1
        for i in range(1,len(input)):
            Mat[i, i] = 1
            Mat[i, i-1] = 1
        Mat_inv = np.asarray(Matrix(np.concatenate((Mat,np.identity(len(input), dtype=int)), axis=1,dtype=int)).rref()[0])[:,len(input):]
    return Mat_inv @ input

def block_permutation(input: np.ndarray) -> np.ndarray:
    input_length: int = len(input)
    result: np.ndarray[int] = np.zeros((input_length),dtype=int)

    for i in range(0, (input_length//4)*4, 4):
        result[i],result[i+1],result[i+2],result[i+3] = input[i+1],input[i+3],input[i],input[i+2]
    
    if input_length % 4 == 1:
        result[-1] = input[-1]
    elif input_length % 4 == 2:
        result[-1],result[-2] = input[-2],input[-1]
    elif input_length % 4 == 3:
        result[-1],result[-2],result[-3] = input[-3],input[-1],input[-2]

    return result

def block_permutation_inverse(input: np.ndarray) -> np.ndarray:
    input_length: int = len(input)
    result: np.ndarray[int] = np.zeros((input_length),dtype=int)

    for i in range(0, (input_length//4)*4, 4):
        result[i],result[i+1],result[i+2],result[i+3] = input[i+2],input[i],input[i+3],input[i+1]

    if input_length % 4 == 1:
        result[-1] = input[-1]
    elif input_length % 4 == 2:
        result[-1],result[-2] = input[-2],input[-1]
    elif input_length % 4 == 3:
        result[-1],result[-2],result[-3] = input[-2],input[-3],input[-1]

    return result

def block_permutation_2(input: np.ndarray) -> np.ndarray:
    input_length: int = len(input)
    result = np.zeros((input_length), dtype=int)

    for i in range(0, (input_length//5)*5, 5):
        result[i],result[i+1],result[i+2],result[i+3],result[i+4] = input[i+2],input[i+4],input[i+3],input[i],input[i+1]

    if input_length % 5 == 1:
        result[-1] = input[-1]
    elif input_length % 5 == 2:
        result[-1],result[-2] = input[-2],input[-1]
    elif input_length % 5 == 3:
        result[-1],result[-2],result[-3] = input[-2],input[-3],input[-1]
    elif input_length % 5 == 4:
        result[-1],result[-2],result[-3],result[-4] = input[-4],input[-3],input[-2],input[-1]
    
    return result

def block_permutation_inverse_2(input: np.ndarray) -> np.ndarray:
    input_length: int = len(input)
    result = np.zeros((input_length), dtype=int)

    for i in range(0, (input_length//5)*5, 5):
        result[i],result[i+1],result[i+2],result[i+3],result[i+4] = input[i+3],input[i+4],input[i],input[i+2],input[i+1]

    if input_length % 5 == 1:
        result[-1] = input[-1]
    elif input_length % 5 == 2:
        result[-1],result[-2] = input[-2],input[-1]
    elif input_length % 5 == 3:
        result[-1],result[-2],result[-3] = input[-3],input[-1],input[-2]
    elif input_length % 5 == 4:
        result[-1],result[-2],result[-3],result[-4] = input[-4],input[-3],input[-2],input[-1]

    return result

# This function is it's own inverse
def block_permutation_3(input: np.ndarray) -> np.ndarray:
    input_length: int = len(input)
    result = np.zeros((input_length),dtype=int)

    for i in range(0, (input_length//4)*4, 4):
        result[i],result[i+1],result[i+2],result[i+3] = input[i+2],input[i+3],input[i],input[i+1]

    if input_length % 4 == 1:
        result[-1] = input[-1]
    elif input_length % 4 == 2:
        result[-1],result[-2] = input[-2],input[-1]
    elif input_length % 4 == 3:
        result[-1],result[-2],result[-3] = input[-2],input[-1],input[-3]

    return result

# For Testing Purposes Only
if __name__ == "__main__":
    ...