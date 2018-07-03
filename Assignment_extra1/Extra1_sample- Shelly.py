import random #voreingestellte Pythonfunktion um Random Algorithmus zu generieren

def patternToNumber(pattern): #Funktion definieren die mithilfe der symbolToNumber Funktion aus einem String pattern eine Zahl generiert
    if len(pattern) == 0:
        return 0
    return 4 * patternToNumber(pattern[0:-1]) + symbolToNumber(pattern[-1:])

def symbolToNumber(symbol): #Funktion, die zu jedem Symbol (Base) eine Zahl zuweist
    if symbol == "A":
        return 0
    if symbol == "C":
        return 1
    if symbol == "G":
        return 2
    if symbol == "T":
        return 3

def numberToPattern(index, k): #Funktion defnieren, die mithilfe der numberToSymbol Funktion eine Zahl in ein String umwandelt
    if k == 1:
        return numberToSymbol(index)
    return numberToPattern(index // 4, k-1) + numberToSymbol(index % 4)

def numberToSymbol(index): #Funktion, die einer Zahl ein bestimmtes Symbol (Base) zuweist
    if index == 0:
        return "A"
    if index == 1:
        return "C"
    if index == 2:
        return "G"
    if index == 3:
        return "T"

def profileProbable(text, k, profile): #Funktion, die ein Profil mit Wahrscheinlichkeiten erstellt
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

def profileRandom(k,profile, text): #Funktion, die zufällig die gebrauchten Profilen erstellt
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

def hammingDistance(p, q): #Funktion, die Hamming Distance, also die Unterschiede zwischen 2 Strings, berechnet
    ham = 0
    for index, y in zip(p, q):
        if index != y:
            ham +=1
    return ham

def distanceBetweenPatternAndString(pattern, DNA): #Funktion, die Unterschied zwischen dem untersuchten Pattern (Basensequenz) und dem DNA Strang berechnet
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

def consensus(profile): #Funktion, die die wahrscheinlichste Sequenz, also Consensus Sequenz, ermittelt
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

def score(motifs): #Funktion, die den score der Motive ausrechnet (je niedriger der Score, desto besser)
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

def gibbsSampler(DNA, k, t, n): #Gibbs Sampler Funktion
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



k = 8 #Länge der kmere ist 8
t = 5 #5 DNA Sequenzen
n = 100 #Länge der DNA Sequenzen ist 100
DNA = ["CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA", "GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG", "TAGTACCGAGACCGAAAGAAGTATACAGGCGT", "TAGATCAAGTTTCAGGTGCACGTCGGTGAACC", "AATCCACCAGCTCCACGTGCAATGTTGGCCTA"]
#Input DNA Sequenzen
best = gibbsSampler(DNA, k, t, n)#bestes Ergebnis ist das, was bei der GibbsSampler Funktion raus kommt
s = score(best)#berechne den score von best
print(s) # gebe den score an
for index in range(50): 
    sample = gibbsSampler(DNA, k, t, n)
    print(score(sample))
    if score(sample) < s:
        s = score(sample)
        best = sample[:]
for b in best:
    print(b)
 #inspired by Nathaniel Lovin
