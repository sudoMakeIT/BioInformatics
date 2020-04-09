# -*- coding: utf-8 -*-

####################################################################################################################
###                                    Algorithms for Bioinformatics
###                                 ***  class Phone Book              ***    
###
### Test number: 7      Class Number: 5         Date:   10 April 2020
###
### Group: 2
### Student: Bruno Pinto               Number: 201603939
### Student: Duarte Melo               Number: 201604476
###
####################################################################################################################
### Complete the code below for the object PhoneBook
### In main give example on how to create, update, insert and use object PhoneBook
### Explain in comments how the data will be organized

# 1.

class MyBlast:
    '''
    Classe que implementa Simple Blast
    '''
    db = []
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
        for l in lines:
            self.addSequenceDB(l)
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
        res = []
        for i in range(len(seq)-self.w+1):
            subseq = seq[i:i+self.w]
            if subseq in query:
                l = query[subseq]
                for ind in l:
                    res.append((ind, i))
        return res
        
    def extendsHit (self, seq, hit, query):
        stq, sts = hit[0], hit[1]
        # move forward
        matfw = 0
        k = 0
        bestk = 0 
        while 2*matfw >= k and stq+self.w+k < len(query) and sts+self.w+k < len(seq):
            if query[stq+self.w+k] == seq[sts+self.w+k]:
                matfw += 1
                bestk = k + 1
            k += 1
        size = self.w + bestk
        # move backwards
        k = 0
        matbw = 0
        bestk = 0
        while 2*matbw >= k and stq > k and sts > k:
            if query[stq-k-1] == seq[sts-k-1]:
                matbw += 1
                bestk = k + 1
            k += 1
        size += bestk

        return (stq-bestk, sts-bestk, size, self.w+matfw+matbw)
        
    def hitBestScore(self, seq, query):
        hits = self.getHits(seq, self.map)
        bestScore = -1.0
        best = ()
        for h in hits:
            ext = self.extendsHit(seq, h, query)
            score = ext[3]
            if score > bestScore or (score == bestScore and ext[2] < best[2]):
                bestScore = score
                best = ext
        return best

    def bestAlignment (self, query):
        self.map = self.buildMap(query)
        bestScore = -1.0
        res = (0,0,0,0,0)
        for k in range(0, len(self.db)):
            bestSeq = self.hitBestScore(self.db[k], query)
            if bestSeq != ():
                score = bestSeq[3]
                if score > bestScore or (score == bestScore and bestSeq[2] < res[2]):
                    bestScore = score
                    res = bestSeq[0], bestSeq[1], bestSeq[2], bestSeq[3], k
        if bestScore < 0: return ()
        else: return res

def test1():
    mb = MyBlast("seqBlast.txt", 3)
    query2 = "cgacgacgacgacgaatgatg"
    r = mb.bestAlignment(query2)
    print(r)       


test1()

# 2.

''' 
Quando existem hits com o mesmo score o factor de desempate é o tamanho do alinhamento, escolhendo a sequências de menor tamanho. 
A lógica por trás desta escolha deve-se ao facto de sequêcias com o mesmo score e tamanhos diferentes terem percentagens de identidade diferentes.
'''

# 3.

'''
db - é o banco de dados de sequências alvo para procurar
query - sequência sobre a qual queremos saber mais
w - comprimento w das subsequências que ocorrem na sequência de consulta

'''

# 4.
    
def readFasta(filename):
    res = ""
    fh = open(filename, "r")
    lines = fh.readlines()
    seq = ""
    for l in lines: 
        seq = l.replace("\n","")
        res += seq
    fh.close()
    return res

def test4():
    mb = MyBlast("seqBlast.txt")
    query1 = readFasta("query1.fasta")
    query2 = readFasta("query2.fasta")
    r1 = mb.bestAlignment(query1)
    r2 = mb.bestAlignment(query2)
    print(r1)
    print(r2)

test4()