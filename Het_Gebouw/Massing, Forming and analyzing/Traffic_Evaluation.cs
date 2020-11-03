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
  private void RunScript(List<Point3d> middlePoints, List<Polyline> druk, List<Polyline> middel, List<Polyline> laag, ref object TrafficValues)
  {

    // calculate a generic value based on the distance from the point to a road & the crowdedness of that road

    //initial Values are 0 for all points
    List<double> DrukteIndex = new List<double>(new double[middlePoints.Count]);

    // calulate values based on the crowdedness of the curves
    if(druk.Count > 0)
    {
      listUpdater(DrukteIndex, 100, druk, middlePoints);
    }
    if(middel.Count > 0)
    {
      listUpdater(DrukteIndex, 50, middel, middlePoints);
    }
    if(laag.Count > 0)
    {
      listUpdater(DrukteIndex, 20, laag, middlePoints);
    }

    //normalize values
    double divider = DrukteIndex.Max();
    List<double> normalizedValues = new List<double>();

    foreach (double waarde in DrukteIndex)
    {
      normalizedValues.Add((waarde / divider) * 100);
    }

    TrafficValues = normalizedValues;

  }

  // <Custom additional code> 

  public List<double> listUpdater (List<double> DrukteIndex, int Value, List<Polyline> curveListValue, List<Point3d> middlePoints)
  {
    int pointID = 0;
    foreach (Point3d point in middlePoints)
    {
      foreach (Polyline line in curveListValue)
      {
        double distance = 10000;
        double lineDistance = point.DistanceTo(line.ClosestPoint(point));

        if (lineDistance < distance)
        {
          double sValue = Value - lineDistance * 1.5;
          if(DrukteIndex[pointID] < sValue)
          {
            DrukteIndex[pointID] = sValue;
          }
          distance = lineDistance;
        }
      }
      pointID++;
    }
    return DrukteIndex;
  }

  // </Custom additional code> 
}