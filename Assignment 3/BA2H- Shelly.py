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

DNA = ["TTACCTTAAC", "GATATCTGTC", "ACGGCGTTCG", "CCCTAAAGAG", "CGTCAGAGGT"]
pattern = "AAA"
print(distanceBetweenPatternAndString(pattern, DNA))
