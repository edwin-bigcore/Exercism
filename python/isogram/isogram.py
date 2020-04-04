def is_isogram(string):
    counter={}
    for c in string.lower():
        if c in [' ','-']: continue
        if c in counter: return False
        counter[c]=1
    return True