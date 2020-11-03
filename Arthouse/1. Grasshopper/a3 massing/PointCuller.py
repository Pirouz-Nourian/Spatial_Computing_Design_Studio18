import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math as math

pointlist = x
shortlist = []
for i in range(len(pointlist)):
    ngh = 0
    for j in range(len(pointlist)):
        dist = pointlist[i].DistanceTo(pointlist[j])
        if dist < 5.1 and dist > 0:
            ngh = ngh +1
    if ngh > 2:
        shortlist.append(pointlist[i])

a = []
a = shortlist