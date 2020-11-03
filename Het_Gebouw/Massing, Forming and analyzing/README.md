# Massing, Forming and analyses

In this folder it will be discussed how we did analyses of the site and made actual point cloud. 

The following analysis were made:
1. Road distance evaluation
2. Traffic Evaluation
3. Sound Evaluation
4. Distance from neighbour evaluation
5. Casting shadow evaluation
6. Receiving solar evaluation

First look at screenshot named 'Surroundings'. Here we first select some buildings around the site according to their contribution of sunlight. For example there are buildings which cast shadow and there are other buildings which needs direct sunlight. They are done and you can see in the screenshots 'ShadowCasting Buildings' and  'Lot Surrounding Buildings' respectively.

## Evaluations

After assighning them to breps we proceed to code. This is done in the cluster called Point evaluation cluster. It is advised to make everything first then cluster them together. In the image 'Point evaluation not clustered' you can see how different nodes comes together and in the image 'Point evaluation cluster' you can see the clustered version. Now lets dive in per analysis.

1. Road distance evaluation:
Node: RoadDistance.( input: middlePoints, type hint: Point3d, list access ; input: roads, type hint Polyline)
...In the screenshot you can see how to make this analysis. Read the code from 'RoadDistance_evaluation.cs'. Here the inputs are Curve which is 3 curves (lines) shown in 'RoadDistance_evaluation_CURVES' and the second input is middle points which comes from node VoxelGrid 3d (Look Configuring and then 'Voxel_Creation'). 

2. Traffic evaluation:
Node: Traffic. ( input: middlePoints, type hint: Point3d, list access ; input: druk & middel & laag type hint: Polyline, list access)
...In the screenshot "Traffic_evaluation.jpg" you can see how to make this analysis. Read the code in Traffic_evaluation.cs )
...See Traffic.cs for the code and Traffic_evaluation.jpg for the image. The inputs here are three curves and again the middle points. In the previous analysis we made three lines and passed as multiple curves to SINGLE curve node but this time we pass three of them separately. See images 'Trafic_curve_node1', 'Trafic_curve_node2' and 'Trafic_curve_node3' which are the curves(selected as inputs) for druk, middel and laag respectievely.

3. Sound evaluation:
Node: TrafficNoise (input: middlePoints, type hint: Point3d, list access ; input: Curve45dB & Cure55dB type hint:Polyline, list access)
...See Sound_evaluation.cs for the code. The inputs are two curves and middle points. See Sound_curve_node1.jpg and Sound_curve_node2.jpg as they are the inputs for Curve50dB and Curve55dB respectievely.

4. Distance from neighbour evaluation:
...This evaluation contains two nodes.
...Node 1: Simplify shape (input: lot type hint: Curve, item access ; input: surrounding type hint: brep list access)
...The input for lot is Site_boundry.jpg (one curve) and for surrounding is node "Lot surrounding buildings" (see Surroundings.jpg).

...Node 2: Neighbor distance:(input: lot type hint: Curve, item access ;input: middlePoints, type hint: Point3d, list access ; input: simpleSurrounding type hint box list access)  
...input for lot is the same curve (See Site_boundry.jpg) , second input is middle points. Input for the last one is actually the output of the previous node.

... See the Simplify_shape.cs and Neighbor_distance.cs for the C# codes.


5. Solar casting shadow evaluation:
Node: Solar Analysis (input: middlePoints, type hint: Point3d, list access ; input: solarVectors type hint: Vector3d, list access, input: shadowCasters type hint:Mesh, list access )
...See Solar.jpg for the node. First input is again middle points. Second input is Solar Vectors (Flatten) coming from the output "SunVec" of node "SolarTimeAngles". Finally the third input is shadowcasters which is a mesh input from Surroundings node "ShadowCastingBuildings".

6. Receiving solar evaluation:
...This node containts various nodes. See Receiving_solar_eval.jpg for whole image of this evaluation. See NeighborFaces.cs, InfoBlock.cs and SolarEnvelope.cs respectievely for the codes of the nodes.

...Node: Neighbor faces: (see above)
...This node have first input lot which is the boundary of the site (see site_boundary.jpg). The second input is surrounding which is coming from "lot surrounding Buildings" (see Surroundings.jpg)

...Node: InfoBlock:(input: boolean type hint boolean , item access)
...Input of entrance is geometry (see: Voxel_creation.jpg from Configuring). Second input is just boolean.

...Node SolarEnvelope: (input: SunVecs & Normals type hint Vector3d, list access ; input: Boxels type hint Mesh, list access; input: Points type hint point3d, list access; input Percent type hint double, item access; input: shadowCasters type hint Mesh, list access)
...First input is Solar Vectors (Flatten) coming from the output "SunVec" of node "SolarTimeAngles" (see SolarTimeAngle.jpg in configuring). Second input is just the output of the node: InfoBlock (exit). Third input is just the output of the node "Neighbor faces" (pointsOut). Fourth input is just the output of the node "Neighbor faces" (normalsOut).Fifth input is just a slider and the last one is coming from the node "shadow casting Buildings" (see Surroundings.jpg).

 
## Combine/Preview all the analyses

