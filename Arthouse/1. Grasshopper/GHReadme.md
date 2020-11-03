# Computing a building with Grasshopper

In this Readme we will describe how to use our **Grasshopper** definitions.

The definitions are used in the following order:
1. VoxelsAndSolar
2. PointCuller
3. GrowerPLUS
4. Pathfinding
5. BlockPlacer

Following these steps should result in the same building we found.



## VoxelsAndSolar

The file to start with is **VoxelsAndSolar.gh**. This is the file that was supplied to us with which we were able to compute a Solar Envelope. This file is meant to be used with the **Computation.3dm** Rhino file.

There are two inputs need in this file, both are meshes. The first one, with the label **"Input Geometry Here"** is the mesh where all the meshes that make up the exisiting building are to be put in, found in the Fbx_root layer in the Rhino file.

The other input mesh are the meshes that are to be used for the points of interest of the neighbours.  These can also be selected in the Rhino file in the Fbx_root layer. Be wary to not select to many faces, as the surrounding buildings are made up of way more meshes than needed.

When both these inputs are filled, the script will run. It creates a bounding box of 100m high around the existing building and divides it up into boxes of 4x4x3.2m. It then intersects those boxes with all the solar vectors shot from every point of interest. If one of these boxes (so-called voxels) is hit by too many solar vectors, it will be deleted.

The most important output is the mesh marked **"Solar Envelope Mesh"** This is baked into the Solution layer of the Rhino file and used in further computation. The other output is the same, only here the voxels are colored according to the amount of sun they block. This allows for some evaluation of the output.

## PointCuller

We are allowed to place building mass in every voxel in the Solar Envelope. However not every voxel is good to actually build in. Some of them are just floating out in space, unconnected to the central mass of voxels. These voxels need to be culled somehow.

To do this we use the **PointCuller.gh** file. This file is meant to be used with the **Computation.3dm** Rhino file. This file takes the Solar Envelope Mesh from **VoxelsAndSolar.gh** as the only input. 

The file takes the centroid from every mesh in the Solar Envelope Mesh and uses those points as input for the python script. In this script points are deleted if they have less than 3 points within a certain distance. This way every point with less than 3 neighbours is deleted. This python script can be repeated to find a scricter Culled Solar Envelope if desired. 

The Grasshopper definition then takes those points and places boxes with dimension 4x4x3.2m on them.

The resulting Culled Solar Envelope is baked into the layer "CulledSolution". Further culling to delete uppermost voxels is done manually in Rhino. This is also where the footprint of the desired building can be set by deleting voxels. The remaing voxels form the boundaries of the building. 

## GrowerPLUS

The next file to be used is the big one: **"GrowerPLUS.gh"**. As the title suggests, this is the point where the building functions are placed in the building boundaries. The functions of the building were clustered together to ease computation. These clusters are placed into the building boundaries by "growing" them into it.

The input for this Grasshopper definition is a 3D grid of points that defines the boundaries of the desired building. To show that this script is flexible, multiple grids are apparent in the file as input. We used the **"Outside"** grid for our building. 

IMPORTANT NOTE: There is a number slider present in the Grasshopper definition. This is used to multiply the program of requirements. Some grids can house less program than others. If a grid can not house the desired amount of the program of requirements, the "check" output from the Python block will be **"FAIL"**.

The "growing" is done in the Python block. The code inside the block can be seen as having two parts: a **Pre-Computation** part and a **Computation** part.

The **Pre-Computation** part starts by defining every cluster. Every cluster has a couple of attributes:
1. A name
2. A size (in voxels)
3. A weight for the height
4. A weight for the normalized distance from the "Noisepoint"
5. A weight for the normalized distance from the "CourtPoint"
6. A weight for the normalized distance from the "VijvPoint"

These points represent a couple critical places in the surroundings of the building. The "NoisePoint" represents the largest source of noise pollution. The "CourtPoint" is point in the center of the courtyard in the middle of the plot. The "VijvPoint" represents the Vijverhofstraat, an important street in our Urban Plan.

These attributes are stored in a new class: **"Cluster"**

Corresponding with the clusters,  every point is evaluated on 4 attributes:
1. The height of the point
2. The normalized distance from the "Noisepoint"
3. The normalized distance from the "CourtPoint"
4. The normalized distance from the "VijvPoint"

These 4 attributes are stored alongside the coordinates of the point in a new class: **"Gridpoint"**.

Another important thing to pre-compute is a list of every voxel and its direct neighbours. This is done using **SciPy** to determine the distance from each point in the input grid to every other point. Then the indices of the closest 6 voxels to each voxel are stored in an array and evaluated, if the distance is too large, the index is set to an arbitrary value.

