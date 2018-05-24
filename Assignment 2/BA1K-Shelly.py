def patternToNumber(pattern):
    if len(pattern) == 0:
        return 0
    return 4 * patternToNumber(pattern[0:-1]) + symbolToNumber(pattern[-1:])
def symbolToNumber(symbol):
    if symbol == "A":
        return 0
    if symbol == "C":
        return 1
    if symbol == "G":
        return 2
    if symbol =="T":
        return 3
text= 'ACGCGGCTCTGAAA'
k= 2
y= [0] * 4**k
for i in range(len(text)-k+1):
    pattern = text[i:i+k]
    j = patternToNumber(pattern)
    y[j]= y[j] +1
f=""
for i in y:
    f+= str(i) + " "
print(f)
