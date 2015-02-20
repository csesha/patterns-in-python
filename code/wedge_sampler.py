import sys
import random
import numpy as np
import scipy.misc as scm
import wedge_sampler as wg
import operator
import datetime

##### Compute the cc(d)/cc/transitivity of a graph by wedge sampling
#####
##### authors: Shweta Jain (cc(d) & cc)
#####          Pei Jiang   (transitivity)
#####

###
### cc(d) & cc
###

# G: graph (undirected or DAG), sorted_vertices: vertices sorted by degree,
# start and end are indices of the start and end of the degree d vertices in sorted_vertices
# sample_size: the number of vertices sampled
#
# samples a degree d vertex u.a.r., samples a wedge sourced at the vertex u.a.r., checks if it is closed
# repeats this sample_size times and returns the number of closed wedges as an estimate for ccd

def ccd_sampled(G, sorted_vertices, start, end, sample_size):

	closed = 0
	for i in range(sample_size):
		index = np.random.randint(start, end + 1)			# pick a vertex u.a.r.
		v = sorted_vertices[index][0]
		closed = closed + wg.check_random_edge(G,v)			# pick a wedge with the vertex as the source u.a.r. and check if it is closed
	return closed / float(sample_size)						# return the fraction of closed wedges as an estimate for cc(d)


# G: graph (undirected or DAG), sample_size: the number of vertices sampled, fname: name of file to write the ccd values to
# outputs the cc(d) for all d that are powers of 2

def ccd(G, sample_size, fname=''):

	sorted_vertices = sorted(G.degrees.items(), key = lambda x: x[1])

	degs = list((G.degrees).values())						# List of degrees
	dbins = np.bincount(degs)			 					# dbins[i] gives the count of vertices of degree i

	d = 2
	start = dbins[0]
	max_deg = len(dbins) -1
	n = int(np.log2(max_deg)) + 1							# n = number of ds for which ccd is to be calculated
	ccdlist = [0]*(n)

	for i in range(1,n):
		if dbins[d] == 0:
			d = d*2
			continue
		else:
			start = start + sum(dbins[(d/2):d])
			end = start + dbins[d] - 1
			ccdlist[i] = ccd_sampled(G, sorted_vertices, start, end, sample_size)
			print('d = ', d, 'ccd = ', "{0:.2f}".format(ccdlist[i]))
			d = d*2

	d = 1
	if fname != '':											# If file name is actually given
		f_input = open(fname,'w')
		for i in range(n):									# Write out each count in separate line
			f_input.write(str(d)+','+str("{0:.2f}".format(ccdlist[i]))+'\n')
			d = d * 2
		f_input.close()

	return ccdlist

# G: graph (undirected or DAG), sample_size: the number of vertices sampled, fname: name of file to write the ccd values to
# samples a vertex u.a.r., samples a wedge sourced at the vertex u.a.r., checks if it is closed
# repeats this sample_size times and returns the number of closed wedges as an estimate for cc

def cc(G, sample_size, fname=''):
	closed = 0
	for i in range(sample_size):
		v = random.choice(G.degrees.keys())					# pick a vertex u.a.r.
		if G.degrees[v] < 2:								# if the degree of the vertex is less than 2, its contribution to cc will be 0
			continue
		closed = closed + wg.check_random_edge(G,v)			# pick a wedge with the vertex as the source u.a.r. and check if it is closed

	cc = closed / float(sample_size)
	print('cc = ', cc)

	if fname != '':
		f_input = open(fname,'w')
		f_input.write(str("{0:.2f}".format(cc))+'\n')
		f_input.close()
	return cc

###
### transitivity
###

# G: graph (undirected or DAG), sample_size: the number of wedges sampled
# return the fraction of wedges that are closed
def transitivity(G, sample_size):
    closed = 0              # Initialize number of closed wedges
    [n, m , wedges] = G.Size()

    if wedges == 0:
        return 1

    deg_table = list()

    sum_wedges = 0

    # build the degree table, wherein each element is (sum_wedges, node id), to facilitate sampling
    for node1 in G.vertices:     # Loop over all nodes
        deg = len(G.adj_list[node1])
        if deg < 2:
            continue

        deg_table.append((sum_wedges, node1))
        sum_wedges +=  deg*(deg-1)/2

    # sampling starts here
    # at each iteration, select a vertex v with probability prop. to (deg(v) choose 2)
    # then pick any two neighbors of v and check if they are connected by some edge
    for s in range(sample_size):
        v = sample_vertex(deg_table, wedges)
        closed += check_random_edge(G, v)

    return closed/float(sample_size)

# pick two vertices u.a.r. from the adjacent list of v and check if they are neighbors
def check_random_edge(G, v):
    [v1, v2] = random.sample(G.adj_list[v],2)
    return G.isEdge(v1,v2)

# seclect a vertex v with probability prop. to (deg(v) choose 2)
def sample_vertex(deg_table, wedges):
    # generate a random integer in [0,wedges) and then use binary search to find the
    # corresponding vertex
    r = np.random.randint(wedges)
    start = 0
    end = len(deg_table)-1
    cur = (start+end)/2
    while cur != start:
        if r >= deg_table[cur][0]:
            start = cur
        else:
            end = cur

        cur = (start+end)/2

    return deg_table[cur][1]
