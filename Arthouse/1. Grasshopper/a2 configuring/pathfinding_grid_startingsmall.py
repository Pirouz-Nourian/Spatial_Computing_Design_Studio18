####Starting Small#####
### Pathfinding using networkx library
### first understanding of the library in a 3d grid

#input nrow, ncol and nheight

## importing the libraries

import sys
import csv
import networkx as nx
from numpy import array, zeros, float64, sqrt



## reading in csv files with data 

# reading in a csv file with the boundary shape of the building (file pathfinding_gebouw) for example : gebouw[0][0]; 0, gebouw[0][1]; 0, gebouw[0][2]; 0, gebouw[1][0]; 40, gebouw[1][1]; 30, gebouw[1][2]; 20 

PathCSV = "C:\\Users\\mivanesch\\Documents\\bouwkunde minor\\Q2 Spatial Computing design\\wk4\\Exceltabellen.relatie.spaces\\Pathfinding_gebouw.csv"
with open(PathCSV, 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    gebouwdata = [row for row in reader]
    # row [0] x coordinate maximum boundary, row[1] y coordinate maximum boundary, row [2] z coordinate maximum boundary 
    gebouw = [(float(row[0]), float(row[1]), float(row[2])) for row in gebouwdata[1:]]

print gebouw (40, 30, 20)


# reading in a csv file with the destination points locations (file pathfinding_bollen)
#the name bollen comes from the location chosen by the dynamic relaxation points

PathCSV = "C:\\Users\\mivanesch\\Documents\\bouwkunde minor\\Q2 Spatial Computing design\\wk4\\Exceltabellen.relatie.spaces\\Pathfinding_bollen.csv"
with open(PathCSV, 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    bollendata = [row for row in reader]
    # row [0] number of bollcluster (location 1 = 1), row [1] x coordinate of boll-location 1, row[2] y coordinate of boll-location 1, row [2] z coordinate of boll-location 1
    bollen = [(float(row[1]), float(row[2]), float(row[3])) for row in bollendata[1:]]


# reading in a csv file with the connections between destinations (file pathfinding_paden)
PathCSV = "C:\\Users\\mivanesch\\Documents\\bouwkunde minor\\Q2 Spatial Computing design\\wk4\\Exceltabellen.relatie.spaces\\Pathfinding_paden.csv"
with open(PathCSV, 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    padendata = [row for row in reader]
    # row [0] count of connections, row [1] start of connection ( location 1 = 1 ), row [2] end of connection ( location 2 = 2)
    paden = [(int(row[1]), int(row[2])) for row in padendata[1:]]

### creating the voxelgrid 
# opening network x function 

G = nx.Graph()

# input slider of grasshopper gives the nrow, ncol and ndepth of the 3d grid 

#nrow = 4
#ncol = 5
#ndepth = 2

#defining grid in boundary shape of the building 
# total amount of nodes to travel along in this grid 

dx = (gebouw[1][0]-gebouw[0][0])/(ncol-1)
dy = (gebouw[1][1]-gebouw[0][1])/(nrow-1)
dz = (gebouw[1][2]-gebouw[0][2])/(nheight-1)

n = nrow*ncol*nheight

##defining midpoints xyz coordinates of nodes
# first in 2d by iterating over j in ncol (x direction) and i in nrow (y direction), then in 3d by iterating with l over nheight (z direction)
 
mid = zeros((n, 3), dtype=float64)
k = 0
for l in range(nheight):
    for i in range(nrow):
        for j in range(ncol):     
            mid[k][0] = gebouw[0][0]+j*dx
            mid[k][1] = gebouw[0][1]+i*dy
            mid[k][2] = gebouw[0][2]+l*dz
            k += 1

#there might be a chance that the coordanites of the locations do not correctly correspond with the location of the grid
#snapping of location coordinate to grid (bolvoxel new location on grid)

nvoxel = nrow*ncol*nheight
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

#adding nodes to the networkx graph library

G.clear()
G = nx.Graph()
for k in range(n):
    G.add_node(k)
k = 0

##defining edges to travel over
for l in range(nheight):
    for i in range(nrow):
        for j in range(ncol):   
            if j < ncol-1:
                G.add_edge(k,k+1)
            if i < nrow-1:
                G.add_edge(k,k+ncol)
            if l < nheight-1:
                G.add_edge(k,k+(ncol*nrow))
            k += 1

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
#print 'shortest nodepath in G van %d naar %d: ' % (start, end)    


#creating shortest path in nodes (this is a list of node points to travel along to get from bolvoxel 0 to 1)
path = []
start = bolvoxel[0]
end = bolvoxel[1]
path.append(sp[start][end])

#creating shortest pathlength in edges (this is a list of edges to travel along to get from bolvoxel 0 to 1)

pathlength = []
start = bolvoxel[0]
end = bolvoxel[1]
pathlength.append(splength[start][end])


#translating to string for python geometry component
#mid all the nodes
#ed all the edges
#Bol the location start and endpoints to visualize 
#Path the edges which it will travel along 

Mid = [(str(item[0])+"%"+str(item[1])+"%"+str(item[2])) for item in mid]
Ed = [(str(item[0])+"%"+str(item[1])) for item in ed]
Bol = [(str(item[0])+"%"+str(item[1])+"%"+str(item[2])) for item in bollen]
Path = [(str(item[0])+"%"+str(item[1])) for item in ed]


#####################################################################################


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
    


