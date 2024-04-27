# 1
def get_score(x: int) -> str:
    scores = {
        9: "A",
        8: "B",
        7: "C",
        6: "D",
    }

    if x > 1 or x < 0:
        return "Bad score"

    x = int(x * 10)
    return scores.get(x, "F")


# 2
import re


def is_alphabetical_order(string):
    string = string.lower()
    prev = " "

    for i in range(len(string)):
        if re.match(r"[0-9]", string[i]):
            continue
        if string[i] < prev:
            return string[i]
        prev = string[i]

    return 0


# 3
def is_palindrome(s: str) -> bool:
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])
