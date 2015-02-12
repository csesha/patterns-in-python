import graph_tools
import triangle_counters
import color_coding





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

## Run the color coding algorithm multiple times to get an average:
print('Running color coding and wedge enumeration on G')
tcounts = []
runs = input('Enter the number of runs: ') 
for run in range(0,runs):
	# Get the count for the number of triangles. For 3 random colors chosen, the number of triangles 
	# estimated from this algorithm, is 2/9 times the actual number of triangles obtained from wedge enumeration.
	g_colorcoding_count = color_coding.color_coding(G)      
	print('Run = ',run, "triangleCount = ",g_colorcoding_count)
	tcounts.append(g_colorcoding_count)

#Calculate the average
print ("Average number of triangle counts over ",run,"runs = ",sum(tcounts)*1.0/len(tcounts))