After all this the **Computation** part of the script can begin. Here every cluster is placed in the grid. This is done by calculating the weighted score of every point in the grid for the current cluster. Then the starting point is set by choosing the point with the highest score. From there the cluster starts to grow. 

The growing is done in the following manner: every voxel in the growth checks it neighbours and adds the neighbour with the highest score to the growth. After a voxel is added a check is performed to see if the growth has reached the desired size.

Every cluster is output as a list of coordinates to a small python block. This translates these coordinates back to actual points. Then voxels are placed back on the points and given a color corresponding to their cluster.

The clusters that have subfunctions are placed lower in the **"GrowerPLUS.gh"** file. These are subdivided by growing the subfunctions inside the boundaries as defined by the growth computed earlier.

Every cluster and the list of remaining points is baked into the Final Building layer of the **"Computation.3dm"** Rhino file.

## Pathfinding using networkx library
### point grid of the building after the growth process (realthing python file)


> ### overall handbook for pathfinding
> - Creating edges and nodes for in graph according to existing growth voxelmidpoint cloud
>> input for pathfinding in 3d and 2d are different
>>- Mainroad structure pathfinding:	Points of clusters connected to eachother, according to connection diagram (*Pathfinding in 3d*, highest point of starters connected to work for example)
>> - Subroad structure pathfinding:	Points of interest on each level to staircase/mainroad structure (*Pathfinding 2d*). (Keep in mind: connection to at least 2 stairways, for fire escape) 

#### creating graph

- input 
- process
- output 

#### input 
 -- *minradius* and *maxradius* for neighbouring voxelsize connections (in this case voxelsize 4.0 x 4.0 x 3.2 m therefore minradius is 3.1 and maxradius is 4.1 m)
 -- *csv file* (**pointlist**) with point data derived from voxelmidpoint-cloud from growing. Exported from rhino to csv
 -- *csv file* (**bollen**) with point data with points of start and end locations. For example starters (0) and work (1)
 -- *csv file* (**paden**)with connections between start and end locations. connection 0 is connection (0 to 1)

#### process

-- if you have locations of start and end points which do not snap to the grid of the building, introduce extra step. Compare comparing the difference distance^2 of location coordinates (xyz) and with the existing voxelmidpoint cloud after growing. 

// adding nodes using networkx graph library. This is a function which creates nodes and edges to create the graph.  

	G = nx.Graph()

    G.add_node(k)


//defining edges to travel along 
-- looking for neighbouring points to connect to. In the existing voxelmidpoint cloud we want to have only orthogonal connections. Therefore the minradius and maxradius come in to check the neighbouring points on distance to create edges between 3.1 and 4.1 m. 
 	
 	dist=sqrt((point[0]-checkpoint[0])**2 + (point[1]-checkpoint[1])**2 + (point[2]-checkpoint[2])**2)        
        	if dist > minradius and dist < maxradius:
                    G.add_edge(j, k)
 
-- shortest path in nodes (sp) using network x library. nx.all_pairs_shortest_path(G) will create a path from one point to all the points in the grid in nodes


-- shortest path in all nodes to ends (splenght) nx.all_pairs_shortest_pathlength(G) will create a path from one point to all the points in the grid in edges

//creating the path

with an reference to the list of connections between functions a path could be created

path = []

	path.append(sp[start][end])


pathlength = []
	
	pathlength.append(splength[start][end])


#### output of GHCPython. Input for GHPython

--**Mid** all the nodes (must be converted to string)
--**Ed** all the edges (must be converted to string)
--**Path** the nodes in voxelmidpoint cloud which it will travel along 
--**Pathlength** the edges in voxelmidpoint cloud which it will travel along

#### output of GHPython
--**points** of grid
--**lines** of grid
--**pathpoints**	points of path (midpoint of voxels)
--**pathlines**	lines of path
--**locations**	start and end points

In grasshopper you can visualisize with the box tool the voxels on the voxelmidpoints from pathpoints. This will only work after aligning with the plane of the building instead of the world xyz plane.

___________________
Then you're done!
you can select your inputs of the start and end points for creating a 3d pathfinding for the mainroads or in 2d if you want to create a subroad to the mainroad.

## BlockPlacer

The last stap is to finalize the form of the building. We chose to use a simple ruleset to define the facade, based on MVRDV's Red7.

The voxels on the 4 outer walls of the building are extruded outwards slightly and given a light red brick material and some windows. The voxels used as circulation space are given a concrete material and very large windows. All the other voxels are given medium size windows and a darker brick material.

The file used for this is **"BlockPlacer.gh"**. It take geometry placed around the origin and copies it to desired points. By designing geometry corresponding to our ruleset around the origin and transposing it to centroids of the correct voxels we find the final building model. This model can also be seen in the **"OnlyBuilding.3dm"** Rhino file.
___________________
group Arthouse
