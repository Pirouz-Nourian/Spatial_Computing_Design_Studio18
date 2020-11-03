#Configuring

In Configuring voxels are made.


### There is no simplified mesh models created for circulation flow since our group had lots of disturbance. At this time 2 members of our group left leaving us with huge amount of undone work. We therefore focussed on programming part.

Node: VexelGrid 3D

inputs:
... curve, vL, vW, totalH and r. where curve is the boundary of the site (see site_boundary). All other inputs are slider. see the code at Voxel_creation.cs.


Node: SolarWinHours

inputs:
...W and h which are sliders.

Node: SolarTimeAngles
 
inputs: 
... yr which is a number, mth which comes from generic grasshopper node named Filter which basically filters few parameters (see Sun_simulator.jpg), hrs which comes from the node "SolarWindows", tzone which is a number like 3.5, latitude which is a number, longitude which is a number and the last input which is scaleRad which is a number like 500.

See SolarTimeAngle.cs for the codes.

important output from this node is sun vectors which are used in section Massing.