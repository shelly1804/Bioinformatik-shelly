def NumberToPattern(index, k):
    if k == 1:
        return NumberToSymbol(index)
    return NumberToPattern(index // 4, k-1) + NumberToSymbol(index%4)
def NumberToSymbol(index):
    if index ==0:
        return "A"
    if index ==1:
        return "C"
    if index ==2:
        return "G"
    if index ==3:
        return "T"
print(NumberToPattern(45,4))
