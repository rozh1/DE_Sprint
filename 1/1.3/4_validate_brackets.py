def validate(input: str) -> bool:
    opens = ("[", "(", "{")
    closes = ("]", ")", "}")
    stack = []

    for ch in input:
        if (ch in opens):
            stack.append(ch)
        if (ch in closes):
            if (len(stack) == 0): return False
            bracket = stack.pop()
            if (bracket != opens[closes.index(ch)]):
                return False
        
    return len(stack) == 0


if (__name__ == "__main__"):
    inputs = (
        "[{}({})]",
        "{]",
        "{",
        "{([][][])[]}",
        ":{[[[]]]}:",
        ")()(",
    )

    for input in inputs:
        print(f'{input}: {validate(input)}')
