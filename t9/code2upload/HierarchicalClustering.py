from BinaryTree import BinaryTree
from NumMatrix import NumMatrix

class HierarchicalClustering:

    def __init__(self, matdists):
        self.matdists = matdists
    
    def execute_clustering(self):
        # initialize the trees
        trees = []
        for i in range(self.matdists.num_rows()):
            # create a tree for each leaf
            # add to list of trees
            # ... 
            t = BinaryTree(i)
            trees.append(t)
        # make a copy of the distance matrix to change it
        tableDist = self.matdists.copy()
        # iterations
        for k in range(self.matdists.num_rows(), 1, -1):
            # indices in the matrix for the minimum distance
            mins = tableDist.min_dist_indexes()
            i,j = mins[0], mins[1]
            # create a new tree joining the clusters
            # this will be internal node; height will half of distance in the distance matrix
            # set left tree; set right tree
            n = BinaryTree(-1,tableDist.get_value(i,j)/2.0,trees[i],trees[j])
            if k>2:
                # remove trees being joined from the list 
                ti = trees.pop(i)
                tj = trees.pop(j)
                dists = []
                # calculate the distance for the new cluster
                for x in range(tableDist.num_rows()):          
                    if x != i and x != j:
                        si = len(ti.get_cluster())
                        sj = len(tj.get_cluster())
                        # use the weighted average to calculate the distances between the clusters
                        d = (si*tableDist.get_value(i,x) + sj*tableDist.get_value(j,x)) / (si+sj)
                        dists.append(d)
                # update the matrix:
                # remove col corresponding to i and j
                # remove row corresponding to i and j
                # add row with new distances
                # add col with zero distances
                tableDist.remove_col(i)
                tableDist.remove_col(j)
                tableDist.remove_row(i)
                tableDist.remove_row(j)
                tableDist.add_row(dists)
                tableDist.add_col([0] * (len(dists)+1))
                trees.append(n)
            else: return n


def test():
    m = NumMatrix(5,5)
    m.set_value(0, 1, 2)
    m.set_value(0, 2, 5)
    m.set_value(0, 3, 7)
    m.set_value(0, 4, 9)
    m.set_value(1, 2, 4)
    m.set_value(1, 3, 6)
    m.set_value(1, 4, 7)
    m.set_value(2, 3, 4)
    m.set_value(2, 4, 6)
    m.set_value(3, 4, 3)
    hc = HierarchicalClustering(m)
    arv = hc.execute_clustering()
    arv.print_tree()
    
if __name__ == '__main__': 
    test()
