import itertools
import sys


##### This file contains different functions to find triangles in a graph.
##### 
##### C. Seshadhri, Jan 2015

### wedge_enum(G) does a simple wedge enumeration by looping over the adjacency list of all vertices.
#### It technically outputs the number of wedges that participate in a triangle. 
#### If the graph is undirected, this is three times the number of triangles. If 
#### the graph is a DAG, this is exactly the number of triangles.
#### 

def wedge_enum(G, wedges=False):
    wedge_cnt = 0
    closed = 0              # Initialize number of closed wedges
    for node1 in G.vertices:     # Loop over all nodes
        for (node2, node3) in itertools.combinations(G.adj_list[node1],2):    #Loop over all pairs of neighbors of node1
            wedge_cnt += 1
            if G.isEdge(node2,node3):    # If (node2, node3) form an edge
                closed += 1              # Then wedge participating in trianglehas been found!
    if wedges:
      return (closed, wedge_cnt)
    return closed
