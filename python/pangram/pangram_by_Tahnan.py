from string import ascii_lowercase

ALPHABET = set(ascii_lowercase)

def is_pangram(string):
    return ALPHABET.issubset(string.lower())