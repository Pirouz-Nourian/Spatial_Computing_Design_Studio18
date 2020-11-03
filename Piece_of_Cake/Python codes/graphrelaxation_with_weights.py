#####################################################
#####################################################
#####################################################

### Dynamic Relaxation
###
### Last Time Edited, Refind and Modified by Shervin Azadi & Pirouz Nourian on 10/09/2018
###
### Thanks to Ir. Dirk Rinze Visser
### Adriaenssens, S., P. Block, D. Veenendaal, and C. Williams (2014). Shell Structures for Architecture: Form Finding and Optimization. New York: Routledge.
### "Chapter 2: Review of Dynamic Relaxation with an extension to six degrees of freedom theory" by Adriaenssens
#####################################################

###
### OBJ Reader
###
#####################################################

import copy
import csv
import math

# Input data:
# -----------
RelationCSV = "C:\\Users\\felis\Documents\SampleData_Relation_ferubenmax3.csv"
# opening the file
with open(RelationCSV, 'r') as csvfile:
     reader = csv.reader(csvfile, delimiter=',', quotechar='|')
     reldata = [row for row in reader]
     # relations: startspace:int, endspace:int, weight:float
     relations = [(int(row[0]), int(row[1]), float(row[2])) for row in reldata[1:]]

SpacesCSV = "C:\\Users\\felis\Documents\SampleData_Spaces_ferubenmax3.csv"
# opening the file
with open(SpacesCSV, 'r') as csvfile:
     reader2 = csv.reader(csvfile, delimiter=',', quotechar='|')
     spacedata = [row for row in reader2]
     # spaces : name:string, id:int, area:int
     spaces = [(row[0], int(row[1]), int(row[2])) for row in spacedata[1:]]         

# initiating the lists
xyz = []  # xyz coordinates

#placement around the circle
rad = int(Radius)
spacecount = len(spaces)
for i in range(spacecount):
    pos = (rad * math.sin(360 * i/spacecount), rad * math.cos(360 * i/spacecount), 0)
    xyz.append(pos)

bbmax = [0,0,0]
bbmin = [0,0,0]
for i, x in enumerate(iter(xyz)):
    #finding the bounding box
    for i in range(3):
        if x[i] > bbmax[i]: bbmax[i] = x[i]
        if x[i] < bbmin[i]: bbmin[i] = x[i]

# reserving the Initial State of the system
xyzIS = copy.deepcopy(xyz)

# Output data:
# -----------
# spaces : List of spaces
# relations : List of relations
# xyz : coordination of centroid of spaces
# xyzIS : Initial state of the system
# bbmax, bbmin : Bounding Box

#####################################################
###
### Dynamic Relaxation
###
#####################################################

from numpy import array, zeros, float64, sqrt
import numpy as np
import copy

# Input data:
# -----------
# spaces : List of spaces
# relations : List of relations
# xyz : coordination of centroid of spaces
# bbmax, bbmin : Bounding Box

m = len(relations)
n = len(spaces)

# initializing the repulsion relations (max verbindingen tussen álle ruimtes)
repulseRel = []
for i in range(n):
    for j in range(n):
        if i<j:
            repulseRel.append(tuple([i,j]))
o = len(repulseRel)

# p : Applied Load Component which in our case is zero
p = zeros((n, 3), dtype=float64)
# v : Velosity
v = zeros((n, 3), dtype=float64)
# restlength : Rest Length of the relations (=sqrt(opp ruimte 2) + sqrt(opp ruimte 1))
restlength = array([(sqrt(spaces[relations[i][1]][2]) + sqrt(spaces[relations[i][0]][2])) for i in range(m)])
# repulslength : threshold of repulsion
repulslength = array([(sqrt(spaces[repulseRel[i][1]][2]) + sqrt(spaces[repulseRel[i][0]][2])) for i in range(o)])

# adamp : Acceleration damp controls the stability of the system
adamp = Damping
IterationMax = int(NumberOfIterations)
# K : Elasticity Constant in Hooke's law

# dt : Time intervals
dt = 0.1
mass = 1

for k in range(IterationMax):
    # S : Stiffness Force
    S = zeros((n, 3), dtype=float64)
    # R : Final Forces
    R = zeros((n, 3), dtype=float64)
    
    if k%100 == 99 : print ('iteration: ' + str(k))
    # xyz0 : Initial Position
    xyz0 = copy.copy(xyz)
    # vp : Initial Velocity
    vp = v.copy()
    
    # calculating the length of the relations
    di = array([(xyz[relations[i][1]][0] - xyz[relations[i][0]][0],
                 xyz[relations[i][1]][1] - xyz[relations[i][0]][1],
                 xyz[relations[i][1]][2] - xyz[relations[i][0]][2]) for i in range(m)])
    dist = array([sqrt(di[i,0]*di[i,0] + di[i,1]*di[i,1] + di[i,2]*di[i,2]) for i in range(m)])
  
    #THIS IS WHERE THE WEIGHTS OF THE RELATIONS ARE IMPLEMENTED
    #Hooke's law : Force = length difference * Elasticity Constant (K)
    #with Elasticity Constant = weight of the relation between two functions = 3rd column in the relations file
    EdgeForce = []
    for i in range(m):
        EF = (dist[i] - restlength[i]) * relations[i][2] 
        EdgeForce.append(EF)
    # Edge Force : Decomposing the existing force in each edge into the 3 dimensions 
    EdgeForceS = zeros((m, 3), dtype=float64)

    # iterating throughout the edges
    for i in range(m):
        for j in range(3):
            # Separating the forces into X, Y, Z dimensions
            EdgeForceS[i,j] = (di[i,j] / dist[i]) * EdgeForce[i]

        # Adding the force of each edge to the corresponding nodes
        S[relations[i][0]] -= EdgeForceS[i]
        S[relations[i][1]] += EdgeForceS[i]

    # calculating the length of the repulsion relations
    repdi = array([(xyz[repulseRel[i][1]][0] - xyz[repulseRel[i][0]][0],
                 xyz[repulseRel[i][1]][1] - xyz[repulseRel[i][0]][1],
                 xyz[repulseRel[i][1]][2] - xyz[repulseRel[i][0]][2]) for i in range(o)])
    repdist = array([sqrt(repdi[i,0]*repdi[i,0] + repdi[i,1]*repdi[i,1] + repdi[i,2]*repdi[i,2]) for i in range(o)])  

    # Repulsion Force
    RepForce = ((repdist - repulslength) - abs(repdist - repulslength)) * K * 0.5
    # Edge Force : Decomposing the existing force in each edge into the 3 dimensions 
    RepForceS = zeros((o, 3), dtype=float64)

    # iterating throughout the edges
    for i in range(o):
        for j in range(3):
            # Separating the forces into X, Y, Z dimensions
            RepForceS[i,j] = (repdi[i,j] / repdist[i]) * RepForce[i]

        # Adding the force of each edge to the coresponding nodes
        S[repulseRel[i][0]] -= RepForceS[i]
        S[repulseRel[i][1]] += RepForceS[i]
    
    R = p - S

    A = 1/(1 + adamp * dt * 0.5)
    B = (1 - adamp * dt * 0.5 ) / (1 + adamp * dt * 0.5)
    
    # updating the velocity
    v = A * dt * R / mass + B * vp
    # updating the position
    xyz = xyz0 + dt * v

SpaceNames = [item[0] for item in spaces]
SpaceAreas = [item[2] for item in spaces]
SpaceCentroid = [(str(item[0])+"%"+str(item[1])+"%"+str(item[2])) for item in xyz]
Relations_A = [item[0] for item in relations]
Relations_B = [item[1] for item in relations]