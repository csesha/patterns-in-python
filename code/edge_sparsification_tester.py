import graph_tools
import triangle_counters
import edge_sparsification
import timeit
from datetime import datetime
import numpy as np


print('Creating empty graph G')
G = graph_tools.graph()                      # Create empty graph

# fname = input('Enter file name: ')           # Enter file name (../graphs/amazon0312.txt)
fname = '../graphs/cit-HepPh.txt' 
print('Reading edges from file',fname,'into G')
G.Read_edges(fname)   # Read edges from file (in this case it is from '../graphs/cit-HepPh.txt' )

G_size = G.Size()          # Output size of G
print('Size of G: vertices = ',G_size[0],', sum of degrees = ',G_size[1],', wedges =',G_size[2])

g_count = triangle_counters.wedge_enum(G)        # Perform wedge enumeration on G to count triangles. Note that this is three times the number of triangles.
print('Running wedge enumeration on G, triangle count =',g_count)

tcounts = []

# p = input('Enter probability of an edge to be included: ') 
# List to store all estimates
estimates = []

# For all probabilities:
for each in [0.1, 0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]:
	# print "edge inclusion probability = ",each
	start = timeit.default_timer()
	G_sparse = edge_sparsification.sparsify_graph(G, each)
	stop = timeit.default_timer()
	print "time to sparsify graph using timer ", stop - start 
	start=datetime.now()
	sparse_size = G_sparse.Size()
	print('Size of G_sparse: vertices = ',sparse_size[0],'sum of degrees = ',sparse_size[1],', wedges =',sparse_size[2])
	g_sparse_count = triangle_counters.wedge_enum(G_sparse)        # Perform wedge enumeration on G to count triangles. Note that this is three times the number of triangles.
	print('Running wedge enumeration on G_sparse, edge inclusion/sparsification probability = ', each,'triangle count =',g_sparse_count)
	print("The estimated number of triangles in the un-sparsified graph is therefore : T/p^3 = ", g_sparse_count/(each*each*each))
	estimates.append(g_sparse_count/(each*each*each))


#Calculate the average
print estimates
print ("Average number of triangle counts using edge_sparsification over different probabilities, over",len(estimates),"runs = ",sum(estimates)*1.0/len(estimates))




	#