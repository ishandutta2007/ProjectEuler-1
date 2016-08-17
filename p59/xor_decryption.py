# xor_decryption.py
# Find the 3 letter password that will decrypt the given file
# Return sum of the letters in the decrypted text

from operator import xor
import sys
import collections

def decrypt_file (password, filename):
    
    decrypt_text = []
    password_key = []
    for ch in password:
        password_key.append (ord(ch))
        
    with open(filename, 'r') as f:
        index = 0
        for line in f:
            x1 = line.split(',')
            for x in x1:
                byte = xor (int(x), password_key[index])
                decrypt_text.append (chr (byte))
                index = (index + 1) % len(password_key)
                
    return decrypt_text

def test_for_words (test_string):
    if "the" in test_string:
        if "be" in test_string:
            if "to" in test_string:
                if "of" in test_string:
                    if "and" in test_string:
                        return 1
    return 0

def sum_letters (decrypt_list):
    letter_sum = 0
    for ch in decrypt_list:
        letter_sum += ord(ch)
    return letter_sum


input_file = "cipher.txt"
lowercase_alphabet =  range (ord('a'), ord('z')+1, 1)
for letter1 in lowercase_alphabet:
    for letter2 in lowercase_alphabet:
        for letter3 in lowercase_alphabet:
            test_password = chr(letter1) + chr(letter2) + chr(letter3)
            test_decrypt = decrypt_file (test_password, input_file)
            if test_for_words (''.join (test_decrypt)) == 1:
                print test_password
                print sum_letters (test_decrypt)
                sys.exit(0)
