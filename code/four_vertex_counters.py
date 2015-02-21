import itertools
import sys
import triangle_counters
import numpy as np

##### This file contains functions to count all 4-vertex patterns in a graph.
##### 
##### C. Seshadhri, Feb 2015

### 4_vertex_count(G) counts all 4-vertex patterns in G. It uses different methods
### for each pattern, which are all explained in the functions. The output
### is a list of 6 numbers, corresponding to the *induced* counts of:
### 3-stars  3-paths  tailed-triangles   4-cycles   chordal-4-cycles   4-cliques
#### the graph is a DAG, this is exactly the number of triangles.
#### 

def four_vertex_count(G):
    order = G.DegenOrdering()   # Get degeneracy ordering
    DG = G.Orient(order)        # DG is digraph with this orientation
    print('Got degeneracy orientation')
    
    tri_info = triangle_counters.triangle_info(DG) # Get triangle info
    print('Got triangle information')
 
    triangle = sum(tri_info[0].values())/3     # Sum of per-vertex triangle counts is 3 times the total triangle count
    
    star_3 = 0.0
    path_3 = 0.0
    tailed_triangle = 0.0
    cycle_4 = 0.0
    chordal_cycle = 0.0
    clique_4 = 0.0
    
    debug = 0
     
    for node in G.vertices:     
        deg = G.degrees[node]
        tri = tri_info[0][node]
        star_3 += deg*(deg-1)*(deg-2)/6    # Number of 3-stars = \sum_v {d_v \choose 3} 
        tailed_triangle += (deg-2)*tri      # Number of tailed triangles hinged at v = (d_v-2)*t_v
        
        for nbr in G.adj_list[node]:             # Loop over neighbors of node
            deg_nbr = G.degrees[nbr]
            path_3 += (deg-1)*(deg_nbr-1)  # Number of 3-paths involving edge (node,nbr) = (deg-1)(deg_nbr-1)
            tri_edge = tri_info[1][(node,nbr)]
            chordal_cycle += tri_edge*(tri_edge-1)/2 # Number of chordal-cycles hinged at edge e = {d_e \choose 2}
    
    # Previous code counts each 3-path twice because each edge appears twice in loop. After this correction
    # each triangle is counted thrice as a 3-path
    path_3 = path_3/2 - 3*triangle        
    
    # Previous code counts each chordal-cycle twice because each edge appears twice in loop.
    chordal_cycle = chordal_cycle/2
    print('Computed everything but 4-cycles and 4-cliques')

    wedge_outout = {}       # Hash tables for storing wedges
    wedge_inout = {}

    # The directed interpretation of Chiba-Nishizeki: for each (u,v), count the number of out wedges and in-out wedges with ends (u,v)

    # There are 3-types of directed 4-cycles
    type1 = 0.0
    type2 = 0.0
    type3 = 0.0

    outout = 0.0
    inout = 0.0

    for node in DG.vertices:
        # First we index out-out wedges centered at node
        for (nbr1, nbr2) in itertools.combinations(DG.adj_list[node],2):    #Loop over all pairs of neighbors of node1
            if nbr1 > nbr2:     # If nbr1 > nbr2, swap, so that nbr1 \leq nbr2
                tmp = nbr1
                nbr1 = nbr2
                nbr2 = tmp            
            
           # print(node,nbr1,nbr2)
             
            if (nbr1,nbr2) in wedge_outout:    # If (nbr1,nbr2) already seen, increment wedge count
                wedge_outout[(nbr1,nbr2)] += 1
            else:
                outout += 1
                wedge_outout[(nbr1,nbr2)] = 1  # Else initialize wedge count to 1

    print('Out-out pairs = ',outout)

    for node in DG.vertices:
        endpoints = {}
        for nbr1 in DG.adj_list[node]:
            for nbr2 in DG.adj_list[nbr1]:       # Get in-out wedge with source at node
                inout += 1
                if nbr2 in endpoints:
                    endpoints[nbr2] += 1
                else:
                    inout += 1
                    endpoints[nbr2] = 1

        for v in endpoints:
            count = endpoints[v]
            type2 += count*(count-1)/2

            v1 = node
            v2 = v

            if v1 > v2:
                swp = v1
                v1 = v2
                v2 = swp

            if (v1,v2) in wedge_outout:
                type3 += count*wedge_outout[(v1,v2)]

    print('In-out pairs =',inout)

    if debug:
        print(wedge_inout)
        print(wedge_outout)

    for pair in wedge_outout:       # Loop over all pairs in wedge_outout
        outout += 1
        count = wedge_outout[pair]  
        type1 += count*(count-1)/2  # Number of type1 4-cycles hinged at (u,v) = {W^{++}_{u,v} \choose 2}

    cycle_4 = type1 + type2 + type3

    print('Computed 4-cycle count')


    clique_work = 0.0
    for node in DG.vertices:        # Loop over nodes
        nbrs = DG.adj_list[node]
        nbrs_info = []
        for cand in nbrs:           # Get topological order position for each cand in nbrs
            nbrs_info.append((cand,DG.top_order_inv[cand]))

        sorted_nbrs = sorted(nbrs_info, key=lambda entry: entry[1])   # Sort nbrs according to position in topological ordering

        deg = len(sorted_nbrs)      # Out-degree of node
        for i in range(0,deg):      # Loop over neighbors in sorted order
            nbri = sorted_nbrs[i][0]
            
            # Get all vertices nbrj > nbri that form triangle with nbri
            tri_end = [] 
            for j in range(i+1,deg):   # Loop over tuple of neighbors i < j
                nbrj = sorted_nbrs[j][0]
                if G.isEdge(nbri,nbrj):
                    tri_end.append(nbrj)  # nbrj forms triangle with (node,nbri)

            # Now look for edges among pairs in tri_end, to find 4-cliques
            for (v1, v2) in itertools.combinations(tri_end,2):
                clique_work += 1
                if G.isEdge(v1,v2):
                    clique_4 += 1

    print('Got cliques. Searched over',clique_work,'tuples')

    transform = np.matrix('1 0 1 0 2 4; 0 1 2 4 6 12; 0 0 1 0 4 12; 0 0 0 1 1 3; 0 0 0 0 1 6; 0 0 0 0 0 1')    

    non_induced_counts = [star_3, path_3, tailed_triangle, cycle_4, chordal_cycle, clique_4]

    print(non_induced_counts)

    return np.linalg.solve(transform,non_induced_counts)


