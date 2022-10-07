NUMBER_TRANSLATE = ((1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
                    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
                    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'),
                    (1, 'I'))


def numbers_to_rome(input: int) -> str:
    result = ""

    for item in NUMBER_TRANSLATE:
        for i in range(0, input//item[0]):
            result += item[1]
        input %= item[0]

    return result


if (__name__ == "__main__"):
    numbers = (
        2,
        9,
        256,
        1945
    )

    for number in numbers:
        print(f'{number}: {numbers_to_rome(number)}')
