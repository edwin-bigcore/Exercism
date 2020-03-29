import functools 
import re

class Luhn:

    def __init__(self, card_num):
        self.card_num = card_num
        self.is_valid = None

    def valid(self):
        if self.is_valid: return self.is_valid

        self.is_valid = False

        match = re.search(r"^\d{2,}$", self.card_num.replace(' ', '') )

        if match:
            total = 0
            for i in range(len(match.string)-2, -1, -2):
                x2 = int(match.string[i] or 0) * 2
                if x2 > 9: x2 -= 9
                total += x2 + int(match.string[i+1])
            if total % 10 == 0: self.is_valid = True

        return self.is_valid  