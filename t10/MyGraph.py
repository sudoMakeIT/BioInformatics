# -*- coding: utf-8 -*-

####################################################################################################################
###
# Test number: 10      Class Number: 8         Date:   13 Maio 2020
###
### Group: I
# Student: Bruno Pinto               Number: 201603939
# Student: Duarte Melo               Number: 201604476
###
####################################################################################################################


'''

1.
A análise de redes de correlação gênica é um método de bioinformática para descrever os padrões
de correlação entre genes em amostras de microarranjos que pode ser usado para encontrar clusters
de genes correlacionados, para relacionar clusters entre si e para cálculo de medidas de associação
ao cluster.
A título de exemplo, as proteínas mitocondriais são codificadas tanto pelo DNA mitocondrial como
pelo DNA nuclear, isto implica uma comunicação controlada entre os dois genomas.
Uma vez que as mitocôndrias coordenam várias actividades celulares essenciais à vida,
nomeadamente a produção de energia e a morte celular, a desregulação desta comunicação está
implicada em muitas doenças complexas como doenças neurodegenerativas, cancro e diabetes. As redes
de correlação vêm facilitar os métodos de triagem de genes baseados em rede que podem ser usados ​​
para identificar biomarcadores candidatos a alvos terapêuticos.
A construção da rede é conceitualmente simples: os nós representam genes e os nós são conectados
se os genes correspondentes forem co-expressos significativamente em amostras de tecido escolhidas
de forma adequada.
As duas etapas principais para a construção de uma rede de correlação gênica são: o cálculo da
medida de correlação para cada par de genes (no exemplo fornecido pelo professor, a correlação de Pearson)
e a seleção de um limiar de significância (por exemplo ter um valor de correlação superior a 0.5).
Esses dados são representados numa matriz. Se tivermos os valores de expressão gênica de m genes
e n amostras, os dados de entrada seriam uma matriz m × n, chamada matriz de expressão.

'''
# Graph represented as adjacency list using a dictionary
# keys are vertices
# values of the dictionary represent the list of adjacent vertices of the key node
class MyGraph:
    def __init__(self, g={}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])

    # get basic info
    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())

    def get_edges(self):
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v, d))
        return edges

    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())

    # add nodes and edges
    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []

    def add_edge(self, o, d):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph '''
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o]:
            self.graph[o].append(d)

    # successors, predecessors, adjacent nodes

    def get_successors(self, v):
        # needed to avoid list being overwritten of result of the function is used
        return list(self.graph[v])

    def get_predecessors(self, v):
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
        return res

    def get_adjacents(self, v):
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res:
                res.append(p)
        return res

    # degrees

    def out_degree(self, v):
        return len(self.graph[v])

    def in_degree(self, v):
        count = 0
        for k in self.graph.keys():
            if v in self.graph[k]:
                count += 1
        return count

    def degree(self, v):
        return (self.out_degree(v) + self.in_degree(v))

    def all_degrees(self, deg_type="inout"):
        ''' Computes the degree (of a given type) for all nodes.
        deg_type can be "in", "out", or "inout" '''
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout":
                degs[v] = len(self.graph[v])
            else:
                degs[v] = 0
        if deg_type == "in" or deg_type == "inout":
            for v in self.graph.keys():
                for d in self.graph[v]:
                    if deg_type == "in" or v not in self.graph[d]:
                        degs[d] = degs[d] + 1
        return degs

    def highest_degrees(self, all_deg=None, deg_type="inout", top=10):
        if all_deg is None:
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()),
                         key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], ord_deg[:top]))

    # topological metrics over degrees

    def mean_degree(self, deg_type="inout"):
        ''' average degree of all nodes: sum of all degrees divided by number of nodes'''
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))

    def prob_degree(self, deg_type="inout"):
        # count the number of occurrences of each degree in the network and derive its frequencies
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            #print("DEBUG::: prob_degree degs: " + str(degs[k]) );
            if degs[k] in res.keys():
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        #print("DEBUG::: prob_degree : " + str(k) + " res: " + str(res));
        #print("DEBUG::: prob_degree :: res: " + str(res));
        for k in res.keys():
            res[k] /= float(len(degs))
        return res

    # BFS and DFS searches

    def reachable_bfs(self, v):
        l = [v]   # list of nodes to be handled
        res = []  # list of nodes to return the result
        while len(l) > 0:
            node = l.pop(0)  # implements a queue: LILO
            if node != v:
                res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res

    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)  # implements a stack:
            if node != v:
                res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res

    def distance(self, s, d):
        if s == d:
            return 0
        l = [(s, 0)]
        visited = [s]
        while len(l) > 0:
            node, dist = l.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return dist + 1
                elif elem not in visited:
                    l.append((elem, dist+1))
                    visited.append(elem)
        return None

    def shortest_path(self, s, d):
        if s == d:
            return 0
        l = [(s, [])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return preds+[node, elem]
                elif elem not in visited:
                    l.append((elem, preds+[node]))
                    visited.append(elem)
        return None

    # clustering

    def clustering_coef(self, v):
        # ... get the list of adjancent nodes
        adjs = self.graph[v]
        if len(adjs) <= 1:
            return 0.0
        # calculate the number of links of the adjacent nodes
        ligs = 0
        # compare pairwisely if nodes in this list are connected between them
        for i in adjs:
            for j in adjs:
                if i != j:
                    # check if i and j are connected to each other; if yes increment counter of links
                    ligs += 1
        return float(ligs)/(len(adjs)*(len(adjs)-1))

    def all_clustering_coefs(self):
        # go through all the nodes and calculate its cc
        # put those in a dictionary and return
        res = {}
        for i in self.graph.keys():
            res[i] = self.clustering_coef(i)
        return res

    def mean_clustering_coef(self):
        # get all the clustering coefficients
        # and return the mean of all ccs
        return float(sum(self.all_clustering_coefs().values()) / len(self.all_clustering_coefs().values()))

    # network correlation from file
    def create_network_from_file(self, filename, minCorr):
        f = open(filename, "r")
        lines = f.readlines()
        lines = lines[1:]
        for l in lines:
            g1, g2, c = l.split()
            if(float(c) >= minCorr):
                self.add_edge(g1, g2)

    def network_features(self):
        return {
            "nodes(n,l)": self.size(),
            "meanDegree": self.mean_degree(),
            "probDegree": self.prob_degree(),
            "clustmean": self.all_clustering_coefs()
        }
    '''
    Task 4.2
    Após análise das features, usando um minimo de correlação de 0.7, chegamos à conclusão que:
        - o grafo é mais semalhante a uma scale free network, pois apresenta um p(k) ~ k^-a (em que a= 2.5) e podemos encontrar um grupo de nós bastante conectados em relação aos destantes
        
    '''


if __name__ == "__main__":

    gr = MyGraph()
    gr1 = MyGraph()
    gr1.create_network_from_file('m_lung_gexp.tab', 0.7)
    gr.add_vertex(1)
    gr.add_vertex(2)
    gr.add_vertex(3)
    gr.add_vertex(4)
    gr.add_edge(1, 2)
    gr.add_edge(2, 3)
    gr.add_edge(3, 2)
    gr.add_edge(3, 4)
    gr.add_edge(4, 2)
    # gr.print_graph()
    # print(gr.size())

    # print (gr.get_successors(2))
    # print (gr.get_predecessors(2))
    # print (gr.get_adjacents(2))

    # print (gr.in_degree(2))
    # print (gr.out_degree(2))
    # print (gr.degree(2))

    # print(gr.all_degrees("inout"))
    # print(gr.all_degrees("in"))
    # print(gr.all_degrees("out"))

    #gr2 = MyGraph({1:[2,3,4], 2:[5,6],3:[6,8],4:[8],5:[7],6:[],7:[],8:[]})
    # print(gr2.reachable_bfs(1))
    # print(gr2.reachable_dfs(1))

    # print(gr2.distance(1,7))
    # print(gr2.shortest_path(1,7))
    # print(gr2.distance(1,8))
    # print(gr2.shortest_path(1,8))
    # print(gr2.distance(6,1))
    # print(gr2.shortest_path(6,1))

    # #print(gr2.reachable_with_dist(1))

    # print("gr1")
    # gr1.print_graph()
    # print(gr1.size())
    # print(gr1.all_degrees())
    # print(gr1.mean_degree())
    # print(gr1.prob_degree())
    # print(gr1.mean_clustering_coef())
    # print(gr1.network_features())
