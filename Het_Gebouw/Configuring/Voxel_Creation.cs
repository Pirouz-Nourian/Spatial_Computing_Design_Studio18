using System;
using System.Collections;
using System.Collections.Generic;

using Rhino;
using Rhino.Geometry;

using Grasshopper;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;



/// <summary>
/// This class will be instantiated on demand by the Script component.
/// </summary>
public class Script_Instance : GH_ScriptInstance
{
#region Utility functions
  /// <summary>Print a String to the [Out] Parameter of the Script component.</summary>
  /// <param name="text">String to print.</param>
  private void Print(string text) { /* Implementation hidden. */ }
  /// <summary>Print a formatted String to the [Out] Parameter of the Script component.</summary>
  /// <param name="format">String format.</param>
  /// <param name="args">Formatting parameters.</param>
  private void Print(string format, params object[] args) { /* Implementation hidden. */ }
  /// <summary>Print useful information about an object instance to the [Out] Parameter of the Script component. </summary>
  /// <param name="obj">Object instance to parse.</param>
  private void Reflect(object obj) { /* Implementation hidden. */ }
  /// <summary>Print the signatures of all the overloads of a specific method to the [Out] Parameter of the Script component. </summary>
  /// <param name="obj">Object instance to parse.</param>
  private void Reflect(object obj, string method_name) { /* Implementation hidden. */ }
#endregion

#region Members
  /// <summary>Gets the current Rhino document.</summary>
  private readonly RhinoDoc RhinoDocument;
  /// <summary>Gets the Grasshopper document that owns this script.</summary>
  private readonly GH_Document GrasshopperDocument;
  /// <summary>Gets the Grasshopper script component that owns this script.</summary>
  private readonly IGH_Component Component;
  /// <summary>
  /// Gets the current iteration count. The first call to RunScript() is associated with Iteration==0.
  /// Any subsequent call within the same solution will increment the Iteration count.
  /// </summary>
  private readonly int Iteration;
#endregion

  /// <summary>
  /// This procedure contains the user code. Input parameters are provided as regular arguments,
  /// Output parameters as ref arguments. You don't have to assign output parameters,
  /// they will have a default value.
  /// </summary>
  private void RunScript(Curve curve, double vL, double vW, double vH, double totalH, double r, ref object geometry, ref object middlepoints, ref object localCoordinates)
  {
    // check if inputs are valid
    if (vL == 0 || vW == 0 || vH == 0)
    {
      Component.AddRuntimeMessage(GH_RuntimeMessageLevel.Error, "invalid input");
    }
    else
    {
      // assign variables
      double vLength = vL;
      double vWidth = vW;
      double vHeight = vH;
      double rotator = r;
      Curve lot = curve;

      // create lists
      List<Point3d> uPoints = new List<Point3d>();
      List<Box> voxels = new List<Box>();
      List<Tuple<int,int,int>> indexList = new List<Tuple<int,int,int>>();

      // construct bounding box & rotating baseplane
      Point3d p0 = new Point3d(0.0, 0.0, 0.0);
      Vector3d v0 = new Vector3d(0.1, 0.0, 0.0);
      Vector3d v1 = new Vector3d(0.0, 1.0, 0.0);
      Plane plane = new Plane(p0, v0, v1);

      plane.Transform(Transform.Rotation(rotator * 2 * Math.PI, AreaMassProperties.Compute(lot).Centroid));
      BoundingBox bBox = lot.GetBoundingBox(plane);

      // create rotating basesurface based on created bounding box
      Point3d point1 = bBox.Min;
      Point3d point2 = new Point3d (bBox.Min[0], bBox.Max[1], bBox.Min[2]);
      Point3d point3 = bBox.Max;
      Point3d point4 = new Point3d (bBox.Max[0], bBox.Min[1], bBox.Min[2]);

      Surface baseplane = NurbsSurface.CreateFromCorners(point1, point2, point3, point4);
      baseplane.Transform(Transform.Rotation(rotator * 2 * Math.PI, AreaMassProperties.Compute(lot).Centroid));

      // create a evaluation box based on the building location
      Curve baseCurve = lot;
      baseCurve.Translate(0.0, 0.0, -2.0);
      Extrusion evalBox = Extrusion.Create(baseCurve, 4, true);
      Brep box = evalBox.ToBrep(true);

      // calculate and place the points on the location
      double width;
      double length;
      baseplane.GetSurfaceSize(out width, out length);

      // create counters for the creation loop
      int uMax = (int) Math.Ceiling(width / vWidth);
      int vMax = (int) Math.Ceiling(length / vLength);
      int hMax = (int) Math.Ceiling(totalH / vHeight);

      // point creation loop
      for (int u = 0; u < uMax; u++ )
      {
        for (int v = 0; v < vMax; v++)
        {
          Point3d point = baseplane.PointAt(u * vWidth, v * vLength);
          if (box.IsPointInside(point, 0.1, true))
          {
            for (int h = 0; h < hMax; h++)
            {
              point.Z = h * vHeight + point1[2];
              Tuple<int,int,int> relativeCoordinate = Tuple.Create(u, v, h);
              indexList.Add(relativeCoordinate);
              uPoints.Add(point);
            }
          }
        }
      }

      // create voxels based on the created points
      foreach (Point3d point in uPoints)
      {
        Plane origin = new Plane(point, v0, v1);
        Interval x = new Interval(-0.5 * vLength, 0.5 * vLength);
        Interval y = new Interval(-0.5 * vWidth, 0.5 * vWidth);
        Interval z = new Interval(0, vHeight);

        origin.Transform(Transform.Rotation(rotator * 2 * Math.PI, point));

        Box voxel = new Box(origin, x, y, z);
        voxels.Add(voxel);
      }

      // outputs
      geometry = voxels;
      middlepoints = uPoints;
      localCoordinates = indexList;
    }
  }

  // <Custom additional code> 


  // </Custom additional code> 
}