import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino.Geometry.Intersect as ri

HitVoxels = []
HitCounts = []
SolarEnvelope = []
RemovedVoxels = []

for i in range(0, PoI.Count):
    poi = PoI[i]
    for j in range(0, SV.Count):
        sv = SV[j]
        reverseSV = -sv
        ray = rg.Ray3d(poi, reverseSV)
        for k,voxel in enumerate(Voxels):
            P = ri.Intersection.MeshRay(voxel,ray)
            if P >= 0:
                HitIndice = k
                HitVoxels.append(HitIndice)
for l in range(len(Voxels)):
    sum = 0
    for m in range(len(HitVoxels)):
        hitvoxel = HitVoxels[m]
        if hitvoxel == l:
            sum += 1
    HitCounts.append(sum)
for n in range(len(HitCounts)):
	if HitCounts[n] < maxhits:
		SolarEnvelope.append(Voxels[n])
	else:
		RemovedVoxels.append(Voxels[n])
