def IsCARD_VALID(CardNO: str) -> bool:
    multiply = 0
    for enum, number in enumerate(CardNO):
        if int(enum) % 2 == 0:
            if int(number) * 2 > 9:
                multiply += (int(number) * 2) - 9
            else:
                multiply += int(number) * 2
        else:
            multiply += int(number)
    if multiply % 10 == 0:
        return True
    else:
        return False
