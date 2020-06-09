import numpy as np
import math


# GENERAL FUNCTIONS


def read_file(path):
    plain_text = open(path, "r")
    plain_message = []
    last_char = None
    for line in plain_text:
        line = line.upper()
        last_char = line[-1]
        plain_message.append(line[:-1])
    plain_text.close()
    plain_message[-1] += last_char
    return plain_message


def write_file(cipher_message, path):
    cipher_text = open(path, "w")
    for cipher_word in cipher_message:
        cipher_text.write(cipher_word+"\n")
    cipher_text.close()

# CAESAR_CIPHER


def caesar_cipher(key):
    plain_message = read_file("./Input Files/Caesar/caesar_plain.txt")
    cipher_message = []
    for word in plain_message:
        cipher_word = ""
        for char in word:
            if(not char.isalpha()):
                continue
            cipher_word += chr((ord(char) - ord('A') + key) % 26 + ord('A'))
        cipher_message.append(cipher_word)
    write_file(cipher_message, "./output/caesar.txt")

# PLAYFAIR


def initialize_key(key):
    temp_key = "".join(dict.fromkeys(key))
    key=""
    for char in temp_key:
        if 65 <= ord(char) <= 91:
            key += char
    for char in range(65, 91):
        if chr(char) not in key and chr(char) != 'J':
            key += chr(char)
    return key


def construct_matrix(key):
    matrix = []
    key = initialize_key(key)
    k = 0
    for _ in range(5):
        row = []
        for _ in range(5):
            row.append(key[k])
            k += 1
        matrix.append(row)
    return matrix


def make_pairs(plain_message):
    paired_plain = []
    for word in plain_message:
        paired_word = word[0]
        for c in range(1, len(word)):
            if word[c] == word[c-1]:
                paired_word += "X"+word[c]
            else:
                paired_word += word[c]
        if len(paired_word) % 2 == 1:
            paired_word += "X"
        paired_plain.append(paired_word)
    return paired_plain


def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i, x.index(v)
    print("failed")


def play_fair(key):
    matrix = construct_matrix(key)
    plain_message = read_file("./Input Files/PlayFair/playfair_plain.txt")
    plain_message = make_pairs(plain_message)
    # print(plain_message)
    cipher_message = []
    for word in plain_message:
        cipher_word = ""
        for (char1, char2) in zip(word[0::2], word[1::2]):
            if char1 == "J":
                char1 = "I"
            if char2 == "J":
                char2 = "I"
            c11, c12 = index_2d(matrix, char1)# char1 and char2 indices
            c21, c22 = index_2d(matrix, char2)
            if c11 == c21:
                new_char1 = matrix[c11][(c12+1) % 5]
                new_char2 = matrix[c21][(c22 + 1) % 5]
            elif c12 == c22:
                new_char1 = matrix[(c11+1) % 5][c12]
                new_char2 = matrix[(c21+1) % 5][c22]
            else:
                new_char1 = matrix[c11][c22]
                new_char2 = matrix[c21][c12]
            cipher_word += new_char1+new_char2
        cipher_message.append(cipher_word)
    write_file(cipher_message, "./output/playfair.txt")

# HILL CIPHER


def init_hill(key):
    matrix = np.array(key)
    if len(key) == 4:
        matrix = matrix.reshape((2, 2))
        plain_message = read_file("./Input Files/Hill/hill_plain_2x2.txt")
    elif len(key) == 9:
        matrix = matrix.reshape((3, 3))
        plain_message = read_file("./Input Files/Hill/hill_plain_3x3.txt")
    else:
        print("invalid input")
        raise RuntimeError
    return matrix, plain_message


def modify_input(plain_message, size):
    modified_plain = []
    for word in plain_message:
        n = int(math.sqrt(size) - len(word) % math.sqrt(size))
        word += "X"*n
        modified_plain.append(word)
    num_plain = []
    for word in modified_plain:
        num_word = []
        for char in word:
            num_word.append(ord(char)-ord("A"))
        num_plain.append(num_word)
    return num_plain