The output of all the evaluations (see the images of the evaluations respectievely) which were RoadDistanceValues, TrafficValues, TrafficNoiseValues, pointsOut and NBlockage are the inputs of roadDistance, trafficValue, soundValues, distanceValues, solarBlockingValue and solarValue respectievely of node "point Attributes" (inside cluster). They all have input as list access, type hint double. See point_Attr.cs for the code and see point_Attr.jpg for image of this node. The outputs of all the evaluations are also inputs (info1 ... info6 respectievely) of another node "previewSwitcher" (outside cluster). See previewSwitcher.cs for code. The output of this color cluster can be then previewd using custom preview node of grasshopper. see custompreview2.jpg.
 
One of its output (preview_inf) go to color cluster named "color cluster" and the second one (preview_tekst) goes to panel which outputs the name of the evaluation. See color_cluster.jpg to see all the grasshopper nodes inside this cluster.


## Point value computation

First download grasshopper pluggin called read_csv. Then create one csv file from excel or simply download "eisen ruimtes" where there are weights given. See "PointValue.jpg". Lets go through nodes one by one

Node 1: ExSRead. This node comes from the installed plugin
...Inputs are path which is the location of the excel (CSV) file. , second input is just a boolean which connects with excel file. This gives output called 'Output' which will be input of the next nodes.

Now we can flip the output from 'Output' using flip node. 

Node 2: PointValues (input:  type hint System.Object, tree access; input: localCoordinates type access System.Object, list access; input: pointAttribute type System.Object, list access)

See PointValues.cs for the code.

...Inputs: first input (functionDemants) is the output of that flip node. Second input (localCoordinates) is the output of node "VoxelGrid 3d" (see Configuring Voxel_Creation.jpg). Third input (pointAttribute) is the output of the node "point Evaluation cluster" made above. 

Node 3: preview (input: functionDemants type hint System.Object, tree access)

See Preview.cs for the codes.

...Inputs: functionDemants which just comes from the node "ExRead".

Next final node in this group.

Node 4: VisualCluster (input: functionindex & nestedList type hint None, list access; input visualNumber type hint None, item access )

See VisualCluster.cs for the codes.

...Inputs: First input (functionIndex) is the output of node preview. Second input (nestedList) is the output of nestedOutput en finally last input is just a slider. This will enable to see different result of the point cloud by just sliding through the slider. this node also enables to see which evaluation is being processed from the output called visualName. 
...Output from this node "visual" can be previewd using Tag node where input L will be the middle points again, T will be visual. Similarly you can use custom preview node where input of G will be middle points and input of s will be M. See custompreview.jpg. 

## Generic Geo Information
See GG_info.jpg for full image of this group. 

Node 1: C# (input: localCoordinates type hint System.Object, list access)

...inputs: localCoordinates which is the output of node "VoxelGrid 3D". See csharp.cs for the codes.

Node 2: Voxel Info (inputs: Width & Length & Height type hint double, item access)

See Voxel_info for the codes.

...Inputs Width, Length and Height which comes from slider Width, Length and Height (See configuring part Voxel_Creation.jpg) 

Node 3: EdgesVisual (input: edgeCon type hint System.Object, list access; input: middlePoint see above)

See EdgesVisual.cs for the codes.

...Inputs: First input (edgeCon) comes from node C#. Second input is just middlePoint. 


## Growing Algorithm
Node: Growing (inputs: pointValues & pointRCoordinates & edgeConnections type hint System.Object, list access ; input: requestedArea type hint double, list access ; inputs: voxelArea & minimalGrade type hint double, item access; input: forceGround type hint bool, item access)

See Growing.cs for the codes and GrowingAlgo to see the full image of this group.

...Inputs: First input is output of node pointValues (nestedOutput). Second input comes from node "VoxelGrid 3D" localCoordinates. Third input comes from node c#. Fourth input comes from node pointValues RequestedArea. Fifth input comes from node Voxel Info. Sixth input is just a slider and the last input is just a toggle. 

See Growing_Output how the outputs are made to the meshes and then previewed using different colors. Here in the 'List index' node input of L is geometry (from node voxelGrid 3D) and the second input i comes from the Growing node.

Text or in other words the names of the functions can be previewd using Tag. Where L will be input of center points of those meshes combined and T comes from node preview. See textTag.jpg.

See presentation slides page 10 for the pseudo code and the flow chart of algorithm.

## Path finding 

see path_finder.jpg for full image of this group.

Node 1: middlepoints (input: cloud type hint System.Object, list access ; input: allMeshes type hint Mesh, list access; input allPoints type hint Point3d, list access)

...inputs: first input comes from nestedOutput of node Growing. Second input comes from node 'VoxelGrid 3D' geometry.  Third node is again middle points. 

see middlepoints.cs for the codes.

Node 2: Astar 

See astar.py for the codes.

...Inputs: first input is just startpoint in this case it is a number (integer) 0. Third input is output of previous node. Fourth input is middle points and fifth input is the output of the node C#. This can be previewd in similar manner like done before.




