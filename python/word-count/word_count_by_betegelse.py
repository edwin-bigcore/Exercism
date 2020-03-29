import string
from collections import Counter

print(Counter("testing, 1, 2 testing".translate(None, string.punctuation).lower().split()))