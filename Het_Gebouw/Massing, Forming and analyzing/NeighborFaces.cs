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
  private void RunScript(Curve lot, List<Brep> surrounding, ref object pointsOut, ref object normalsOut)
  {


    // set inputs & variables
    List<Brep> buildings = surrounding;
    Curve location = lot;

    Plane localPlane;

    Rhino.Geometry.Collections.BrepEdgeList edges;
    List<BrepEdge> baseLines = new List<BrepEdge>();
    List<Box> bBoxes = new List<Box>();
    List<NurbsCurve> EvalLines = new List<NurbsCurve>();
    List<BrepFace> allFaces = new List<BrepFace>();
    List<BrepFace> normalFaces = new List<BrepFace>();
    double[] result;

    int uDivision = 0;
    int vDivision = 0;

    List<Point3d> points = new List<Point3d>();
    List<Vector3d> normals = new List<Vector3d>();

    // adjustment variables (can be used to make the grid of normals on the surface more dense)

    double lHold = 3;
    double hHold = 6;

    double uDistance = 5;
    double vDistance = 3;


    // temporary lists
    List<double> ding = new List<double>();
    List<Line> ding2 = new List<Line>();

    // calculate location centrepoint
    Point3d centre = AreaMassProperties.Compute(lot).Centroid;
    centre[2] = centre[2] + 3;

    // join the buildings next to eachother
    Array blocks = Brep.CreateBooleanUnion(buildings, 0.01);

    // create orientated bounding boxes to simplify the surroundings
    foreach (Brep block in blocks)
    {
      edges = block.Edges;
      Curve evalLine = (Curve) edges[0];

      if (evalLine.GetLength(0.1) < lHold)
      {
        foreach (BrepEdge edge in edges)
        {
          if (edge.GetLength(0.1) > lHold &&
            Math.Abs(edge.PointAtEnd[2] - edge.PointAtStart[2]) < 1 &&
            edge.PointAtEnd[2] < hHold)
          {
            evalLine = (Curve) edge;
          }
        }
      }
      Vector3d direction = new Vector3d(evalLine.PointAt(1) - evalLine.PointAt(0));
      Vector3d perpDir = Vector3d.CrossProduct(direction, Vector3d.ZAxis * -1);
      localPlane = new Plane(evalLine.PointAt(0), direction, perpDir);
      BoundingBox boundBox = block.GetBoundingBox(localPlane);
      Box bBox = new Box(localPlane, boundBox);
      bBoxes.Add(bBox);
    }

    // select faces that are orientated to the centrepoint of the lot
    foreach (Box box in bBoxes)
    {
      Brep brbox = box.ToBrep();
      Rhino.Geometry.Collections.BrepFaceList faces = brbox.Faces;

      foreach (BrepFace face in faces)
      {
        allFaces.Add(face);
        Point3d faceCentrePoint = AreaMassProperties.Compute(face).Centroid;
        Line evalLine = new Line(faceCentrePoint, centre);
        EvalLines.Add(evalLine.ToNurbsCurve());
      }
      foreach (NurbsCurve line in EvalLines)
      {

        Rhino.Geometry.Intersect.Intersection.CurveBrep(line, brbox, 0.01, 0.01, out result);
        if (result.Length == 1)
        {
          int index = EvalLines.IndexOf(line);
          normalFaces.Add(allFaces[index]);
        }
      }
    }

    // split the faces to get a grid of normals
    foreach (BrepFace face in normalFaces)
    {
      double width = 0;
      double height = 0;
      face.GetSurfaceSize(out width, out height);
      if (uDistance > width)
      {
        uDivision = 1;
      }
      else
      {
        uDivision = Convert.ToInt32(width / uDistance);
      }
      if (vDistance > height)
      {
        vDivision = 2;
      }
      else
      {
        vDivision = Convert.ToInt32(height / vDistance);

      }
      ding.Add(uDivision);

      for (int i = 0; i < uDivision; i++)
      {
        for (int j = 0; j < vDivision; j++)
        {
          points.Add(face.PointAt(i * uDistance, j * vDistance));
          normals.Add(face.NormalAt(1, 1));
        }
      }
    }
    pointsOut = points;
    normalsOut = normals;


  }

  // <Custom additional code> 

  // </Custom additional code> 
}