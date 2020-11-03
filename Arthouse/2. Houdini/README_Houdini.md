# README Houdini
in this README you will find a description of the Houdini file. Nobody likes wasting words, so let's dive in!

## overal structure
Evey node has a colour. The four used colours represent what type of information is inside the node.
* Solar system = yellow
* Environment = blue
* Point cloud = dark green
* voxel cloud = light green

### Input
In the OBJ folder of the Houdini network view you will find the general structure of the program. On the top there are **two inputs**, the environmental buildings, downloaded from [3drotterdam](https://www.3drotterdam.nl/#/) and the group ratings. This is a .csv file containing the groups and there ratings for different environmental features like distance to the courtyard, height etc. A positive number means that the function wants to be close to it. A negative rating results in a repulsion from this environmental aspect.

**The paths to both these inputs have to be reselected for the program to work.**
### structure
Then there is a single vertical column where the input data goes through the following steps:
1. Create the point cloud
3. Set ratings for every point
4. grow the functions
5. create paths using find shortest path node
6. visualize the output.
### Output
To visualize the different products of this program 4 outputs have been defined.
* The voxelcloud in its environment without the paths
* The voxelcloud in its environment with the paths
* Analyse node in which group sizes are included
* The paths.
### Controls
Also a controller node is present in the top left corner. In this node the following adjustments can be done to adjust the outcome:
* Voxel_size: this sets the multiplier for the voxels. A multiplier is calculated by 2^input.
* Build_height: This value is multiplied by 5 meters to set the maximum height of the point cloud.
* Sun_hours: This roughly sets the amount of hours during the day the sun is included in the solar envelope (from midday, so 6 hours means from 9 - 15)
* Grow_rate: the maximum amount of voxels that a function can grow in each iteration. Take in account that it will also delete one voxel each iteration.
* Accesibility: this is used in the shortest path section. One divided by this number represents the amount of points that will be connected. So 14 means 1 in 14 voxels will be connected.
* Attraction: the amount of extra points given the to point closest to a function it wants to be close to.
* Self_attraction: The amount of extra points given the to point closest to its own center.
* Shape: the overal shape of the building, this refers to the 50% cut in the build area.

**Warning! Some outputs will no longer function when the voxel size or shape is changed.**

## Create the point cloud
Inside this sub network on the top left there is a sub-network node (Voxel_cloud) where the initial building volume is created. This is combined with the geometry (Shadow_Geometry) and the sunrays into the Solar_envelope point wrangle node. In this node a code is written where light rays are calculated for all the points in the shadow geometry and it checks wether the ray hits a point in the voxelcloud.
In the next node the hits are connected to the points in the pointcloud. Than all the points with a hit will be removed.
Then the ''delete floating points'' and ''delete non functional points'' will remove points where the building could not grow efficient enough. 
At last a shape is selected and the pointcloud shape is adjusted to meet the 50% area requirement.

## Set ratings for every point
Here every point in the pointcloud receives a integer type rating (0-19) based on its location in the cloud. the factors are:
1.  Distance to Zomerhofstraat (road with cars and offices on the opposite site of the street)
2. Distance to Vijverhofstraat ( road between the railway and the buiding, mainly cycling and walking traffic
3. Height
4. Distance to courtyard, this is the horizontal distance to the courtyard where a park will be placed. A view on this part could give a nice view.

Then the group ratings input is inserted and scores per group are created per voxel by the following formula:
>Score = Factor_distance_courtyard x rating_Courtyard + 
Factor_distance_Vijverhofstraat x rating_Vijverhof + 
Factor_distance_Zomerhofstraat x rating_Zomerhof + 
Factor_height x rating_Height;        

where the rating is different per group.
In the node ''Total_voxelgroup_rating'' the scores of the 8 surrounding neighbours on the same height are added to the score to find an area with high points instead of just one single point.

Than the points with the highest total scores are added to a group to set the starting points of the functions.

## Grow the functions
In this part of the program a solver node is used to create a loop where the pointcloud iterates over several nodes and updates its values and groups.

It starts of with an wrangle node where the centerpoints of the functions are calculated, since more and more points are added to a function this centerpoint is updated on the start of every interation. Then **two nodes** are found per group. The **first one** runs over all the points inside the group and selects the best neighbour and puts him into a temporary group. Also it selects all the points that are on the edge of the group and adds them to the edge_group.
The '**second node** runs only once. It takes all the points in the temporary group and increases the scores for nodes close to itself and other functions, than the list of points is sorted on scores and the best points are added to the group. Then it does the same thing for all the points in the edge_group and sorts them from low to high. It deletes the edge point with the lowest score.

## Create paths using find shortest path node
In this part of the program a pointcloud with groups is inserted and is will calculate the shortest paths between the centerpoints of several functions. Also it will create 4 stairways and hallways to connect all living and working groups. At last is will connect a number of points in the living and working groups to these main halls.

The points that are part of the path are no longer part of the group. But since all the groups are three times there required size this does not cause issues.

## Visualize the output.
In this sub network voxels are put on all the groups and paths. Also the voxelcloud is transported to the location inside the environment and the environment is copied into the picture to give the end result.
