import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino.Geometry.Intersect as ri

sums = []
SoundValues = []

#adding the two values together (with weights)
for i in range(len(RoadDistances)):
    RoadDistances[i] = 0.4*RoadDistances[i]+1.0*TrainDistances[i]
    sums.append(RoadDistances[i])

#normalizing the values (0.0 to 1.0)
lowestvalue = min(sums)
highestvalue = max(sums) - lowestvalue
for j in range(len(sums)):
    normalizedvalue = (sums[j]-lowestvalue)/highestvalue
    SoundValues.append(normalizedvalue)

