
import numpy as np
import copy


def eigen_val(G):
    #Need to add function to convert
    #Adj list to Adj matrix in Numpy form    

    #Create Empty Matrix
    adjMatrix_G = []
    
    #Hold the keys into a set list
    keys = G.adj_list.keys()    
    #Create a template for the row to fill the links
    blank_row = np.zeros(len(keys))
    #Iterate through the keys
    for node in keys:
        #Create a new row for elem node
        temp = copy.deepcopy(blank_row)
        #Iterate through the elems list of edges
        for node2 in G.adj_list[node]:
            #For each node2 in the edge list of node
            #Place a 1 at their location within temp
            temp.put(keys.index(node2), 1)
        #Add temp to the matrix
        adjMatrix_G.append(temp)
    #Find the eigenvalues for the matrix
    #After the matrix is turned into an np matrix
    adjMatrix_G = np.matrix(adjMatrix_G)
    
    #Calculate the matrix cubed
    adjMatrix_G = adjMatrix_G*adjMatrix_G*adjMatrix_G

    #Find the trace of the cubed matrix
    trace = np.trace(adjMatrix_G)
    return trace/2