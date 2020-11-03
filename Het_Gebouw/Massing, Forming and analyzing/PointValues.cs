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
  private void RunScript(DataTree<System.Object> functionDemants, List<System.Object> localCoordinates, List<System.Object> pointAttribute, ref object RequestedArea, ref object nestedOutput)
  {

    // calculates a livability value for every point
    // based a formula that uses the demants and the calculated point attributes

    // create new lists
    List<List<double>> nestedValues = new List<List<double>>();
    List<double> FunctionArea = new List<double>();

    for (int i = 1; i < functionDemants.BranchCount; i++)
    {
      // create a area list per function based on the values of the demants
      FunctionArea.Add(Convert.ToDouble(functionDemants.Branch(i)[7]));

      // set weigths based on the values of the Demants
      List<double> pointGrades = new List<double>();
      List<double> weights = new List<double>();
      List<object> datastream = functionDemants.Branch(i);
      for (int j = 1; j < datastream.Count; j++)
      {
        double tempValue = Convert.ToDouble(datastream[j]);
        weights.Add(tempValue);
      }

      foreach (Tuple<double,double,double,double,double,double> point in pointAttribute)
      {
        // formula giving the points their value
        double roadDistance = point.Item1 * weights[0];
        double trafficValue = point.Item2 * weights[1];
        double noiseValue = (point.Item3 / 45) * weights[2];
        double distanceValue = weights[3] * point.Item4;
        double solarValue = weights[5] * point.Item6 - weights[4] * point.Item5;
        if (solarValue < 0) {solarValue = 1;}
        double tempValue = roadDistance + distanceValue + solarValue - noiseValue + 1.5 * trafficValue;
        if (tempValue < 0){tempValue = 1;}
        pointGrades.Add(tempValue * 100);
      }

      // normalize the values
      double divider = pointGrades.Max();
      List<double> normalizedValues = new List<double>();

      foreach (double waarde in pointGrades)
      {
        normalizedValues.Add((waarde / divider) * 100);
      }

      nestedValues.Add(normalizedValues);
    }

    //output
    RequestedArea = FunctionArea;
    nestedOutput = nestedValues;



  }

  // <Custom additional code> 

  // </Custom additional code> 
}