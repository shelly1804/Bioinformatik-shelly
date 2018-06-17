import random

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
    if symbol == "T":
        return 3

def numberToPattern(index, k):
    if k == 1:
        return numberToSymbol(index)
    return numberToPattern(index // 4, k-1) + numberToSymbol(index % 4)

def numberToSymbol(index):
    if index == 0:
        return "A"
    if index == 1:
        return "C"
    if index == 2:
        return "G"
    if index == 3:
        return "T"

def profileProbable(text, k, profile):
    maxprob = 0
    kmer = text[0:k]
    for i in range(0, len(text) - k +1):
        prob =1
        pattern =text[i:i+k]
        for j in range(k):
            l = symbolToNumber(pattern[j])
            prob *= profile [l][j]
        if prob > maxprob:
            maxprob =prob
            kmer = pattern
    return kmer

def hammingDistance(p, q):
    ham = 0
    for index, y in zip(p, q):
        if index != y:
            ham +=1
    return ham

def distanceBetweenPatternAndString(pattern, DNA):
    k = len(pattern)
    distance = 0
    for index in DNA:
        hamming = k+1
        for i in range(len(index) - k + 1):
            z = hammingDistance(pattern, index[i:i+k])
            if hamming > z:
                hamming = z
        distance += hamming
    return distance

def profileForm(motifs):
    k= len(motifs[0])
    profile = [[1 for i in range(k)] for j in range(4)]
    for index in motifs:
        for i in range(len(index)):
            j = symbolToNumber(index[i])
            profile[j][i] +=1
    for index in profile:
        for i in range(len(index)):
            index[i] = index[i]/len(motifs)
    return profile

def consensus(profile):
    str = ""
    for i in range(len(profile[0])):
        max = 0
        loc = 0
        for j in range(4):
            if profile[j][i] > max:
                loc = j
                max = profile[j][i]
        str+=numberToSymbol(loc)
    return str

def score(motifs):
    profile = profileForm(motifs)
    cons = consensus(profile)
    score = 0
    for index in motifs:
        for i in range(len(index)):
            if cons[i] != index[i]:
                score +=1
    return score

def randomMotifSearch(DNA, k, t):
    bestMotifs = []
    motifs = []
    for index in range(t):
        random.seed()
        i= random.randint(0, len(DNA[index])-k)
        motifs.append(DNA[index][i:i+k])
    bestMotifs = motifs.copy()
    count = 0
    while True:
        profile = profileForm(motifs)
        for index in range(t):
            motifs[index] = profileProbable(DNA[index], k, profile)
        if score(motifs) < score(bestMotifs):
            bestMotifs = motifs.copy()
            count +=1
        else:
            print(count)
            return bestMotifs

k = 8
t = 5
DNA = ["CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA", "GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG", "TAGTACCGAGACCGAAAGAAGTATACAGGCGT", "TAGATCAAGTTTCAGGTGCACGTCGGTGAACC", "AATCCACCAGCTCCACGTGCAATGTTGGCCTA"]
best = randomMotifSearch(DNA, k, t)
min = score(best)
for index in range(1000):
    print(index)
    a = randomMotifSearch(DNA, k, t)
    if score(a) < score(best):
        best = a
        min = score(a)
print(min)
for index in best:
    print(index)

