import random
import math
import networkx as nx


def greedy_algorithm(G, r):
    edges = sorted(G.edges(data=True), key=lambda t: t[2].get('weight', 1)) #sort the graph according to the weights
    gtag = nx.Graph() #create new graph
    gtag.add_nodes_from(G) #adding G vertices
    for e in edges:
        try:
            d = nx.algorithms.dijkstra_path_length(gtag, e[0], e[1]) #find the shortest path
        except: #if the result is infinity
            d = math.inf #
            pass
        if d > r * e[2]['weight']: #checking if the distance is bigger than r*e's weight
            gtag.add_edge(e[0], e[1], weight=e[2]['weight']) #add the edge to Gtag
    return gtag

#function that adds weights to the graph.
def add_weights_to_graph(G):
    edges = G.edges(data=True)
    for e in edges:
        e[2]['weight'] = random.randint(1, 100) #random weight from 1 to 100
    return G

#a formated line for printing the results
def table(lines, delim='\t'):
    lens = [len(max(col, key=len)) for col in zip(*lines)]
    fmt = delim.join('{:' + str(x) + '}' for x in lens)
    return [fmt.format(*line) for line in lines]


#test 1 by number of edges.
def spanner_by_edges(n, v_list):
    t_list = [0.1, 0.3, 0.8, 1, 1.2, 1.5]
    fields = ["number Of Points","stretch factor","number Of Edges In Source" ,"number Of Edges In Spanner", "weight Of Source", "weight Of Spanner", "weight Of MST", "is connected"]
    rows = [fields]
    graphs=[]
    mst_edges = n - 1
    next_e = (n / 12) * int(mst_edges)
    num_of_edges_list = []
    lastt=t_list[-1]
    t_list=t_list[:-1]
    for i in range(5):
        num_of_edges_list.append((i + 1) * int(next_e))
    for num_of_edges,t in zip(num_of_edges_list,t_list):
        r = (2 * t) + 1
        G = nx.Graph()
        edges_list = []
        for j in range(int(num_of_edges)): #add edges to the graph randomly
            booli=True
            while booli:
                 u, v = random.sample(v_list, 2)
                 if (u,v) not in edges_list and (v,u) not in edges_list:
                     G.add_edge(u,v)
                     edges_list.append((u,v))
                     booli=False
        weighted_g = add_weights_to_graph(G)
        spanner=greedy_algorithm(weighted_g, r)
        mst = nx.minimum_spanning_tree(weighted_g)
        row = [n, r, len(weighted_g.edges),len(spanner.edges), weighted_g.size(weight='weight'), spanner.size(weight='weight'),mst.size(weight='weight'), nx.is_connected(weighted_g)]
        rows.append(row)
        graphs.append([weighted_g, spanner])
    r = (2 * lastt) + 1
    G_complete = nx.complete_graph(n)
    weighted_g = add_weights_to_graph(G_complete)
    spanner = greedy_algorithm(G_complete, r)
    row = [n, r, len(weighted_g.edges), len(spanner.edges), weighted_g.size(weight='weight'),spanner.size(weight='weight'), mst.size(weight='weight'), nx.is_connected(weighted_g)]
    rows.append(row)
    return (rows, graphs)




#test 2 by different t and r factors.
def spanner_by_t(n):
    t_list = [1, 1.2, 1.4, 1.6, 1.8, 2]
    fields = ["number Of Points","stretch factor","number Of Edges In Source" ,"number Of Edges In Spanner", "weight Of Source", "weight Of Spanner", "weight Of MST", "is connected"]
    rows = [fields]
    graphs= [];
    G = nx.complete_graph(n)
    weighted_g = add_weights_to_graph(G)
    for t in t_list:
        r=(2*t)+1
        spanner=greedy_algorithm(weighted_g, r)
        mst = nx.minimum_spanning_tree(weighted_g)
        row = [n, r, len(weighted_g.edges), len(spanner.edges), weighted_g.size(weight='weight'), spanner.size(weight='weight'), mst.size(weight='weight'), nx.is_connected(weighted_g)]
        rows.append(row)
        graphs.append([weighted_g, spanner])
    return rows, graphs



def printRows(rows):
    s = [[str(e) for e in row] for row in rows]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

if __name__ == "__main__":
    n_list1=[100,150,200,250,300]
    n_list2=[100,150,200]
    for n in n_list1:
        vList = [str(x) for x in range(n)] #a list of vertices from 1 to n
        rows, graphs = spanner_by_edges(n,vList)
        printRows(rows)
    for n in n_list2:
        rows, graphs = spanner_by_t(n)
        printRows(rows)


