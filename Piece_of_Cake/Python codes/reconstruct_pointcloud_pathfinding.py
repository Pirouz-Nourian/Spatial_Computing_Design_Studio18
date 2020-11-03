import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

P = all_points
B = breps

AllPoints = P
AllIndices = []
PointsRemoved = []
PointsRemaining = []
RemovedIndices = []
RemainingIndices = []

for i in range(len(P)):
    point = rg.Point3d(P[i])
    n = 0
    for j in range(len(B)):
        if n == 0:
            if (B[j].IsPointInside(point,0.05,True)):
                PointsRemoved.append(point)
                RemovedIndices.append(i)
                n = n+1
    if n == 0:
        PointsRemaining.append(point)
        RemainingIndices.append(i)
    AllIndices.append(i)

removed_points = PointsRemoved
remaining_points = PointsRemaining
removed_indices = RemovedIndices
remaining_indices = RemainingIndices
all_points = AllPoints
all_indices = AllIndices