from PairwiseAlignment import PairwiseAlignment
from MyAlign import MyAlign
from MySeq import MySeq
from SubstMatrix import SubstMatrix

class MultipleAlignment():

    def __init__(self, seqs, alignseq):
        self.seqs = seqs # list of MySeq objects
        self.alignpars = alignseq # PairwiseAlignment objects
    
    def num_seqs(self):
        return len(self.seqs)
    
    def add_seq_alignment (self, alignment, seq):
        res = []
        for i in range(len(alignment.listseqs)+1):
            res.append("")
        # create consensus from give alignments
        cons = MySeq(alignment.consensus(),alignment.al_type)
        self.alignpars.needleman_Wunsch(cons, seq)
        align2 = self.alignpars.recover_align()
        orig = 0
        for i in range(len(align2)):
            if align2[0,i]== '-':
                for k in range(len(alignment.listseqs)):
                    res[k] += "-"
            else:
                for k in range(len(alignment.listseqs)):
                    res[k] += alignment[k,orig]
                orig+=1
        res[len(alignment.listseqs)] = align2.listseqs[1]
        return MyAlign(res, alignment.al_type) 
    
    def align_consensus(self):
        self.alignpars.needleman_Wunsch(self.seqs[0], self.seqs[1])
        res = self.alignpars.recover_align()

        for i in range(2, len(self.seqs)):
            res = self.add_seq_alignment(res, self.seqs[i])
        return res 
        
    def scoreColumn(self, charsCol):
        score = 0
        gap = False
        if charsCol[1:] == charsCol[:-1]:
            return len(charsCol) * self.alignpars.score_pos(charsCol[0],charsCol[1])
        for i in range(0, len(charsCol)-1):
            #print(charsCol[i])
            #print(charsCol[i+1])
            #print(self.alignpars.score_pos(charsCol[i],charsCol[i+1]))
            if(charsCol[i] == '-' and charsCol[i+1] == '-'):
                score += 2 * self.alignpars.g
                gap = True
            elif(charsCol[i] == '-' or charsCol[i+1] == '-'):
                if gap == False:
                    score += self.alignpars.g
                    gap = True                    
            else:
                score += self.alignpars.score_pos(charsCol[i],charsCol[i+1])
        if(charsCol[0] != '-' and charsCol[-1] != '-' and gap == True):            
            score += self.alignpars.score_pos(charsCol[0],charsCol[-1])
        elif(charsCol[0] == '-' and charsCol[-1] == '-' and gap == True):          
            score +=  self.alignpars.g
        return score
        
    def scoreSP (self, alignment):
        #print(SubstMatrix.score_pair(self.alignpars.sm,'A','T'))
        #print(MyAlign.column(self.seqs, 0))
        score = 0
        #print(self.alignpars.sm.sm)
        for i in range(0,len(alignment)):
            print(str(alignment.column(i)) + ": " + str(self.scoreColumn(alignment.column(i))))
            score += self.scoreColumn(alignment.column(i))
        return score

def printMat (mat):
    for i in range(0, len(mat)):
        print(mat[i])

def test_prot():  
    s1 = MySeq("PHWAS","protein")
    s2 = MySeq("HWASW","protein")
    s3 = MySeq("HPHWA","protein")
    sm = SubstMatrix()
    sm.read_submat_file("blosum62.mat", "\t")
    aseq = PairwiseAlignment(sm, -8)
    ma = MultipleAlignment([s1,s2,s3], aseq)
    alinm = ma.align_consensus()
    print(alinm)
    print("score: " + str(ma.scoreSP(alinm)))
    

def test():
    s1 = MySeq("ATAGC")
    s2 = MySeq("AACC")
    s3 = MySeq("ATGAC")
    
    sm = SubstMatrix()
    sm.create_submat(1,-1,"ACGT")
    aseq = PairwiseAlignment(sm,-1)
    ma = MultipleAlignment([s1,s2,s3], aseq)
    al = ma.align_consensus()
    print(al)
    print("score: " + str(ma.scoreSP(al)))
    
def exercise1():
    s1 = MySeq("ACATATCAT")
    s2 = MySeq("AACAGATCT")
    s3 = MySeq("AGATATTAG")
    s4 = MySeq("GCATCGATT")
    
    sm = SubstMatrix()
    sm.create_submat(1,-1,"ACGT")
    aseq = PairwiseAlignment(sm,-1)
    ma = MultipleAlignment([s1,s2,s3,s4], aseq)
    al = ma.align_consensus()
    print(al)
    print("score: " + str(ma.scoreSP(al)))

if __name__ == "__main__": 
    test_prot()
    print()
    test()
    print()
    exercise1()