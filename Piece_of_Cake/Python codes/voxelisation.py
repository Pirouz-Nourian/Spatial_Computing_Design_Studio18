import Rhino.Geometry as rg
import math as math
import scriptcontext as sc

#Find the bounding box of the brep in question
Bbox = S.GetBoundingBox(True)

#Find the Length, Width, and Height of the bounding boz of the Brep
W = Bbox.Diagonal.X
L = Bbox.Diagonal.Y
H = Bbox.Diagonal.Z

#Divide the 3 axis of the bounding box by the dimensions of the voxel
#This will give you a U, V, W value along the bounding box
#Turn this value into an integer by finding the next biggest integer (roundingUp)
UC = int(math.ceil(W/xS))
VC = int(math.ceil(L/yS))
WC = int(math.ceil(H/zS))

#Create a container for you Point List
#Create a container for your distance List
Point_list = []
Distance_list = []

#Create a base Plane for all the geometry 
Baseplane = rg.Plane(Bbox.Min, rg.Vector3d.XAxis, rg.Vector3d.YAxis)


#Due to the fact that all voxels are based on the center points, we need
#to create a shift towards the voxel's center, which is half of each dimension
xShift = xS*0.5
yShift = yS*0.5
zShift = zS*0.5

#Write a for-loop that itereates through all U, V, W values of the bounding box
#Create a point with consideration of the half shift at each U, V, W locaiton
#Store this point in the point list
#Create a 'closest point; from the brep to the point at the U,V,W value 
#find the distance of the point in the u, v ,w address to the closet point on the brep
#if the point is inside the brep, give it a negative value
#save distances to list
#out put both lists
for i in range(0,WC):
    for j in range (0,VC):
        for k in range (0,UC):
            point = Baseplane.PointAt(xShift +k * xS, yShift + j * yS, zShift + i * zS)
            if (S.IsPointInside(point,0.05,True)):
                Point_list.append(point)

PntList = Point_list
c = Distance_list