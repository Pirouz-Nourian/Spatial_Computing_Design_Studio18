import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math
import random as rd
import heapq

# A* algorithm and classes/definitions
# from: https://www.redblobgames.com/pathfinding/a-star/implementation.html
# (A* algorithm is closer to uniform cost search)
# in bounds, passable, tup_p3d definitions inspired by viktor's work

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

#cartesian distance
def heuristic(a, b):
    (x1, y1, z1) = a
    (x2, y2, z2) = b
    return math.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)

#To quickly convert a tuples of point into a rhino geometry Points3d
def tup_p3d(tuples):
    return rg.Point3d(tuples[0],tuples[1],tuples[2])

#Transforms a point3d into xyz values
def Point_to_XYZ(points):
    XYZ = points.X,points.Y,points.Z
    return XYZ

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        travel_id = (0,0,3)
        for next in graph.neighbors(current,(travel_id)):
            new_cost = cost_so_far[current]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    return came_from

#appends the shortest found path
def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    if current in came_from:
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start) # optional
        path.reverse() # optional
    else:
        print "no", current, "in came_from"
    return path 

#returns the actual indices of the shortest path
def find_indices(path, points):
    indices = []
    for i in range (len(path)):
        spheres = rg.Brep.CreateFromSphere(rg.Sphere(path[i],1))
        for j in range (len(points)):
            CheckPoint = points[j]
            if rg.Brep.IsPointInside(spheres,CheckPoint,0.1,True):
                indices.append(j)
    return indices

#creates a grid on the origin with the sane voxel count as the total grid in reality has
#checks if the points considered for the path are actually usable
class SquareGrid:
    def __init__(self, width, depth, height, walls):
        self.width = width
        self.depth = depth
        self.height = height
        self.walls = walls
    
    def in_bounds(self, id):
        (x,y,z) = id
        return 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.height
    
    def passable(self, id):
        return id not in self.walls
    
    def neighbors(self, id, (xi, yi, zi)):
        (x,y,z) = id
        results = []
        if xi == 0:
            results.append((x+1, y, z))
            results.append((x-1, y, z))
        elif xi == 1:
            results.append((x+1, y, z))
        elif xi == 2:
            results.append((x-1, y, z))
            
        if yi == 0:
            results.append((x, y+1, z))
            results.append((x, y-1, z))
        elif yi == 1:
            results.append((x, y+1, z))
        elif yi == 2:
            results.append((x, y-1, z))
        
        if zi == 0:
            results.append((x, y, z+1))
            results.append((x, y, z-1))
        elif zi == 1:
            results.append((x, y, z+1))
        elif zi == 2:
            results.append((x, y, z-1))
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


XP = Removed_Points
XI = Removed_Indices
SP = Start_Points
EP = End_Points
W = X_Count
D = Y_Count
H = Z_Count
AP = AllPoints

coordinates = {}
total_paths = 1 #nr of paths

RemovedPoints = []
for j in range (len(XP)):
    NewPoints = int(XP[j].X),int(XP[j].Y),int(XP[j].Z)
    RemovedPoints.append(NewPoints)
g = SquareGrid(W,D,H,RemovedPoints)

start = Point_to_XYZ(SP)
goal = Point_to_XYZ(EP)

#calling the search
Path_Points = []
came_from = a_star_search(g, start, goal)
r_p = reconstruct_path(came_from, start, goal)
for i in r_p:
    coord = i
    Path_Points.append(tup_p3d(coord))

PathIndices = find_indices(Path_Points,AP)
path = Path_Points