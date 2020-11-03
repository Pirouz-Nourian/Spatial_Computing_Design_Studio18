import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# define a function that draws a box based off a center point
# Input: Given a 3d point in space, and xyz dimensions
# Output: Desired a 3d box spanning xyz dimensions based of given center point
# e.g def boxMaker(point,spanX,spanY,spanZ):
def boxMaker (point, spanX, spanY, spanZ):
    
    # initialize a point at the origin, will be later redefined at desired locations
    newPnt = rg.Point3d(0,0,0)
    # deconstruct given point into x y z components as seperate variables
    x = point.X
    y = point.Y
    z = point.Z
    
    temp = []
    
    # initialize empty mesh
    M = rg.Mesh()
    # create a for loop that loops through the corner locations of box and 
    # draws a point at this location
    # utilize the span distance (note must divide by 2 since going from center)
    # e.g range(-0.5 * spanX, spanX*0.5)
    for xi in [-spanX*0.5,spanX*0.5]:
        for yi in [-spanY*0.5,spanY*0.5]:
            for zi in [-spanZ*0.5,spanZ*0.5]:
                newpt = rg.Point3d(x+xi,y+yi,z+zi)
                M.Vertices.Add(newpt)
                #redefine your new point at every corner
                #add all points as Vertices to the initialzed mesh
    M.Faces.AddFace(1,5,7,3)
    M.Faces.AddFace(5,4,6,7)
    M.Faces.AddFace(7,6,2,3)
    M.Faces.AddFace(3,2,0,1)
    M.Faces.AddFace(1,0,4,5)
    M.Faces.AddFace(4,0,2,6)
    
    
    return M

    # add points in counterclock wise motion for each face
    # eg. 0----1
    #     ------
    #     3----2
    # therefore you add the point in this order (0,3,2,1)
    # do this for all 6 faces of the cube
    # you might need to vizualize the point number in grasshopper to make it easier

    
    #return the final mesh with all the points and faces added
meshFaces = boxMaker(centerPoint,BoxSpanX,BoxSpanY,BoxSpanZ)
    
    
    # call your function with all required variables
    # output result of your function and save it into a variable