# -*- coding: utf-8 -*-

def create_submat (match, mismatch, alphabet):
    """ substitution matrix as dictionary """
    sm = {}
    for c1 in alphabet:
        for c2 in alphabet:
            if (c1 == c2):
                sm[c1+c2] = match
            else:
                sm[c1+c2] = mismatch
    return sm

# read substitution matrix from file
def read_submat_file (filename):
    """read substitution matrix from file """
    sm = {}
    f = open(filename, "r")
    line = f.readline()
    tokens = line.split("\t")
    ns = len(tokens)
    alphabet = []
    for i in range(0, ns): 
        alphabet.append(tokens[i][0])
    for i in range(0,ns):
        line = f.readline()
        tokens = line.split("\t")
        for j in range(0, len(tokens)):
            k = alphabet[i]+alphabet[j]
            sm[k] = int(tokens[j])
    return sm

# score of a position (column)
def score_pos(c1, c2, sm, g):
    """score of a position (column)"""
    if c1 == "-" or c2=="-":
        return g
    else:
        return sm[c1+c2]

# score of the whole alignment
def score_align (seq1, seq2, sm, g):
    """ score of the whole alignment; iterate through the two sequences
    sum the score of each position and return its sum; assume sequences are of equal length
    
    """
    res = 0
    # complete here ...
    for i in range(len(seq1)):
        res += score_pos(seq1[i],seq2[i],sm,g)
    return res

def score_affinegap (seq1, seq2, sm, g, r):
    ''' calculates the score of alignment based on : affine_gap(len) = g + r*len
    if the gap is open (first occurrence) sum value g; if gap continues sum r to each new gap position;
    if there is no gap use the substitution matrix for the score.
    '''
    res = 0
    ingap1 = False # two gaps are true when inside gap sequences
    ingap2 = False
    for i in range(len(seq1)):
        if seq1[i]=="-":
            # gap is already open; add r
            if ingap1: res += r
            else:
                # gap is open for the first time; add g
                ingap1 = True
                res += g
        elif seq2[i]=="-":
            # gap is already open; add r
            if ingap2: res += r
            else:
                # gap is open for the first time; add g
                ingap2 = True
                res += g 
        else:
            # no gaps; use substitution matrix
            if ingap1: ingap1 = False
            if ingap2: ingap2 = False
            res += sm[seq1[i]+seq2[i]]
    return res

## global alignment 

def needleman_Wunsch (seq1, seq2, sm, g):
    """Global Alignment"""
    S = [[0]]
    T = [[0]]
    # initialize gaps in rows
    for j in range(1, len(seq2)+1):
        S[0].append(g * j)
        T[0].append(3)
    # initialize gaps in cols
    for i in range(1, len(seq1)+1):
        S.append([g * i])
        T.append([2])
    # apply the recurrence to fill the matrices
    for i in range(0, len(seq1)):
        for j in range(len(seq2)):
            s1 = S[i][j] + score_pos (seq1[i], seq2[j], sm, g); 
            s2 = S[i][j+1] + g
            s3 = S[i+1][j] + g
            S[i+1].append(max(s1, s2, s3))
            T[i+1].append(max3t(s1, s2, s3))
    return (S, T)

def max3t (v1, v2, v3):
    """Provides the integer to fill in T"""
    if v1 > v2:
        if v1 > v3: return 1
        else: return 3
    else:
        if v2 > v3: return 2
        else: return 3

def recover_align (T, seq1, seq2):
    # alignment are two strings
    res = ["", ""]
    i = len(seq1)
    j = len(seq2)
    while i>0 or j>0:
        if T[i][j]==1:
            res[0] = seq1[i-1] + res[0]
            res[1] = seq2[j-1] + res[1]
            i -= 1
            j -= 1
        elif T[i][j] == 3:
            res[0] = "-" + res[0]
            res[1] = seq2[j-1] + res[1]
            j -= 1
        else:
            res[0] = seq1[i-1] + res[0]
            res[1] = "-" + res[1]
            i -= 1
    return res

## local alignment

def smith_Waterman (seq1, seq2, sm, g):
    """Local alignment"""
    S = [[0]]
    T = [[0]]
    maxscore = 0
    # first row filled with zero
    for j in range(1, len(seq2)+1):
        S[0].append(0)
        T[0].append(0)
    # first column filled with zero
    for i in range(1, len(seq1)+1):
        S.append([0])
        T.append([0])
    for i in range(0, len(seq1)):
        for j in range(len(seq2)):
            s1 = S[i][j] + score_pos (seq1[i], seq2[j], sm, g); 
            s2 = S[i][j+1] + g
            s3 = S[i+1][j] + g
            b = max(s1, s2, s3)
            if b <= 0:
                S[i+1].append(0)
                T[i+1].append(0)
            else:
                S[i+1].append(b)
                T[i+1].append(max3t(s1, s2, s3))
                if b > maxscore: 
                    maxscore = b
    return (S, T, maxscore)

