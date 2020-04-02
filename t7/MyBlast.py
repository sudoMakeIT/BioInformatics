# -*- coding: utf-8 -*-

class MyBlast:
    '''
    Classe que implementa Simple Blast
    '''
    db = []
    w = 0
    map = None

    def __init__(self, filename = None, w = 3):
        '''
        Construtor
        '''
        if filename is not None:
            self.readDatabase(filename)
        else:
            self.db = []
        self.w = w
        self.map = None

    def readDatabase(self, filename):
        fh = open(filename, "r")
        lines = fh.readlines()
        seq = ""
        for l in lines: 
            seq = l.replace("\n","")
            self.addSequenceDB(seq)
        fh.close()
    
    def addSequenceDB(self, seq):
        self.db.append(seq)
        
    def buildMap (self, query):
        res = {}
        for i in range(len(query)-self.w+1):
            subseq = query[i:i+self.w]
            if subseq in res:
               res[subseq].append(i)
            else:
                res[subseq] = [i]
        
        return res 
    
    def getHits (self, seq, query):
        res = [] # list of tuples
        m = self.buildMap(query)
        for i in range(len(seq)-self.w+1):
            subseq = seq[i:i+self.w]
            if subseq in m:
                l = m[subseq]
                for ind in l:
                    res.append( (ind,i) )
        return res 
        
    def extendsHit (self, seq, hit, query):
        stq, sts = hit[0], hit[1]
        ## move forward
        matfw = 0
        k=0
        bestk = 0
        while 2*matfw >= k and stq+self.w+k < len(query) and sts+self.w+k < len(seq):
            if query[stq+self.w+k] == seq[sts+self.w+k]:
                matfw+=1
                bestk = k+1
            k += 1
        size = self.w + bestk
        ## move backwards
        k = 0
        matbw = 0
        bestk = 0
        while 2*matbw >= k and stq > k and sts > k:
            #print(2*matbw >= k and stq > k and sts > k)
            if query[stq-k-1] == seq[sts-k-1]:
                matbw+=1
                bestk = k+1
            k+=1
        size += bestk
        return (stq-bestk, sts-bestk, size, (self.w)+matfw+matbw)     
    
    def hitBestScore(self, seq, query):
        hits = self.getHits(seq, query)
        #print("hist: " + str(hits))
        m = self.buildMap(query)
        bestScore = -1.0
        best = ()
        for h in hits:
            ext = self.extendsHit(seq, h, query)
            score = ext[3]
            if score > bestScore or (score== bestScore and ext[2] < best[2]):
                bestScore = score
                best = ext
        return best     
 
    def bestAlignment (self, query):
        m = self.buildMap(query)
        bestScore = -1.0
        res = (0,0,0,0,0)
        for k in range(0,len(self.db)):
            bestSeq = self.hitBestScore(self.db[k], query)
            if bestSeq != ():
                score = bestSeq[3]
                if score > bestScore or (score== bestScore and bestSeq[2] < res[2]):
                    bestScore = score
                    res = bestSeq[0], bestSeq[1], bestSeq[2], bestSeq[3], k
        if bestScore < 0: return ()
        else: return res 

def read_fasta(filename):
    res = ""
    fh = open(filename, "r")
    lines = fh.readlines()
    seq = ""
    for l in lines: 
        seq = l.replace("\n","")
        res += seq
    fh.close()
    return res

def test1():
    mb = MyBlast("seqBlast.txt", 11)
    query2 = "cgacgacgacgacgaatgatg"
    r = mb.bestAlignment(query2)
    print(r)       

def test1_test():
    mb = MyBlast("seqBlast.txt",3)
    query2 = "cagctactag"
    r = mb.getHits("atatagtgctagatctgatcgatgctaaatgctagatagtgatcgtagagctgatagcgtagatatagatgcgctgctagaatgctgatagctgaaatagatcgatagtcgatagtcgctgatagtctgtagctgatgcgctgatggatgtttgggtacacgatgctgatacgcatgatgatgatgaaca",query2)
    print(str(r) + "\n")       

def test4():
    #read querys
    q1 = read_fasta("query1.fasta")
    q2 = read_fasta("query2.fasta")
    print(q1)
    mb = MyBlast("seqBlast.txt", 11)
    r = mb.bestAlignment(q1)
    print(r)       
    r = mb.bestAlignment(q2)
    print(r)       
    

#test1()
#test1_test()
test4()


#ex2
'''

'''

#ex3
'''

'''
