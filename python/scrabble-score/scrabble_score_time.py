import timeit
import functools

#From commond to least commond
lctlc = {
    1  : ['A', 'E', 'I', 'O', 'U', 'L', 'N', 'R', 'S', 'T'],
    2  : ['D', 'G'],
    3  : ['B', 'C', 'M', 'P'],
    4  : ['F', 'H', 'V', 'W', 'Y'],
    5  : ['K'],
    8  : ['J', 'X'],
    10 : ['Q', 'Z'],
}

# Leter = Value
leval = {
    'A' : 1, 'E' : 1, 'I' : 1, 'O' : 1, 'U' : 1, 
    'L' : 1, 'N' : 1, 'R' : 1, 'S' : 1, 'T' : 1,

    'D' : 2, 'G' : 2,

    'B' : 3, 'C' : 3, 'M' : 3, 'P' : 3,

    'F' : 4, 'H' : 4, 'V' : 4, 'W' : 4, 'Y' : 4,

    'K' : 5,

    'J' : 8, 'X' : 8,

    'Q' : 10, 'Z' : 10
}

points = dict([(x, 1) for x in 'AEIOULNRST'] 
            + [(x, 2) for x in 'DG'] 
            + [(x, 3) for x in 'BCMP'] 
            + [(x, 4) for x in 'FHVWY'] 
            + [(x, 5) for x in 'K'] 
            + [(x, 8) for x in 'JX'] 
            + [(x, 10) for x in 'QZ'])

def score_1(word):
    points = 0
    for letter in word.upper():
        points += get_lctlc(letter)
    return points

def score_2(word):
    points = 0
    for letter in word.upper(): points+=leval.get(letter,0)
    return points

def score_3(word):
    return functools.reduce(lambda a, b : a+get_lctlc(b), word.upper(), 0)

def get_lctlc(letter):
    for points, letters in lctlc.items():
        if letter in letters: return points
    return 0

def score_4(word):
    return functools.reduce(lambda a, b : a+leval.get(b,0), word.upper(), 0)

def score_5(word):
    return sum(points[x] for x in word.upper())


if __name__=='__main__':
    
    time_1 = timeit.repeat(r'score_1("abcdefghijklmnopqrstuvwxyz")', setup='from __main__ import score_1', repeat=3, number=10000)
    time_2 = timeit.repeat(r'score_2("abcdefghijklmnopqrstuvwxyz")', setup='from __main__ import score_2', repeat=3, number=10000)
    time_3 = timeit.repeat(r'score_3("abcdefghijklmnopqrstuvwxyz")', setup='from __main__ import score_3', repeat=3, number=10000)
    time_4 = timeit.repeat(r'score_4("abcdefghijklmnopqrstuvwxyz")', setup='from __main__ import score_4', repeat=3, number=10000)
    time_5 = timeit.repeat(r'score_5("abcdefghijklmnopqrstuvwxyz")', setup='from __main__ import score_5', repeat=3, number=10000)

    print( time_1 )
    print( time_2 )
    print( time_3 )
    print( time_4 )
    print( time_5 )