
code/ has three files: graph_tools.py, tester.py, and triangle_counters.py
graphs/ has a bunch of graphs downloaded from the SNAP graphs library (sending link shortly), all txt files with lists of edges.

* graph_tools.py has the code for inputting graphs, getting degree distributions, and getting the degeneracy/core/minimum-degree-removal ordering we discussed in class. *Read* the code. It's pretty well documented, and should clarify doubts that you have.
* triangle_counters.py has the wedge enumeration code.
* tester.py is a simple script that inputs a graph, computes the degeneracy orientation/ordering, gets the degree distributions, and does wedge enumeration (to count triangles). Read over it, and it should be clear how to try out different graphs.

When I run tester.py (using python 3.x, it also works for 2.x), this is the output I get.

Creating empty graph G
Reading edges from file ../graphs/amazon0312.txt into G
raw edges = 3200444
Computing degeneracy ordering/orientation into D
Computing degreee distributions of G and D
Size of G: vertices =  400732 , sum of degrees =  4699746 , wedges = 68910461.0
Size of D: vertices =  400732 , sum of degrees =  2349873 , wedges = 6750650.0
Running wedge enumeration on D, triangle count = 3686467
Running wedge enumeration on G, triangle count = 11059401

