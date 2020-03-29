
def distance(strand_a, strand_b):
    length = len(strand_a)
    if length != len(strand_b):
        raise ValueError('The Hamming distance is only '
                       + 'defined for sequences of equal length')

    distance = 0

    for i in range(length):
        if strand_a[i] != strand_b[i]: distance += 1

    return distance
