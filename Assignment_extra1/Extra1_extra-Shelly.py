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

def profileRandom(k,profile, text):
    probs = []
    for i in range(0, len(text) - k+1):
        prob = 1.0
        pattern = text[i:i+k]
        for j in range(k):
            l = symbolToNumber(pattern[j])
            prob *= profile[l][j]
        probs.append(prob)
    r = myRandom(probs)
    return r

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

def myRandom(dist):
    s = 0.0
    for index in dist:
        s += index
    i = random.random()
    partial = 0.0
    for index in range(len(dist)):
        partial += dist[index]
        if partial/s >= i:
            return index

def gibbsSampler(DNA, k, t, n):
    bestMotifs = []
    motifs = []
    for index in range(t):
        i = random.randint(0, len(DNA[index])-k)
        motifs.append(DNA[index][i:i+k])
    bestMotifs = motifs [:]
    for i in range(n):
        j = random.randint(0, t-1)
        profile = profileForm(motifs[:j] + motifs[j+1:])
        r = profileRandom(k, profile, DNA[j])
        motifs[j] = DNA[j][r:r+k]
        if score(motifs) < score(bestMotifs):
            bestMotifs = motifs[:]
    return bestMotifs



k = 15
t = 20
n = 2000
DNA = ["CTCTTGATTAAGGAGATGTAAAACTCTTTCCGGACATTAACTTGTCGATTGGTTCGTTTTATGATTGTTAGCCCATACAACGAGTGCTACTTTCGACGATTACCTGGCAACAATAGACAAGTCAGGGCCGCGGAAGACTGATCCCCTATACAGACCGTTATCATGCTACGAGAACGGTTGTCTAGCAACTCTTAGCTACGTGTGACGTCCACCGGCGTCGAGCCTGGCGACTATTAAATTCGCATGCGCTAAAAGCACCTGTTATAAACGGCTGTCAGCGATGTTCGGCCGATATGCGCATCTTCGTTTCCTCTTGATTAAGGAG", "ATGTAAAACTCTTTCCGGACATTAACTTGTCGATTGGTTCGTTTTATGATTGTTAGCCCATACAACGAGTGCTACTTTCGACGATTACCTGGCAACAATAGACAAGTCAGGGCCGCGGAAGACTGATCCCCTATACAGACCGTTATCATGCTACGAGAACGGTTGTCTAGCAACTCTTAGCTACGTGTGACGTCCACCGGCGTCGAGCCTGGCGACTATTAAATTCGCATGCGCTAAAAGCACCTGTTATAAACGGCTGTCAGCGATGTTCGGCCGATATGCGCATCTTCGTAAGCGCACCGGGGTGTTCCTCTTGATTAAGGAG", "GAGATGATAGGTTGGCCGGTTCGCCTCGATACGGTCCACGCCTGCTGGAATCTAGCTAGACAATTGCTTAGTGGATTCATTCTCCTCACCCCTGTAATTTACCCTTACCGGGGTGGGGAGGAAATACTCCACGTAGAACACGTTTACGAGCCTAAGGGCCGAGAATCACATAAGGCGTCTAACTATTAAGTGCCTTTGGTATCGATTATTGTGTTTTTCCCCATGCCCGCAGTCCTCCACTTAATAGACTGCTATCAACTATGGTAAATCAATTTCCACGATCGGGCTCTCGAACTTCTGTGTTATCCGATACGTCGCCGAAATC", "GCCTAATTGAATTATAAAGTATTTCGTCCGACATATCGCCATGTTGACTGTATGCGCATGGAATTCGCTTCGAGAAGTTCCTCGGGGTGAGGCACGTTTTGAAGAACCCGGAAGCTCCTTCGGTTGAGCCTAAGTTTACTCTATAGGCAATCTCACCATCCGCGTCCACCCAATCGCGTGAGGTAAGATCTAAGTCCGGCTGCAAGTATCCATAAGGCCCCTTGCGGATGGTCACGTCTCTTAGCAAGGAGTCAATGAGATCGGCCCTCCCTACCCTTAGTCTATGTTTTGGCATAAGCATTGGGAATTGTGTAGGATATGTGAG", "CGTTTCATCTACATGACATTGCTGCTACGACATGCGTGTCGCCCTCCTGGAGCCCAGTGTTGATCACCGTGGGAACGTTCCTAATAGCTGAAGTGAGGACTGGGAATTCGTTCACTTGACGTCTCACCTGTCGATTTATGCATTTGAAGCTCAATTTGGGGGTAAATTGGAATGAGAGCGAAGAGACGTTTACCTATCCTTCTAATAGGAAACTTCTAGTTGGATGATGAGATAAGTTTTATGGGGTGTATATTGGGCGTCAATGAACCCTCGCCAGTGTAAACACCAATTTCCATTGAGGTTGGGTGGTAGAGTCCGCGGGACA", "TAGACTAACCCACACGTAACCAATTGGTTTTTCGGACAGGGTGAAGGGATGTGTGCATCGAAAGTTTTTAGCTACGACTGTAATATCCACTTCACCTCTGTCCACCAGTACAATCCAGGTAATAAATCTCCTCTGGCTGGTGCTTTAAAGGGAGTCTGTTTCACGATCCTTGAACAGGTGCGTCTCACGAGGACGTGTATGAATTTTCATAATAGACGTGTTCCCGAGCCACCAACAGGAGCGTGCCTGATTCGGAAGATGCAAAGCCAATTGCATACCACCTGCACAGGAGGAGGCATGGATCGCAAGTTTACCGGGTGCAAGG", "CCTACTTGACAAGCGTAGGCGCGGTACGCAAGTGTTGCGTTCTCCCTCGCAACACCCGTCAGTGCTACGGGGACGGGTTTTACGACTTGACGCTCTTCCGGCCACCTGCATTAACTCGACGGAATGAGCACGGCTCGGTAGGCGATCGAGTATGCGTCATGGGAAAATAGGAATCGGACGCCCCTCGGGCATATTAAGCCTGCGTTCGTGTTGTCCTTACGATATTAGCCTACCAAGTTTCGAGGGGTGCCAAGCTCAAGTGATCCGGAACTTTGCTTTACCACCACCGCCATCCAGGGCATTATACATCGCTCCCTTGTGACCT", "TAATACACATCCTCGGACTCCACATGACGATACCACTAAAAAATCAACGACCTTTCGGCCGCATGATAGGTCATGAGGGGGCAGTTTATTCTCGGTTCCTGTTTACCGGGGTATGGTAAATCTGCAGGGTTGCACACCCGATCAGCTTGTAGGCTTTCGTGCTTTCAGATTTCTAACAATACGTTAAAGATTTTTGAGTTAGAGAAAGAGCGTCGAACATACTGTCGTACCAATTTACTCTTTACGATCATTCGCCCGCAGCATTCCGGTGCAATCGATTATTCGCATAGTCATTCCCCTGTTCCGTGGCTATTCTTCGTACCTT", "AATGGGATTGCTGAACAAGAAGGCGGCTTAGACTGTCTATGGCTTCCGATCGGACTAACGGCGAATAATAGTAAGATTACGGATCCCTGACAGCTTCAGTCCGCAAACGACACCACAGGCTCCTGTAGTAAAACAGACAGCCACTATAGCGCGATTGTTGGCCCCCCCTTAAGTTGCTCGGGGTGGTCCAACAGTCCCCAGAAGACATACGACGGGATGTATATAATGAAATTCGCCTTCTTTAAGAAGATGCTCTGGCAGTTTCATATAGGGGCCCGCTGTTGAAAATCGGATGAGTGAGGATACATGCGTTTGCGTTCGTGTC", "GATACTCCTATCGCGCAGTGACCTCCCTGCGTTCATATTTAGCCCTACTTTGACGAGACAGATAGCTGGGAAAGCCTATTCGACATATATACTGCGATGACTCCGGAACGTAAAAGAGTAAATCGACATATTTAGTGGCTTGGATTTGAGTAGTATCGCAACCTACGCCGATGCGGAAAATTAAACATACCGGGGTGTCCCATATGAGGGGGGCGAAATCTCCGAGGATTGAGTACTCGTGCCCCCGACTTTTTTTCGACTCGCGGCAATGAAAACCGAAGGAGGCACGAAGTGGTACATGTGTACCCCTCTTTGGTTACTCATG", "CGCAGGCTCATTCGTTCACGAACACACGGAACTACCCAGCGCGTTGATGCTCCAAAACGAGGCCACGTTCACAGAACCGAAACACCGATAAAAGCGCGCCAACAACCCGACGACGCACAGGGTGAAATGGCACTTACGGCTCTTTCATGATCTTCGACCGAAGGAATGGAGGGGGTCACCTGGCCCGGCCCGGTGAGTGCTTGTATAGGCGTTTGTACTGAGGTACCAGGACCGGGCGCTGCACAAGCTGCCATTCTAGCGTATTCTCATATCCAAATGGCTCGCAAGTTTAGGAGGGTGGGGCTCCCGCCAGGCCGTCATATCC", "ACGTTTCGCAGCTGAGGTAAGGAAACCGGGGTGGAATCACCCTCGAAGCTGGTCGCGCCGGCATCTATTGTTGAGCAGGTCATCACAATTCCTCTATTTCTATGATACAACTTCGACGATCCACGGGATATGTAACGCCGGAACACAGGAGTAAATGTGATTGACAGGGGCTCATCCGTCTGCCCAAACGGCATCTACGCAATGACTGCATAGGTTTTGTGTAAAAGAGTTTGTCATCTACCCAACCAGGACAAGTCAGCCCGCGCAAACGGCCCACGCGCACATATCAAGCCCGTCAGGCGCCCGCAGAAACAGATCCTAAGTT", "GTGGCTGTGCGTAACCGTCTAAATGTAAAAGCGCACATGAGGTAAGTTTACACAGGTGACCCAAGTGATCCTGATCGAGATGGGTAACCGCATTTCTGTGAGTCGGGACACTGGGTGTTACCAGTTGCCAGAAATTCGGCGGGGAGTGAGTTCGGTCGGTATTTATGACTAGGTCATTGGGCTGCAGCGCTCCGCAACAGTCCATGGTTTATAGTTGGAACAGACCGGGGTGATTCATTAAAAGAACATTCATCTGCTTAGAAAAATAGATTTACGTTCCGTAGAACCGTAAGAAATTACTGGCTAACCCAACATAAAAGCTGAG", "TCGAATCCGCCACATGCAAGGCTCAATGTTGACAACTCTTGTGGAGAAGACATTGCAAGACAGCTTGAAGGAGGTCCGCTAGAGCTAGTCTACGCTCCGTGTCAAAGCCTGGAGAACATACGATAATGAGTTAGACCGGGGCCAATTAGTTTACCGGGGATCGCTGAACAACCGGTCCGTGACCATACACTTAGTTGGGTAGCAATACATCTGGCCCGGTCAATTTCATCTAAGGCACCCGATATGAGGACGTGTGCAATACACATATTTTCGGTGCTGTCATGTCCTGTGAGGTTTGCATGGCTGACCGTACTAGTATTAACAG", "GGCCTTAATGAATCGCTCTGTCATGCATGCATTGGGATGGGGACCCCTCCGTTAGCTGTGATGGGTCGAGACGTACGATGTACCGCCCCTTTTACCGGGGTGAGCGATTCTCGTGCGAAATGTTCTCCCACTTTGTCCGGCCGTGCGCGCAGCATACTGGGCAGCCTGCGTTCCCCGCCCCCCCACATGACCACGACTGGGTTCGCCATCGTCAGCTTAAAATCCGTATGGTTAGGGAAGATAGCGTCCAAATGGGAAGCATGCACGTAATTCAGACTGAGTCCCTCTGTATTCTGTCTTGGACGTAATGAAACTCTATAAAACT", "CCCTAGCAAAAGCCCTCTTCAATCACTTGCAATTGTTCTTTACCCCCTTAACTCAGCTTGACCATCATCAATCCAAACCGAAGCTTCGGCCACATCCAGTATGCCGAACAAAGGCAGTAGATTATGCGATCATTCTGTTCTATAACTTTCTTTCTACCCTCACCGATCCACATATTAGCTGTGATTTCGAGTCATTCTGATTGACTATTCATGACTTCCGGCTAAAGACAGGTACATGAAGTGAGCCGGGGTGATACAGGAGTGGGATGCTTGGGCAGCGTTCAATTGGAGAAATCGGAGAGTTGCTACCATTCCTGCTGTCTGG", "GCGTGACGGCTCTATAAGAGAACTACGACCAATAGTACCGGTGGTCCTCAGCCTTAAATATAGTGTAAAGTCGTCCGGGGTGATTCAAATGGGTGTCTTTAAACTTATTTAGAAGTACATTGTGCCTAGGTTTCCGGGACTTGCCATAATTGAGAGTCCCTCATTCTCGGTGAGGAGCGCCGAAGTCCCGTTAATCTGGCGTGTCCCGTGATGCATCATCTAAGTTATCAGTCAGTCGCACGCACTCCTACATGACTGAACCAGTGCGCGCTGAGATGGTACGCGTGCTCACTGTCCAAGGAGACGGACACGTATCAACTGGCGC", "GCCTATGGAATTGCAATGGAGTTATGTCCAGTACAGAGGTGAAAGTTTACCGGACAGAGATTACCAACCCCGGGATTAGGGGAGATCGAGCTGCGGGCTCGTGGGCCAAGTATTCAACGAACAAAGCTTAAGTAAAGCAGCGAAACGCCTACCGGTACAACAGGCGGTTCAGGTGACTACCAATAAAGTAAATGTTCGGACGCAGACGTCTAAGCAAGTGACGGCCTAGGAGTTTACGCCCTACAACCCACCAGCCACCAACGGCAAATAAGTCCCTACTGACCGCGGCATTTTGCGCACCGAACTAGCCGTCAACCACATCACG", "CGGTCCATGTCTCTAGCGCAAATGGATAGGTTCTGTATATACGGCACCTGGCCCAGCACGTCTTTACACAATAAACAATAACCCGAGTGGTGTTAGGTGAGACTTACTAAGGGACCCGCGCAACAACGGGTCCAAGGTGACGGATTTTAATCGTTGCGTGTCGATATCTCGCAGCATCTAAGACTGAGAATGGCGGGATTCACTCCTCGGACTAGGACATCTTCCCAAAGTTTACCAATGTGAGAGACAGAGGTGCACCACTAGGCACGGATGTATGCGCGAGCAATTGAACAATACGGTCCTGTTATACAGTTCACGTTAACAC", "GTCGGTTCAGAGCAACTTTACATAGAGGAACGGAAAGAGCAACATTCTTCCCAAGTTTACCGTCATGGTTTGCGAGTACAGCGGCCGGCACTACTGGCGGAGTGAGCCACATCGTTGGCTGGGACCGAGAAACTGCGAGTCTTTAAACGGACCCGCGCCCCAGACACTAGTGTTTCCTATGCGCGCGCATAAAAAGCCAGTCCCGGTAACTGGAGTTCAGGACCAAGGAGTTTGGACAAGCTTGCTAATCGAAATACCATTTGTGTTGCGATCTTGGAGCGTGCGTAGCGCTTACGGTCGAAACGTACCCCGCAGTATTATACCC"]

best = gibbsSampler(DNA, k, t, n)
s = score(best)
print(s)
for index in range(20):
    sample = gibbsSampler(DNA, k, t, n)
    print(score(sample))
    if score(sample) < s:
        s = score(sample)
        best = sample[:]
for b in best:
    print(b)