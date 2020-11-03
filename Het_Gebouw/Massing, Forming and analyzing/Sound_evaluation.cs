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
  private void RunScript(List<Point3d> middlePoints, List<Polyline> Curve45dB, List<Polyline> Curve50dB, List<Polyline> Curve55dB, List<Polyline> Curve60dB, ref object TrafficNoiseValues)
  {

    // calculates the dba levels created by roadcurves on a point
    // only accurate in low traffic situations (point source)

    //initial Values are 0 for all points
    List<double> soundValues = new List<double>(new double[middlePoints.Count]);

    // update list based on the soundvalues created by the roads
    // source: https://www.atlasleefomgeving.nl

    if(Curve60dB.Count > 0)
    {
      listUpdater(soundValues, 60, Curve60dB, middlePoints);
    }
    if(Curve55dB.Count > 0)
    {
      listUpdater(soundValues, 55, Curve55dB, middlePoints);
    }
    if(Curve50dB.Count > 0)
    {
      listUpdater(soundValues, 50, Curve50dB, middlePoints);
    }
    if(Curve45dB.Count > 0)
    {
      listUpdater(soundValues, 45, Curve45dB, middlePoints);
    }

    //normalize values
    double divider = soundValues.Max();
    List<double> normalizedValues = new List<double>();

    foreach (double waarde in soundValues)
    {
      normalizedValues.Add((waarde / divider) * 100);
    }

    TrafficNoiseValues = normalizedValues;

  }

  // <Custom additional code> 

  public List<double> listUpdater (List<double> soundValues, int Value, List<Polyline> curveListValue, List<Point3d> middlePoints)
  {
    int pointID = 0;
    foreach (Point3d point in middlePoints)
    {
      foreach (Polyline line in curveListValue)
      {
        double distance = 0;
        double lineDistance = point.DistanceTo(line.ClosestPoint(point));

        if (lineDistance > distance)
        {
          double sValue = Value - 10 * Math.Log10((4 * Math.PI * Math.Pow(lineDistance, 2)) / 4);
          if(soundValues[pointID] < sValue)
          {
            soundValues[pointID] = sValue;
          }
          distance = lineDistance;
        }
      }
      pointID++;
    }
    return soundValues;
  }

  // </Custom additional code> 
}