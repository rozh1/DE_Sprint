def is_palindrome(input: str) -> bool:
    result = True
    trimed_str = input.replace(' ', '')

    for i in range(0, len(trimed_str)//2):
        if (trimed_str[i] != trimed_str[-i-1]):
            result = False
            break

    return result


if (__name__ == "__main__"):
    words = [
        "aba",
        "awsswa",
        "qwerty",
        "rotator",
        "taco cat",
        "black cat"
    ]

    for word in words:
        print(f'{word}: {is_palindrome(word)}')
