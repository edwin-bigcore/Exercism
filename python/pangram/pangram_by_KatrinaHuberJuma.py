from string import ascii_lowercase


def is_pangram(sentence):
    sentence_set = set(sentence.lower())
    alpha_set = set(ascii_lowercase)

    if alpha_set - sentence_set == set([]):
        return True

    return False