def mod_26(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] %= 26
    return matrix


def encrypt_2d(plain_message, matrix):
    matrix = np.array(matrix)
    cipher_message = []
    for word in plain_message:
        cipher_word = []
        for (char1, char2) in zip(word[0::2], word[1::2]):
            new_chars = matrix.dot(np.array([char1, char2]))
            cipher_word.extend(new_chars)
        cipher_message.append(cipher_word)
    return cipher_message


def encrypt_3d(plain_message, matrix):
    matrix = np.array(matrix)
    cipher_message = []
    for word in plain_message:
        cipher_word = []
        for (char1, char2, char3) in zip(word[0::3], word[1::3], word[2::3]):
            new_chars = matrix.dot(np.array([char1, char2, char3]))
            cipher_word.extend(new_chars)
        cipher_message.append(cipher_word)
    return cipher_message


def to_strings(message):
    new_message = []
    for i in range(len(message)):
        new_word = ""
        for j in range(len(message[i])):
            new_word += chr(message[i][j]+ord("A"))
        new_message.append(new_word)
    return new_message


def hill(key, size):
    try:
        matrix, plain_message = init_hill(key)
    except:
        return
    plain_message = modify_input(plain_message, size)
    if size == 4:
        cipher_message = encrypt_2d(plain_message, matrix)
    else:
        cipher_message = encrypt_3d(plain_message, matrix)
    cipher_message = mod_26(cipher_message)
    cipher_message = to_strings(cipher_message)
    write_file(cipher_message, "./output/hill.txt")

# Vigenere


def get_key(plain_message, init_key, mode):
    if int(mode) == 1:
        rem = len(plain_message) - len(init_key)
        key = init_key + plain_message[0:rem]
    else:
        q = int(len(plain_message)/len(init_key))
        rem = len(plain_message) - q*len(init_key)
        key = q*init_key+init_key[0:rem]
    return key


def vigenere(init_key, mode):
    plain_message = read_file("./Input Files/Vigenere/vigenere_plain.txt")
    cipher_message=[]
    for word in plain_message:
        key = get_key(word, init_key, mode)
        cipher_word=""
        for char in range(len(word)):
            if (word[char].isalpha()):
                cipher_word += chr((ord(word[char]) - 2*ord('A') + ord(key[char])) % 26 + ord('A'))
        cipher_message.append(cipher_word)
    write_file(cipher_message, "./output/vigenere.txt")

# Vernam


def vernam(init_key):
    plain_message = read_file("./Input Files/Vernam/vernam_plain.txt")
    cipher_message = []
    key=[]
    for i in range(len(init_key)):
        key.append(ord(init_key[i])-ord("A"))
    for word in plain_message:
        cipher_word = ""
        for char in range(len(word)):
            if (word[char].isalpha()):
                cipher_word += chr(((ord(word[char]) - ord('A')) ^key[char]) % 26 + ord('A'))
        cipher_message.append(cipher_word)
    write_file(cipher_message, "./output/vernam.txt")



def main():
    encryption_type = int (input("Enter algorithm number\n 1- caesar\n 2-playfair\n 3-hill\n 4-Vigenere\n 5-Vernam "))
    if encryption_type == 1:
        key = int(input("enter key"))
        caesar_cipher(key)
    elif encryption_type == 2:
        key = input("enter key")
        play_fair(key.upper())
    elif encryption_type == 3:
        key_size = int(input("Enter key size"))
        key = []
        for _ in range(key_size):
            key.append(int(input("enter a number")))
        hill(key, key_size)
    elif encryption_type == 4:
        key = input("Enter Key")
        mode = input("Enter Mode")
        vigenere(key.upper(), mode)
    elif encryption_type == 5:
        key = input("Enter Key")
        vernam(key.upper())


if __name__ == "__main__":
    main()