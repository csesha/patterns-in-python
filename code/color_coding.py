import itertools
import sys
import random
from random import randint



### This module computes the triangle count in a graph using color coding. 
### Each vertex is assigned on random one of 3 colors. Only colored wedges are checked 
### to see if they are closed. 

### Author : Shachi H Kumar


### Functions : 
### Color_coding - This function assigns random colors to vertices, and enumerates the
### colorful wedges. For each node, choose 2 vertices from its adjacency list, such that 
### their color is different from the node, and different from each other.


def color_coding(G):
	#assign colors (between 1 and 3) to vertices , in random
	for node in G.vertices:
		color = randint(1,3)
		color_vertices(G,node, color)

	# Enumerate colorful wedges
	closed = 0			  # Initialize number of closed wedges
#	print len(G.vertices)
	for node1 in G.vertices:	 
		color_of_node1 = G.colors[node1]
#		print color_of_node1
		for (node2, node3) in itertools.combinations(G.adj_list[node1],2):	#Loop over all pairs of neighbors of node1
		# check for the pair of nodes whose colors are different from node1
			if ((G.colors[node2] == G.colors[node3]) or (G.colors[node1] == G.colors[node2]) or (G.colors[node1]==G.colors[node3])):
				continue
			else:
				if G.isEdge(node2,node3):	# If (node2, node3) with different colors form an edge 
					closed += 1			  # Then add the colorful triangle to the count
	return closed


### color_vertices colors a node in the graph with the random color assigned.

def color_vertices(G, node, color):
    if node not in G.vertices:          # Check if the node is in the graph
        return                          
    if(color>3):                        # A color > 3 is not a valid color, do nothing.
        return 
    else:
        G.colors[node] = color