def recover_align_local (S, T, seq1, seq2):
    """recover one of the optimal alignments"""
    res = ["", ""]
    """determine the cell with max score"""
    i, j = max_mat(S)
    """terminates when finds a cell with zero"""
    while T[i][j]>0:
        if T[i][j]==1:
            res[0] = seq1[i-1] + res[0]
            res[1] = seq2[j-1] + res[1]
            i -= 1
            j -= 1
        elif T[i][j] == 3:
            res[0] = "-" + res[0];
            res[1] = seq2[j-1] + res[1] 
            j -= 1
        elif T[i][j] == 2:
            res[0] = seq1[i-1] + res[0]
            res[1] = "-" + res[1]
            i -= 1
    return res

def max_mat(mat):
    """finds the max cell in the matrix"""
    maxval = mat[0][0]
    maxrow = 0
    maxcol = 0
    # returns the cell with maximum value
    # complete here...
    
    for i in range(0,len(mat)):
        for j in range(0,len(mat[0])):
            if mat[i][j] >= maxval:
                maxval = mat[i][j]
                maxrow = i
                maxcol = j
    return (maxrow,maxcol)

def identity(seq1, seq2, alphabet = "ACGT"):
    '''calculate the identity score between seq1 and seq2 '''
    # complete here ...
    sm = create_submat(1,0,alphabet)
    # solve the NW algorithm with gap p
    resNW = needleman_Wunsch(seq1, seq2, sm, 0)
    S = resNW[0]
    T = resNW[1]
    # obtain the score of the alignment: using matrix cells and score alignment function
    score = S[len(seq1)][len(seq2)]
    print(score)
    return float(score)/max(len(seq1),len(seq1))

def print_mat (mat):
    for i in range(0, len(mat)):
        print(mat[i]) 


### tests

def test_DNA():
    sm = create_submat(2,-2,"ACGT")
    seq1 = "-CAGTGCATG-ACATA"
    seq2 = "TCAG-GC-TCTACAGA"
    g = -3
    print(sm)
    print(score_align(seq1, seq2, sm, g))

def test_prot():
    # test the alignment of the two sequence
    sm = read_submat_file("blosum62.mat")
    seq1 = "LGPSSGCASRIWTKSA"
    seq2 = "TGPS-G--S-IWSKSG"
    g = -8
    # plot the score of alignment using the subtitution matrix blosum62.mat
    print(score_align(seq1, seq2, sm, g))
    # plot the score of alignment using affine gap score with gap value.
    r = -1
    print(score_affinegap(seq1, seq2, sm, g,r))

def test_global_alig():
    sm = read_submat_file("blosum62.mat")
    seq1 = "PHSWG"
    seq2 = "HGWAG"
    res = needleman_Wunsch(seq1, seq2, sm, -2)
    S = res[0]
    T = res[1]
    print("Score of optimal alignment:", S[len(seq1)][len(seq2)])
    print_mat(S)
    print_mat(T)
    alig = recover_align(T, seq1, seq2)
    print(alig[0])
    print(alig[1])

def test_local_alig():
    sm = read_submat_file("blosum62.mat")
    seq1 = "PHSWG"
    seq2 = "HGWAG"
    res = smith_Waterman(seq1, seq2, sm, -8)
    S = res[0]
    T = res[1]
    print("Score of optimal alignment:", res[2])
    print_mat(S)
    print_mat(T)
    alinL= recover_align_local(S, T, seq1, seq2)
    print(alinL[0])
    print(alinL[1])
    i, j = max_mat(S)
    best_score = S[i][j]
    print ("best score: " + str(best_score))
    
def test_DNA_GlobalAlign():
    # test function
    # Test sequences seq1 and seq2
    seq1 = "TACT"
    seq2 = "ACTA"
    # create a substitution matrix with the match and mismatch values
    sm = create_submat(3,-1,"ACGT")
    # solve the NW algorithm with gap p
    resNW = needleman_Wunsch(seq1, seq2, sm, -3)
    S = resNW[0]
    T = resNW[1]
    # obtain the score of the alignment: using matrix cells and score alignment function
    score = S[len(seq1)][len(seq2)]
    # recover the alignment and print the aligned sequences 1 and 2
    alig = recover_align(T, seq1, seq2)
    print(alig[0])
    print(alig[1])
   
def test_Prot_LocalAlign():
    # Test local alignment SW to sequences seq1 and seq2
    seq1 = "ANDDR"
    seq2 = "AARRD"
    sm = create_submat(3,-1,"ADNR")
    resSW = smith_Waterman(seq1, seq2, sm, -8)
    S = resSW[0]
    T = resSW[1]
    score = resSW[2]
    alinL= recover_align_local(S, T, seq1, seq2)
    print(alinL[0])
    print(alinL[1])
    i, j = max_mat(S)
    best_score = S[i][j]
    print ("best score: " + str(best_score))


#test_DNA()
#test_prot()
#test_global_alig()
#test_local_alig()
#test_DNA_GlobalAlign()
#test_Prot_LocalAlign()