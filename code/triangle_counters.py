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
    wedge_cnt = 0.0
    closed = 0.0              # Initialize number of closed wedges
    for node1 in G.vertices:     # Loop over all nodes
        for (node2, node3) in itertools.combinations(G.adj_list[node1],2):    #Loop over all pairs of neighbors of node1
            wedge_cnt += 1
            if G.isEdge(node2,node3):    # If (node2, node3) form an edge
                closed += 1.0              # Then wedge participating in trianglehas been found!
    if wedges:
      return (closed, wedge_cnt)
    return closed

### triangle_info(DAG) does a simple wedge enumeration by looping over the adjacency list of all vertices.
#### It counts the number of triangles incident to each vertex and edge. 
#### The input should be a DAG to prevent overcounting of triangles.
#### 
#### The output is two dictionaries. The first gives the number of triangles incident to each vertex. The second
#### gives the number of triangles incident to each (directed) edge.

def triangle_info(DAG):
    tri_vertex = {}         # Output structures
    tri_edge = {}

    for node in DAG.vertices:
        tri_vertex[node] = 0.0   # Initialize for each vertex
        for nbr in DAG.adj_list[node]:
            tri_edge[(node,nbr)] = 0.0    # Initialize for each edge, note each edge is tuple with lower vertex first
            tri_edge[(nbr,node)] = 0.0    # Initialize for each edge, note each edge is tuple with lower vertex first

    for node1 in DAG.vertices:     # Loop over all nodes
        for (node2, node3) in itertools.combinations(DAG.adj_list[node1],2):    #Loop over all pairs of neighbors of node1
            if DAG.isEdge(node2,node3):    # If (node2, node3) form an edge
                tri_vertex[node1] += 1       # Increment all triangle counts
                tri_vertex[node2] += 1
                tri_vertex[node3] += 1
                tri_edge[(node1,node2)] += 1
                tri_edge[(node1,node3)] += 1
                tri_edge[(node2,node3)] += 1
                tri_edge[(node2,node1)] += 1
                tri_edge[(node3,node1)] += 1
                tri_edge[(node3,node2)] += 1
    return [tri_vertex, tri_edge]


#### edge_iter(G) performs simple edge iteration by looping over all edges (u,v), and basically
#### doing a list join for the neighbors of u and v (given by their adjacency lists)
#### increments common neighbor counter
def edge_iter(G):
	common_neighbor_count = 0    #Initialize count of common neighbors to 0
	edge_set = get_edge_set(G)   #get edges of graph as a set
	adj = G.adj_list              

	for edge in edge_set:        #Loop over edges (u,v)
		node1 = edge[0]
		node2 = edge[1]

		neighbor_intersection = set(adj[node1]) & set(adj[node2])     #represent adjacency lists of u and v as sets and take set intersection
		intersect_count = len(neighbor_intersection)                   #num triangles is then num common neighbors of u,v

		common_neighbor_count += intersect_count                       #increment count

	return common_neighbor_count


#### method to convert adjacency list into set of edges

def get_edge_set(G):
	edge_set = set()

	for node1 in G.adj_list:
		for node2 in G.adj_list[node1]:
			if not (node2, node1) in edge_set:
				edge_set.add((node1, node2))

	return edge_set
