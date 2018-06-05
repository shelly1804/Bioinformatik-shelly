def hammingDistance(p,q):
    ham = 0
    for x, y in zip(p,q):
        if x != y:
            ham += 1
    return ham

def distanceBetweenPatternAndString(pattern, DNA):
    k = len(pattern)
    distance = 0
    for x in DNA:
        hamming = k+1
        for i in range(len(x)- k+1):
            z = hammingDistance(pattern, x[i:i+k])
            if hamming > z:
                hamming = z
        distance += hamming
    return distance

def numberToPattern(x,k):
    if k ==1:
        return numberToSymbol(x)
    return numberToPattern(x//4, k-1) + numberToSymbol(x % 4)

def numberToSymbol(x):
    if x == 0:
        return "A"
    if x == 1:
        return "C"
    if x == 2:
        return "G"
    if x == 3:
        return "T"

def medianString(DNA, k):
    distance = (k+1) * len(DNA)
    median = ""
    for i in range(4**k):
        pattern = numberToPattern(i, k)
        z = distanceBetweenPatternAndString(pattern, DNA)
        if distance > z:
            distance = z
            median = pattern
    return median

DNA =["TGATGATAACGTGACGGGACTCAGCGGCGATGAAGGATGAGT", "CAGCGACAGACAATTTCAATAATATCCGCGGTAAGCGGCGTA", "TGCAGAGGTTGGTAACGCCGGCGACTCGGAGAGCTTTTCGCT", "TTTGTCATGAACTCAGATACCATAGAGCACCGGCGAGACTCA", "ACTGGGACTTCACATTAGGTTGAACCGCGAGCCAGGTGGGTG", "TTGCGGACGGGATACTCAATAACTAAGGTAGTTCAGCTGCGA", "TGGGAGGACACACATTTTCTTACCTCTTCCCAGCGAGATGGC", "GAAAAAACCTATAAAGTCCACTCTTTGCGGCGGCGAGCCATA", "CCACGTCCGTTACTCCGTCGCCGTCAGCGATAATGGGATGAG", "CCAAAGCTGCGAAATAACCATACTCTGCTCAGGAGCCCGATG"]
k = 6
print(medianString(DNA, k))