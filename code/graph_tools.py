import os
import re
import copy
import numpy as np
import random

##### This is the main graph class. It contains the methods for creating and 
##### minor manipulations of graphs. The creation and edge insertion process creates 
##### undirected graphs, though one can easily adapt the representation for directed
##### graphs. Indeed, we later define the DAG (directed acyclic graph) class by
##### inheriting the methods of this class.
##### 
##### 
##### The graph is stored as an adjacency list. This is represented by a dict() structure,
##### where the keys are vertices and the values are sets with the corresponding neighborhood lists. 
##### 
##### C. Seshadhri, Jan 2015 



class graph(object):

#### Initializing empty graph
####

    def __init__(self):
        self.adj_list = dict()   # Initial adjacency list is empty dictionary 
        self.vertices = set()    # Vertices are stored in a set   
        self.degrees = dict()    # Degrees stored as dictionary
        self.colors = dict()     # Colors assigned to each node in the graph

#### Checks if (node1, node2) is edge of graph. Output is 1 (yes) or 0 (no).
####

    def isEdge(self,node1,node2):
        if node1 in self.vertices:               # Check if node1 is vertex
            if node2 in self.adj_list[node1]:    # Then check if node2 is neighbor of node1
                return 1                         # Edge is present!

        if node2 in self.vertices:               # Check if node2 is vertex
            if node1 in self.adj_list[node2]:    # Then check if node1 is neighbor of node2 
                return 1                         # Edge is present!

        return 0                # Edge not present!

#### Add undirected, simple edge (node1, node2)
####
    
    def Add_und_edge(self,node1,node2):

        if node1 == node2:            # Self loop, so do nothing
            return
        if node1 in self.vertices:        # Check if node1 is vertex
            nbrs = self.adj_list[node1]   # nbrs is neighbor list of node1
            if node2 not in nbrs:         # Check if node2 already neighbor of node1
                nbrs.add(node2)           # Add node2 to this list
                self.degrees[node1] = self.degrees[node1]+1    # Increment degree of node1

        else:                    # So node1 is not vertex
            self.vertices.add(node1)        # Add node1 to vertices
            self.adj_list[node1] = {node2}  # Initialize node1's list to have node2
            self.degrees[node1] = 1         # Set degree of node1 to be 1

        if node2 in self.vertices:        # Check if node2 is vertex
            nbrs = self.adj_list[node2]   # nbrs is neighbor list of node2
            if node1 not in nbrs:         # Check if node1 already neighbor of node2
                nbrs.add(node1)            # Add node1 to this list
                self.degrees[node2] = self.degrees[node2]+1    # Increment degree of node2

        else:                    # So node2 is not vertex
            self.vertices.add(node2)        # Add node2 to vertices
            self.adj_list[node2] = {node1}  # Initialize node2's list to have node1
            self.degrees[node2] = 1         # Set degree of node2 to be 1


#### Read a graph from a file with list of edges. Arguments are fname (file name),
#### dirname (directory name), sep (separator). Looks for file dirname/fname.
#### Assumes that line looks like:
#### 
#### node1 sep node2 sep <anything else>
#### 
#### If sep is not set, then it is just whitespace.
####
 
    def Read_edges(self,fname,sep=None):
        num_edges = 0
        with open(fname, 'r') as f_input: # Open file
            for line in f_input: # Read line by line. This is more memory efficient, but might be slower
                line = line.strip() # Remove whitespace from edge
                if not line.startswith('#'): # Skip comments
                    tokens = re.split(sep or '\s+', line.strip())
                    if len(tokens) >= 2:
                        self.Add_und_edge(tokens[0],tokens[1])
                        num_edges += 1
        print('raw edges =', num_edges)    # Print number of lines in file


#### Give the size of the graph. Outputs [vertices (sum of degrees) wedges]
#### Note that sum of degrees is twice the number of edges in the undirected case 
####

    def Size(self):
        n = len(self.vertices)            # Number of vertices

        m = 0                    # Initialize edges/wedges = 0
        wedge = 0
        for node in self.vertices:        # Loop over nodes
            deg = self.degrees[node]      # Get degree of node
            m = m + deg                   # Add degree to current edge count
            wedge = wedge+deg*(deg-1)/2   # Add wedges centered at node to wedge count
        return [n, m, wedge]              # Return size info

