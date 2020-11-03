'''

import numpy as np
import networkx as nx
import math

print (type (Rel_edges))
print (type (First_point) )

G = nx.Graph()

# Making set of nodes for each vertex 
G.add_nodes_from(range (len (points)))

#Making a weight function

def weight_func (a1,b1):
    dist = math.sqrt()
    
 

F = G + H
F = Total cost ; G = Diff between current node and start node ; H = estimated distance between current node
and end node

for a,b in Rel_cords:
    G.add_edge(a,b)

'''
import sys
import io

from heapq import heappush, heappop
from itertools import count

import networkx as nx
from networkx.utils import not_implemented_for

__all__ = ['astar_path', 'astar_path_length']

G = nx.Graph()
G.add_nodes_from(range (len (points)))

G.add_edges_from(Rel_cords)

def astar_path(G, source, target, heuristic=None, weight='weight'):

    push = heappush
    pop = heappop

    c = count()
    queue = [(0, next(c), source, 0, None)]

    
    enqueued = {}
   
    explored = {}

    while queue:
        # Pop the smallest item from queue.
        _, __, curnode, dist, parent = pop(queue)

        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if curnode in explored:
            continue

        explored[curnode] = parent

        for neighbor, w in G[curnode].items():
            if neighbor in explored:
                continue
            ncost = dist + w.get(weight, 1)
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            push(queue, (ncost + h, next(c), neighbor, ncost, curnode))



edges = G.edges()
nodes = G.nodes()


#path =  (nx.astar_path(G,source, target))
#path2 =  (nx.astar_path(G,source, target))
#path3 =  (nx.astar_path(G,source, target))

s = 0
path = []
for i in range (len (path_index)):
    path.append ( nx.astar_path(G,path_index[i-1], path_index[i]))



    

