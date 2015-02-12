import graph_tools
import wedge_sampler
import triangle_counters


print('Creating empty graph G')
G = graph_tools.graph()                      # Create empty graph

fname = '../graphs/email-Enron.txt'           # Enter file name
print('Reading edges from file',fname,'into G')
G.Read_edges(fname)   # Read edges from file (in this case it is from amazon0312.txt)

G_size = G.Size()          # Output size of G
print('Size of G: vertices = ',G_size[0],', sum of degrees = ',G_size[1],', wedges =',G_size[2])

g_count = triangle_counters.wedge_enum(G)        # Perform wedge enumeration on G to count triangles. Note that this is three times the number of triangles.

print('cc(d) of G:')
wedge_sampler.ccd(G,50,'')
print('cc of G:')
wedge_sampler.cc(G,100)

trans = wedge_sampler.transitivity(G,10000)
print('actual transitivity of G:',g_count/float(G_size[2]))
print('estimated transitivity of G:',trans)
