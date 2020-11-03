import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino.Geometry.Intersect as ri

sums = []
NormalizedValues = []
ShadowValues = []

#Calculating shadowvalue of all the voxels using reversed solar rays
for i in PoI:
    sum = 0
    for j in SV:
        reverseSV = -j
        ray = rg.Ray3d(i, reverseSV)
        P = ri.Intersection.MeshRay(Environment,ray)
        if P > 0:
            sum = sum + 1
    sums.append(sum)

#normalizing the values (0.0 to 1.0)
highestvalue = max(sums)
for j in range(len(sums)):
    normalizedvalue = sums[j]/highestvalue
    NormalizedValues.append(normalizedvalue)

#making sure the heart of the building receives no direct sunlight
for m in range(0,len(Distances)):
    if (Distances[m] > 11000):
        NormalizedValues[m] = 1
    if (7000 < Distances[m] < 11000):
        NormalizedValues[m] = 0.9 
    if (6000 < Distances[m] < 7000):
        NormalizedValues[m] = 0.7 
    ShadowValues.append(NormalizedValues[m])