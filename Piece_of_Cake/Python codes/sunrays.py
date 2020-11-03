import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math as math

pointslist = []
vectorlist = []
R=200000
hours = 6
months = 6
for theta in rs.frange(0, (2*math.pi / 24) * (hours), math.pi/12):
    for phi in rs.frange(-23.45*math.pi/180, 23.45*math.pi/180, (46.9*math.pi/180)/months):
        x = X + R * math.cos(phi) * math.cos(theta)
        y = Y + R * math.cos(phi) * math.sin(theta)
        z = Z + R * math.sin(phi)
        point = rg.Point3d(x, y, z)
        pointslist.append(point)
        vector = rg.Vector3d(X-x, Y-y, Z-z)
        vectorlist.append(vector)
        
points = pointslist
vectors = vectorlist