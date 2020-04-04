import re
from collections import Counter

def is_isogram(string):
    return is_isogram_5(string) #best for True
    return is_isogram_2(string) #best for rapids falses

def is_isogram_1(string):
    chars = re.findall('([a-z])', string.lower())
    cchars = Counter(chars)
    return set(cchars.values()).difference(set([1])) == set()

def is_isogram_2(string):
    counter={}
    for c in string.lower():
        if c in [' ','-']: continue
        if c in counter: return False
        counter[c]=1
    return True

def is_isogram_3(string):
    chars=[]
    for c in string.lower():
        if c in [' ','-']: continue
        if c in chars: return False
        chars+=[c]
    return True

def is_isogram_4(string):
    string = string.lower().replace(" ","").replace("-", "")
    return False if [False for x in string if string.count(x) != 1].count(False) > 0 else True

def is_isogram_5(string):
    a =list(string.lower().replace(' ', '').replace('-', ''))
    return len(a) == len(set(a))

if __name__=='__main__':
    import timeit
    #print(is_isogram('Ss'))
    #print(is_isogram('jkfhlkdfhsafhjkdflfs'))
    #print(is_isogram('subdermatoglyphic'))
    #print(is_isogram('thumbscrew-japingly'))
    
    print(timeit.repeat("is_isogram_1('jjkfhlkdfhsafhjkdflfs')", setup="from __main__ import is_isogram_1", repeat=3, number=10000))
    print(timeit.repeat("is_isogram_2('jjkfhlkdfhsafhjkdflfs')", setup="from __main__ import is_isogram_2", repeat=3, number=10000))
    print(timeit.repeat("is_isogram_3('jjkfhlkdfhsafhjkdflfs')", setup="from __main__ import is_isogram_3", repeat=3, number=10000))
    print(timeit.repeat("is_isogram_4('jjkfhlkdfhsafhjkdflfs')", setup="from __main__ import is_isogram_4", repeat=3, number=10000))
    print(timeit.repeat("is_isogram_5('jjkfhlkdfhsafhjkdflfs')", setup="from __main__ import is_isogram_5", repeat=3, number=10000))
    
    print(timeit.repeat("is_isogram_1('thumbscrew-japingly')", setup="from __main__ import is_isogram_1", repeat=3, number=10000))
    print(timeit.repeat("is_isogram_2('thumbscrew-japingly')", setup="from __main__ import is_isogram_2", repeat=3, number=10000))
    print(timeit.repeat("is_isogram_3('thumbscrew-japingly')", setup="from __main__ import is_isogram_3", repeat=3, number=10000))
    print(timeit.repeat("is_isogram_4('thumbscrew-japingly')", setup="from __main__ import is_isogram_4", repeat=3, number=10000))
    print(timeit.repeat("is_isogram_5('thumbscrew-japingly')", setup="from __main__ import is_isogram_5", repeat=3, number=10000))