#### Print the adjacency list of the graph. Output is written in dirname/fname. 
####
 
    def Output(self,fname,dirname):
        os.chdir(dirname)
        f_output = open(fname,'w')    # Opening file

        for node1 in list(self.adj_list.keys()):   # Looping over nodes
            f_output.write(str(node1)+': ')        # Writing node
            for node2 in (self.adj_list)[node1]:   # Looping over neighbors of node1
                f_output.write(str(node2)+' ')     # Writing out neighbor
            f_output.write('\n')
        f_output.write('------------------\n')     # Ending with dashes
        f_output.close()

#### Compute the degree distribution of graph. Note that the degree is the size of the neighbor list, and is hence the *out*-degree if graph is directed. 
#### Output is a list, where the ith entry is the number of nodes of degree i.
#### If argument fname is provided, then list is written to this file. (This is convenient for plotting.)
####
 
    def Deg_dist(self,fname=''):
        degs = list((self.degrees).values())    # List of degrees
        dd = np.bincount(degs)                  # Doing bincount, so dd[i] is number of entries of value i in degs
        if fname != '':                         # If file name is actually given
            f_input = open(fname,'w')
            for count in dd:                    # Write out each count in separate line
                f_input.write(str(count)+'\n')
            f_input.close()
        return dd 

    def DegreeOrder(self):
      '''Creates a DAG by imposing an order of vertices based on their degree.'''
      debug = False
      core_G = DAG()
      core_G.top_order = sorted(self.degrees, key=lambda el: self.degrees[el])
      if debug:
        print core_G.top_order
      for source in core_G.top_order:
        if debug:
          print "%s: " % source,
        core_G.vertices.add(source)
        core_G.adj_list[source] = set()
        core_G.degrees[source] = 0
        for node in self.adj_list[source]:
          if debug:
            print "%s" % node,
          if node in core_G.vertices:  # Average case O(1), worse case O(n) 
            # We already accounted for this edge
            # (node has higher order than source, so don't add add from higher to lower)
            if debug:
              print "(skipping), ",
            continue
          else:
            if debug:
              print ", ",
          core_G.adj_list[source].add(copy.deepcopy(node))
          core_G.degrees[source] += 1
        if debug:
          print
      return core_G

    def RandomOrder(self):
      '''Creates a DAG by imposing a random order to the vertices of the graph.'''
      debug = False
      core_G = DAG()
      # Makes a copy of the set of vertices and turns them into a list
      core_G.top_order = list(self.vertices)
      random.shuffle(core_G.top_order)
      for source in core_G.top_order:
        if debug:
          print "%s: " % source,
        core_G.vertices.add(source)
        core_G.adj_list[source] = set()
        core_G.degrees[source] = 0
        for node in self.adj_list[source]:
          if debug:
            print "%s" % node,
          if node in core_G.vertices:  # Average case O(1), worse case O(n) 
            # We already accounted for this edge
            # (node has higher order than source, so don't add add from higher to lower)
            if debug:
              print "(skipping), ",
            continue
          else:
            if debug:
              print ", ",
          core_G.adj_list[source].add(copy.deepcopy(node))
          core_G.degrees[source] += 1
        if debug:
          print
      return core_G


