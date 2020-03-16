###Task2


def simpleBooyerMoore(seq, pattern):
    """Very simplified version of Booyer-Moore with the BCR rule"""
    alphabet = "".join(set(list(seq)))    
    occ = {}
    for symb in alphabet:
        occ[symb] = -1
    for j in range(len(pattern)):
        c = pattern[j]
        occ[c] = j     
    res = []
    i = 0
    while i <= len(seq) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and pattern[j] == seq[j+i]:
            j -= 1
        if (j < 0):
            res.append(i)
            i += 1
        else:
            c = seq[j + i]
            i += max(1, j - occ[c]) 
    return res


def repeated_subsequences_frequency(dna_seq, k = 10):
    '''Write a function that, given a DNA sequence, allows to detect if there are repeated sequences of size k
    The result should be a dictionary with sub-sequences as keys, and their frequency as values.'''
    res = {}
    for i in range(0, len(dna_seq)-k+1):
        temp = dna_seq[i:i+k]
        if temp not in res.keys():
            index = simpleBooyerMoore(dna_seq,temp)
            if(len(index) > 0):
                res[temp] =len(index)
    return res