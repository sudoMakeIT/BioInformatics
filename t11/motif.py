# -*- coding: utf-8 -*-

####################################################################################################################
###
# Test number: 11     Class Number: 89        Date:   20 Maio 2020
###
### Group: I
# Student: Bruno Pinto               Number: 201603939
# Student: Duarte Melo               Number: 201604476
###
####################################################################################################################

import getopt, sys

'''
usage: python3 motif.py -i demo.fasta -f 2 -n 6 -m 10

result:

GCTATA 0.5                                                                                                              
ATAAAA 0.5                                                                                                              
TAAAAG 0.5                                                                                                              
AAAAGG 0.5                                                                                                              
TCCTCA 0.5                                                                                                              
CCTCAC 0.5                                                                                                             
CAGGGC 0.5                                                                                                             
GCTGCT 0.75                                                                                                            
CTGCTG 0.5                                                                                                             
TGCTGC 0.5                                                                                                            
ATAAAAG 0.5                                                                                                          
TAAAAGG 0.5                                                                                                        
TCCTCAC 0.5                                                                                                  
GCTGCTG 0.5                                                                                                        
CTGCTGC 0.5                                                                                                        
TGCTGCT 0.5                                                                                                           
ATAAAAGG 0.5                                                                                                           
GCTGCTGC 0.5                                                                                                 
CTGCTGCT 0.5                                                                                                            
GCTGCTGCT 0.5


'''  

def read_from_file(filename):
    seqs = []
    fh = open(filename, "r")
    lines = fh.readlines()
    for l in lines:
        seqs.append(l)
    fh.close()
    return seqs

def split_seqs(seqs, min_len,max_len):
    words = {}
    for i in range(int(min_len), int(max_len)+1):
        for seq in seqs:
            for x in range(len(seq)-i+1):
                a = seq[x:x+i]
                if a not in words:
                    words[a] = 1
                else:
                    words[a] += 1
    return words

def filter_freq(words, min_freq, num):
    final = {}
    for x, y in words.items():
        if y >= min_freq:
            final[x] = float(y)/num
    return final


if __name__ == "__main__" :
    argv = sys.argv[1:]

    filename = None
    min_freq = None
    min_len = None
    max_len = None

    try:
        opts,args = getopt.getopt(argv, "i:f:n:m:")
    except getopt.GetoptError as err:
        print(err)
        exit() 
    
    for opt,arg in opts:
        if opt in ['-i']:
            filename = arg
        elif opt in ['-f']:
            min_freq = arg
        elif opt in ['-n']:
            min_len = arg
        elif opt in ['-m']:
            max_len = arg

    seqs = read_from_file(filename)
    words = split_seqs(seqs, min_len,max_len)
    words_with_freq = filter_freq(words, int(min_freq), len(seqs))
    for x, y in words_with_freq.items():
        print(x,y)