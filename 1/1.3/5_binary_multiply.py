def sum(x1: str, x2: str) -> str:
    x1_len = len(x1)
    x2_len = len(x2)
    min_len = x1_len if x1_len < x2_len else x2_len

    result = []
    mem = 0

    for i in range(1, min_len+1):
        s = mem
        mem = 0

        if (x1[x1_len-i] == "1" and x2[x2_len-i] == "0" or x1[x1_len-i] == "0" and x2[x2_len-i] == "1"):
            s += 1
            if (s > 1):
                s = 0
                mem = 1

        elif (x1[x1_len-i] == "1" and x2[x2_len-i] == "1"):
            mem = 1

        result.insert(0, str(s))

    if (mem > 0):
        if (x1_len > x2_len):
            result.insert(0, sum(x1[0:x1_len-x2_len], str(mem)))
        else:
            result.insert(0, sum(x2[0:x2_len-x1_len], str(mem)))

    if (min_len == 0):
        if (x1_len > x2_len):
            result.append(x1)
        else:
            result.append(x2)

    return "".join(result)


def multiply(x1: str, x2: str) -> str:
    result = ""
    x2_len = len(x2)
    for i in range(len(x2)-1, -1, -1):
        if (x2[i] != "1"):
            continue
        iter = x1
        for _ in range(0, x2_len-i-1):
            iter += "0"
        result = sum(result, iter)

    return result


if (__name__ == "__main__"):
    numbers = (
        ("10", "1"),
        ("10", "10"),
        ("11", "11"),
        ("111", "11"),
        ("11", "111"),
        ("111", "101"),
    )

    for number in numbers:
        print(f'{number}: {multiply(*number)}')
