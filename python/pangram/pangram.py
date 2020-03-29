def is_pangram(sentence):

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    for c in sentence.replace(' ','').lower():
        alphabet = alphabet.replace(c,'')

    return alphabet==''