#### The fun stuff. This computes the core numbers/degeneracy by applying the minimum vertex removal algorithm. Basically, it iteratively removes 
#### the vertex of minimum degree, till the graph is empty. This leads to an order of vertex removal, say v1, v2, v3,...,vn. The algorithm then
#### constructs the graph where all edges only point from vi to vj where i < j. This creates a DAG, where each edge of the original graph is directed.
#### 
#### The output is this directed graph. Each DAG object (see end) has an associated topological ordering of vertices. In this case, this ordering
#### is just v1, v2, ..., vn.
#### 

    def Degeneracy(self):
        G = copy.deepcopy(self)      # Generate deepcopy, since we will modify G
        n = len(G.vertices)
        top_order = [0]*(n+1)        # Initialize list of degeneracy ordering
        core_G = DAG()               # This is the DAG that will be output
        core_G.vertices = copy.deepcopy(G.vertices)    # Vertices are the same
        for node in core_G.vertices: # Initialize adjacency list and degrees of core_G, the output
            core_G.adj_list[node] = set()
            core_G.degrees[node] = 0

        deg_list = [set() for _ in range(n)]    # Initialize list, where ith entry is set of deg i vertices
        min_deg = n       # variable for min degree of graph

       
        for node in G.vertices:    # Loop over nodes
            deg = G.degrees[node]      # Get degree of node
            deg_list[deg].add(node)    # Update deg_list with node
            if deg < min_deg:          # Update min_deg
                min_deg = deg

        # At this stage, deg_list[d] is the list of vertices of degree d

        for i in range(n):        # The main loop, just going n times
                                  
            # We first need the vertex of minimum degree. Due to the looping and deletion of vertex, we may have exhaused
            # all vertices of minimum degree. We need to update the minimum degree

            while len(deg_list[min_deg]) == 0:  # update min_deg to reach non-empty set
                min_deg = min_deg+1
                
            source = deg_list[min_deg].pop()    # get vertex called "source" with minimum degree 
            core_G.top_order.append(source)     # append to this to topological ordering
            
            # We got the vertex of the ordering! All we need to do now is delete vertex from the graph,
            # and update deg_list appropriately.

            for node in G.adj_list[source]: # loop over nbrs of source, each nbr called "node" 
 
                # We update deg_list
                deg = G.degrees[node]           # degree of node
                deg_list[deg].remove(node)      # move node in deg_list, decreasing its degree by 1
                deg_list[deg-1].add(node)
                if deg-1 < min_deg:             # update min_deg in case node has lower degree
                    min_deg = deg-1

               
                # We then remove the edge (node,source) from G
                G.adj_list[node].remove(source) # remove this edge from G
                G.degrees[node] -= 1            # update degree of node

                core_G.adj_list[source].add(node) # Add directed edge (source,node) to output DAG core_G
                core_G.degrees[source] += 1       # Update the degree of source
                
        return core_G


    def DegenOrder(self):
        n = len(self.vertices)
        touched = {}                 # Map of touched vertices
        cur_degs = {}                # Maintains degrees as vertices are processed
        core_G = DAG()               # This is the DAG that will be output
        core_G.vertices = set(self.vertices)    # Vertices are the same
        for node in core_G.vertices: # Initialize adjacency list and degrees of core_G, the output
            core_G.adj_list[node] = set()
            core_G.degrees[node] = 0

        deg_list = [set() for _ in range(n)]    # Initialize list, where ith entry is set of deg i vertices
        min_deg = n       # variable for min degree of graph

       
        for node in self.vertices:    # Loop over nodes
            deg = self.degrees[node]      # Get degree of node
            touched[node] = 0          # Node not yet touched
            cur_degs[node] = deg       # cur_degs of node just degree
            deg_list[deg].add(node)    # Update deg_list with node
            if deg < min_deg:          # Update min_deg
                min_deg = deg

        # At this stage, deg_list[d] is the list of vertices of degree d

        for i in range(n):        # The main loop, just going n times
                                  
            # We first need the vertex of minimum degree. Due to the looping and deletion of vertex, we may have exhaused
            # all vertices of minimum degree. We need to update the minimum degree

            while len(deg_list[min_deg]) == 0:  # update min_deg to reach non-empty set
                min_deg = min_deg+1
                
            source = deg_list[min_deg].pop()    # get vertex called "source" with minimum degree 
            core_G.top_order.append(source)     # append to this to topological ordering
            touched[source] = 1                 # source has been touched
            
            # We got the vertex of the ordering! All we need to do now is "delete" vertex from the graph,
            # and update deg_list appropriately.

            for node in self.adj_list[source]: # loop over nbrs of source, each nbr called "node"
                
                if touched[node] == 1:         # if node has been touched, do nothing
                    continue 
 
                # We update deg_list
                deg = cur_degs[node]           # degree of node
                deg_list[deg].remove(node)      # move node in deg_list, decreasing its degree by 1
                deg_list[deg-1].add(node)
                if deg-1 < min_deg:             # update min_deg in case node has lower degree
                    min_deg = deg-1
                cur_degs[node] = deg-1          # decrement cur_deg because it has another touched neighbor

                core_G.adj_list[source].add(node) # Add directed edge (source,node) to output DAG core_G
                core_G.degrees[source] += 1       # Update the degree of source
                
        return core_G

    def DegenOrdering(self):
        n = len(self.vertices)
        touched = {}                 # Map of touched vertices
        cur_degs = {}                # Maintains degrees as vertices are processed
        top_order = []               # Topological ordering

        deg_list = [set() for _ in range(n)]    # Initialize list, where ith entry is set of deg i vertices
        min_deg = n       # variable for min degree of graph

       
        for node in self.vertices:    # Loop over nodes
            deg = self.degrees[node]      # Get degree of node
            touched[node] = 0          # Node not yet touched
            cur_degs[node] = deg       # cur_degs of node just degree
            deg_list[deg].add(node)    # Update deg_list with node
            if deg < min_deg:          # Update min_deg
                min_deg = deg

        # At this stage, deg_list[d] is the list of vertices of degree d

        for i in range(n):        # The main loop, just going n times
                                  
            # We first need the vertex of minimum degree. Due to the looping and deletion of vertex, we may have exhaused
            # all vertices of minimum degree. We need to update the minimum degree

            while len(deg_list[min_deg]) == 0:  # update min_deg to reach non-empty set
                min_deg = min_deg+1
                
            source = deg_list[min_deg].pop()    # get vertex called "source" with minimum degree 
            top_order.append(source)     # append to this to topological ordering
            touched[source] = 1                 # source has been touched
            
            # We got the vertex of the ordering! All we need to do now is "delete" vertex from the graph,
            # and update deg_list appropriately.

            for node in self.adj_list[source]: # loop over nbrs of source, each nbr called "node"
                
                if touched[node] == 1:         # if node has been touched, do nothing
                    continue 
 
                # We update deg_list
                deg = cur_degs[node]           # degree of node
                deg_list[deg].remove(node)      # move node in deg_list, decreasing its degree by 1
                deg_list[deg-1].add(node)
                if deg-1 < min_deg:             # update min_deg in case node has lower degree
                    min_deg = deg-1
                cur_degs[node] = deg-1          # decrement cur_deg because it has another touched neighbor

                
        return top_order

