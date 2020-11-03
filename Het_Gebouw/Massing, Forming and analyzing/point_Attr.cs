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
  private void RunScript(List<double> roadDistance, List<double> trafficValue, List<double> soundValues, List<double> distanceValues, List<double> solarBlockingValue, List<double> solarValue, ref object pointAttribute)
  {
    // bring all the normalized values together in one single tuple per pointindex

    List<Tuple<double,double,double,double,double,double>> attributes = new List<Tuple<double,double,double,double,double,double>>();
    int solarCorrection = 4;

    if (soundValues.Count == distanceValues.Count && distanceValues.Count == solarBlockingValue.Count && solarBlockingValue.Count == solarValue.Count)
    {
      for (int i = 0; i < soundValues.Count; i++)
      {
        Tuple<double,double,double,double,double,double> attribute = Tuple.Create(roadDistance[i], trafficValue[i], soundValues[i], distanceValues[i], solarBlockingValue[i] * Math.Pow(10, solarCorrection), solarValue[i]);
        attributes.Add(attribute);
      }
    }
    pointAttribute = attributes;

  }

  // <Custom additional code> 

  // </Custom additional code> 
}