import itertools
import sys
import random
from random import randint
import graph_tools

### This module sparsifies the graph by sampling edges based on an input probability 'p'. 
### With this spasified graph as input, the number of triangles are estimated by wedge 
### Each vertex is assigned on random one of 3 colors. Only colored wedges are checked 
### to see if they are closed. 

### Author : Shachi H Kumar


### Functions : 
### Color_coding - This function assigns random colors to vertices, and enumerates the
### colorful wedges. For each node, choose 2 vertices from its adjacency list, such that 
### their color is different from the node, and different from each other.




#### Sparsifies the graph
#### Choose each edge from the graph with a probability p (given) and construct a new graph G'
    
def sparsify_graph(G, p):
    processed_edges = {}
    numedges = 0
    # Create a new graph 
    G_sparse = graph_tools.graph()
    for node1 in G.vertices:
        neighbors = G.adj_list[node1]            # Get all neighbors of node1
        for eachneighbor in neighbors:
            # if the processed_edges dictionary has the entry for edge (node1, eachneighbor) or (eachneighbor, node1)
            if(processed_edges.has_key((node1, eachneighbor)) or processed_edges.has_key((eachneighbor,node1))):
                if(processed_edges.has_key((node1, eachneighbor))):
                    if not processed_edges.has_key((eachneighbor, node1)):
                        processed_edges[(eachneighbor, node1)] = 1
                else:
                    if not processed_edges.has_key((eachneighbor, node1)):
                        processed_edges[(node1, eachneighbor)] = 1 

            else:
            # If there is no entry for (node1,eachneighbor), then add the edge to the processed_edges dict
            # Generate a random number for the edge. 
            # If the generated random number is less than input 'p', include the edge to G_sparse
                processed_edges[(eachneighbor, node1)] = 1
                processed_edges[(node1, eachneighbor)] = 1
                
                randno = random.uniform(0,1)
                if(randno <= p) :
                    numedges = numedges+1
                    G_sparse.Add_und_edge(node1,eachneighbor)
                    G_sparse.Add_und_edge(eachneighbor,node1)

    print "number of edges in the sparse graph = ", numedges
    return G_sparse