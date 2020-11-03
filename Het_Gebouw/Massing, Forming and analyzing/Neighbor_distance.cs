using System;
using System.Collections;
using System.Collections.Generic;

using Rhino;
using Rhino.Geometry;

using Grasshopper;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;

using System.Linq;

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
  private void RunScript(Curve lot, List<Point3d> middlePoints, List<Box> simpleSurrounding, ref object pointsOut)
  {

    // calculates the distance of a point to the closest building to that point

    // set inputs & variables
    Curve location = lot;

    List<BrepEdge> baseLines = new List<BrepEdge>();
    List<Box> bBoxes = new List<Box>();
    List<NurbsCurve> EvalLines = new List<NurbsCurve>();
    List<BrepFace> allFaces = new List<BrepFace>();
    List<BrepFace> normalFaces = new List<BrepFace>();
    List<double> distances = new List<double>(new double[middlePoints.Count]);
    double[] result;

    List<Point3d> points = new List<Point3d>();
    List<Vector3d> normals = new List<Vector3d>();

    // select faces that are orientated to the points by drawing a line from every surface to a centrepoint and counting intersections on itself
    // if there are none the surface faces the building is faceing the centrepoint
    foreach (Box box in simpleSurrounding)
    {
      Brep brbox = box.ToBrep();
      Rhino.Geometry.Collections.BrepFaceList faces = brbox.Faces;

      foreach (BrepFace face in faces)
      {
        allFaces.Add(face);
        Point3d faceCentrePoint = AreaMassProperties.Compute(face).Centroid;
        Line evalLine = new Line(faceCentrePoint, AreaMassProperties.Compute(lot).Centroid);
        EvalLines.Add(evalLine.ToNurbsCurve());
      }
      foreach (NurbsCurve line in EvalLines)
      {

        Rhino.Geometry.Intersect.Intersection.CurveBrep(line, brbox, 0.01, 0.01, out result);
        if (result.Length == 1)
        {
          int index = EvalLines.IndexOf(line);
          int pIndex = 0;

          // calculate distance from neighbour point to point of building
          foreach (Point3d point in middlePoints)
          {
            double u;
            double v;
            allFaces[index].ClosestPoint(point, out u, out v);
            Point3d evalPoint = allFaces[index].PointAt(u, v);
            double distance = point.DistanceTo(evalPoint);

            // if the distance is bigger than the saved distance update the distance to the smaller value
            if (distances[pIndex] > distance || distances[pIndex] == 0)
            {
              distances[pIndex] = distance;
            }

            pIndex++;

          }

          normalFaces.Add(allFaces[index]);
        }
      }
    }

    //normalize
    double divider = distances.Max();
    List<double> normalizedValues = new List<double>();

    foreach (double waarde in distances)
    {
      normalizedValues.Add((waarde / divider) * 100);
    }

    pointsOut = normalizedValues;

  }

  // <Custom additional code> 

  // </Custom additional code> 
}