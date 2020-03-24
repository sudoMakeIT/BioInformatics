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
                res[temp] = len(index)
    return res

#Task3
import re

def get_regex(info):
    m = re.search("(sp\\|[A-Z0-9]+\\|[A-Z0-9_]+)", info)
    if m:
        found = m.group(1)
    return found


def read_Fasta (filename):
    from re import sub, search

    res = []
    sequence = None
    info = None
    dic = {}
    fh = open(filename)
    i = 0
    for line in fh:
        if search(">.*", line):
                if(i!=0):
                    infoKey = get_regex(info)
                    dic[infoKey] = sequence
                if sequence is not None and info is not None and sequence != "":
                    res.append(sequence)
                info = line              
                sequence = ""
        else:
            if sequence is None: return None
            else: sequence += sub("\\s","",line)
        i += 1

    if sequence is not None and info is not None and sequence != "":
        res.append(sequence)
    fh.close()
    return dic

#Task4
def find_ap_nuclease():
    match_keys = []
    dic_seq = read_Fasta("PS00727.fasta")
    from re import search
    regexp = "N.G.R[LIVM]D[LIVMFYH].[LV].S"
    for seq in dic_seq:
        mo = search(regexp, dic_seq[seq])
        if (mo != None):
            match_keys.append(seq)
    return match_keys

print(repeated_subsequences_frequency("ATATATTATATAT",3))
print(read_Fasta("PS00727.fasta"))
print(find_ap_nuclease())