####The real thing #####
### Pathfinding using networkx library
### using networkx in point grid of the building after the growth process

## importing the libraries


import sys
import csv
import networkx as nx
from numpy import array, zeros, float64, sqrt


## reading in csv files with data 

# reading in a csv file with all the points left after the growth process. These points are the exported selection of rhino to a csv file.  

    PathCSV = "C:\\Users\\mivanesch\\Documents\\bouwkunde minor\\Q2 Spatial Computing design\\wk4\\Exceltabellen.relatie.spaces\\SampleData_pointslist4_functions.csv"
    with open(PathCSV, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        nodedata = [row for row in reader]
	# row [0] point #, row [1] x coordinate of point #, row[1] y coordinate of point #, row [2] z coordinate of point #
        mid = [(float(row[1]), float(row[2]), float(row[3])) for row in nodedata[1:]]


# reading in a csv file with the destination points locations (file pathfinding_bollen)
#the name bollen comes from the location chosen by the dynamic relaxation points
PathCSV = "C:\\Users\\mivanesch\\Documents\\bouwkunde minor\\Q2 Spatial Computing design\\wk4\\Exceltabellen.relatie.spaces\\SampleData_Pathfinding_bollen1.csv"
with open(PathCSV, 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    bollendata = [row for row in reader]
        # row [0] number of bollcluster (location 1 = 1), row [1] x coordinate of boll-location 1, row[2] y coordinate of boll-location 1, row [2] z coordinate of boll-location 1
    bollen = [(float(row[1]), float(row[2]), float(row[3])) for row in bollendata[1:]]

# reading in a csv file with the connections between destinations (file pathfinding_paden)
PathCSV = "C:\\Users\\mivanesch\\Documents\\bouwkunde minor\\Q2 Spatial Computing design\\wk4\\Exceltabellen.relatie.spaces\\SampleData_Pathfinding_paden1.csv"
with open(PathCSV, 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    padendata = [row for row in reader]
    print padendata
    paden = [(int(row[1]), int(row[2])) for row in padendata[1:]]

#there might be a chance that the coordanites of the locations do not correctly correspond with the location of the grid
#snapping of location coordinate to grid (bolvoxel new location on grid)
        
nvoxel = len(mid)
nbollen = len(bollen)
bolvoxel = zeros((nbollen), dtype=int)
for i in range(nbollen):
    mindist = 9e99
    for j in range(nvoxel):
        dist = 0.0
        for k in range(3):
	# comparing the difference distance in square of boll coordinate and midpoint of node of grid 
            dist += (bollen[i][k]-mid[j][k])*(bollen[i][k]-mid[j][k])
        if (dist < mindist):
            bolvoxel[i] = j
            mindist = dist

##adding nodes using networkx graph library 

G.clear()
G = nx.Graph()
for k in range(nvoxel):
    G.add_node(k)
k = 0

##defining edges to travel over
#looking for neighbouring points to connect to. The minradius and maxradius are set to the domain between 3.1 and 4.1 because of our chosen computing voxelsize of 4.0 x 4.0 x 3.2 m
# minradius = 3.1
# maxradius = 4.1 

j = 0
for point in mid[:nvoxel]:
	k = 0
	for checkpoint in mid[:nvoxel]:
            if j < k:
                dist=sqrt((point[0]-checkpoint[0])**2 + (point[1]-checkpoint[1])**2 + (point[2]-checkpoint[2])**2)        
                if dist > minradius and dist < maxradius:
                    G.add_edge(j, k)
            k += 1
        j += 1
        
    
#defining the edges 
ed = zeros((G.number_of_edges(), 2), dtype=int)

#for i in range(G.number_of_edges()):
i = 0
for (u, v, wt) in G.edges.data():
    ed[i][0] = u
    ed[i][1] = v
    i += 1


###shortest path using networkx graph library
#shortest path in nodes (sp)
sp = dict(nx.all_pairs_shortest_path(G))
#print 'shortest in G van %d naar %d: ' % (start, end)

#shortest path in all nodes to ends (splenght)
splength = dict(nx.all_pairs_shortest_path_length(G))
#print splength

#for mid in (start, end)
#print 'shortest nodepath in G van %d naar %d: ' % (start, end)    


#creating shortest path in nodes

path = []
#start = bolvoxel[0]
#end = bolvoxel[1]
#path.append(sp[start][end])
#start = bolvoxel[2]
#end = bolvoxel[3]
#path.append(sp[start][end])

pathlength = []
#start = bolvoxel[0]
#end = bolvoxel[1]
#pathlength.append(splength[start][end])
#start = bolvoxel[2]
#end = bolvoxel[3]
#pathlength.append(splength[start][end])

# writing all these things above shorter you’ll get:

for i in xrange(len(paden)):
    path.append(sp[bolvoxel[paden[i][0]]][bolvoxel[paden[i][1]]])
    pathlength.append(splength[bolvoxel[paden[i][0]]][bolvoxel[paden[i][1]]])



#translating to string for python geometry component
#translating to string for python geometry component
#mid all the nodes
#ed all the edges
#Bol the location start and endpoints to visualize 
#Path the edges which it will travel along 


Mid = [(str(item[0])+"%"+str(item[1])+"%"+str(item[2])) for item in mid]
Ed = [(str(item[0])+"%"+str(item[1])) for item in ed]
Bol = [(str(item[0])+"%"+str(item[1])+"%"+str(item[2])) for item in bollen]
Path = [(str(item[0])+"%"+str(item[1])) for item in ed]
 

####################################################################################
GhPython script Pathfinding

import Rhino.Geometry as rg
from math import sqrt

points = []
lines = []
pathpoints = []
pathlines = []
locations=[]
lengths = []

#reading in strings and converting to datatype


for i in xrange(len(Mid)):
    point = Mid[i].replace(" ",'')
    point = point[1:-1].split('%')
    point = [float(j) for j in point]
    #creating point3d for nodepoints
    point = rg.Point3d(point[0],point[1],point[2])
    points.append(point)

#locations
print Bol

for i in xrange(len(Bol)):
    print Bol[i]
    location = Bol[i].replace(" ",'')
    location = location[1:-1].split('%')
    location = [float(j) for j in location]
    #creating point3d for nodepoints
    location = rg.Point3d(location[0],location[1],location[2])
    locations.append(location)

#creating shortestpathnodes from nodepoints
for i in xrange(len(path)):
    pathpoint = path[i].replace(" ",'')
    print pathpoint
    pathpoint= rg.Point3d(points[int(pathpoint)])
    print pathpoint
    pathpoints.append(pathpoint)

for i in xrange(len(pathlength)):
    length = pathlength[i].replace(" ",'')
    lengths.append((int)(length))

#creating lines for edges
for i in xrange(len(Ed)):
    line = Ed[i].replace(" ",'')
    line = line[1:-1].split('%')
    line = [int(j) for j in line]
    line = rg.Line(points[line[0]], points[line[1]])
    lines.append(line)
    
#creating lines for path
k = 0
for j in xrange(len(lengths)):
    
    print lengths[j]
    for i in xrange(lengths[j]):
        pathline = rg.Line(pathpoints[k], pathpoints[k+1])
        pathlines.append(pathline)
        k = k+1
    k = k+1
    





