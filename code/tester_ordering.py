#!/usr/bin/python
import sys
import time
import graph_tools
import triangle_counters
import json
 
def test_DAGs(gfnames, iterations=1, verbose=False):
  orderings = ['Random', 'DegreeOrder', 'Degeneracy']
  stats = {}

  for gfname in gfnames:
    stats[gfname] = {'G' : {'read': [], 'wedges' : [], 'triangles' : [], 'time' : []}}
    for ordering in orderings:
      stats[gfname][ordering] = {'create' : [], 'wedges' : [], 'triangles' : [], 'time' : []}

  for iteration in range(0,iterations):
    for gfname in gfnames:

      G = graph_tools.graph()
      if verbose:
        print('Reading edges from file %s' % gfname)
      start = time.clock()
      G.Read_edges(gfname)
      end = time.clock()
      ellapsed = end - start
      stats[gfname]['G']['read'].append(ellapsed)
      if verbose:
        print("  Time to read graph (%s): %.2fs" % (gfname, ellapsed))
        print
  
      start = time.clock()
      (triangles, wedges) = triangle_counters.wedge_enum(G, wedges=True)
      triangles /= 3
      end = time.clock()
      ellapsed = end - start
      stats[gfname]['G']['triangles'].append(triangles)
      stats[gfname]['G']['wedges'].append(wedges)
      stats[gfname]['G']['time'].append(ellapsed)
      if verbose:
        print('  Running wedge enumeration on G, triangle count=%d (time=%.2fs)' % (triangles, ellapsed))
        print
  
      for order in orderings:
        start = time.clock()
        D = eval('G.%s()' % order)
        end = time.clock()
        ellapsed = end - start
        stats[gfname][order]['create'].append(ellapsed)
        if verbose:
          print("  Time to create DAG (%s): %.2fs" % (order, ellapsed))
  
        start = time.clock()
        (triangles, wedges) = triangle_counters.wedge_enum(D, wedges=True)
        end = time.clock()
        ellapsed = end - start
        stats[gfname][order]['triangles'].append(triangles)
        stats[gfname][order]['wedges'].append(wedges)
        stats[gfname][order]['time'].append(ellapsed)
        if verbose:
          print('  Running wedge enumeration on D (%s), triangle count=%d (time=%.2fs)' % (order, triangles, ellapsed))
          print
  return stats

def main(argv):
  gfnames = ['../graphs/amazon0312.txt', '../graphs/p2p-Gnutella31.txt', '../graphs/facebook_combined.txt', '../graphs/email-Enron.txt']
  stats = test_DAGs(gfnames, verbose=True)
  print json.dumps(stats, indent=2)

  # TODO: Plot stats in matplotlib

if __name__ == '__main__':
  sys.exit(main(sys.argv))
