import graph_tools
import triangle_counters

print('Creating empty graph G')
G = graph_tools.graph()                      # Create empty graph

fname = input('Enter file name: ')           # Enter file name (../graphs/amazon0312.txt)
print('Reading edges from file',fname,'into G')
G.Read_edges(fname)   # Read edges from file (in this case it is from amazon0312.txt)

print('Computing degeneracy ordering/orientation into D')
D = G.Degeneracy()                          # Compute degeneracy DAG

print('Computing degeneracy ordering/orientation using new function into DN')
DN = G.DegenOrder()                          # Compute degeneracy DAG

print('Computing degreee distributions of G and D')
dd = G.Deg_dist('amazon-dd.txt')              # Compute degree distribution of G in dd, and output that in 'amazon-dd.txt'
dd_degen = D.Deg_dist('amazon-degen-dd.txt') # Compute degree distribution of D in dd, and output that in 'amazon-degen-dd.txt'
dd_degen_new = DN.Deg_dist('amazon-degen-new.txt')


G_size = G.Size()          # Output size of G
print('Size of G: vertices = ',G_size[0],', sum of degrees = ',G_size[1],', wedges =',G_size[2])

D_size = D.Size()         # Output size of D
print('Size of D: vertices = ',D_size[0],', sum of degrees = ',D_size[1],', wedges =',D_size[2])

DN_size = DN.Size()         # Output size of DN
print('Size of DG: vertices = ',DN_size[0],', sum of degrees = ',DN_size[1],', wedges =',DN_size[2])

dg_count = triangle_counters.wedge_enum(D)       # Perform wedge enumeration on D to count triangles
print('Running wedge enumeration on D, triangle count =',dg_count)

dn_count = triangle_counters.wedge_enum(DN)       # Perform wedge enumeration on D to count triangles
print('Running wedge enumeration on DN, triangle count =',dn_count)


g_count = triangle_counters.wedge_enum(G)        # Perform wedge enumeration on G to count triangles. Note that this is three times the number of triangles.
print('Running wedge enumeration on G, triangle count =',g_count)