#### This function creates a DAG by orienting the edges according to "ordering", which is a permutation
#### of the vertices. 

    def Orient(self,ordering):
        output = DAG()          # Creating empty output graph
        counter = 1
        for node in ordering:   # Loop over nodes
            output.vertices.add(node)   # First add node to vertices in output
            output.top_order_inv[node] = counter    # Setting inverse of topological ordering
            counter += 1
            output.adj_list[node] = set()  # Set up empty adjacency and in lists
            output.in_list[node] = set()
            output.degrees[node] = 0
            output.indegrees[node] = 0
            for nbr in self.adj_list[node]: # For every neighbor nbr of node
                if nbr in output.vertices: # Determine which is higher in order. If nbr already in output.vertices, then nbr is lower. 
                    output.in_list[node].add(nbr)  # If nbr is lower, then nbr is in-neighbor.
                    output.indegrees[node] += 1       # Update degree of nbr accordingly. 
                else:
                    output.adj_list[node].add(nbr) # If nbr is higher, nbr is out neighbor.
                    output.degrees[node] += 1         # Update degree of nbr accordingly.          
        
        output.top_order = ordering         # Topological ordering is as given by input
        return output 
                



#### The DAG class is inherited from the graph class, and the only difference is an additional topological ordering.
#### For outputting into a file, we print the vertices in topological order, so we redefine output.

class DAG(graph):

    def __init__(self):
        super(DAG,self).__init__()
        DAG.top_order = []
        DAG.top_order_inv = dict()
        DAG.in_list = dict()            # Optional in-neighbor list. adj_list only maintains out neighbors
        DAG.indegrees = dict()          # Optional indegrees

    def Output(self,fname):
        f_output = open(fname,'w')

        for node1 in list(self.top_order):
            f_output.write(str(node1)+': ')
            for node2 in (self.adj_list)[node1]:
                f_output.write(str(node2)+' ')
            f_output.write('\n')

