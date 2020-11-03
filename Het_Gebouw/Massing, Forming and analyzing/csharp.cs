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
  private void RunScript(List<System.Object> localCoordinates, ref object A)
  {
    //create edges index
    List<Tuple<int,int>> edges = new List<Tuple<int,int>>();

    int indexi = 0;


    foreach (Tuple<int,int,int> i in localCoordinates)
    {
      int indexj = 0;
      foreach (Tuple<int,int,int> j in localCoordinates)
      {
        if (i != j)
        {
          if (i.Item1 == j.Item1 && i.Item2 == j.Item2 && Math.Abs(j.Item3 - i.Item3) == 1)
          {
            Tuple<int,int> edgeF = Tuple.Create(indexi, indexj);
            edges.Add(edgeF);
          }

          else if (i.Item1 == j.Item1 && i.Item3 == j.Item3 && Math.Abs(j.Item2 - i.Item2) == 1)
          {
            Tuple<int,int> edgeF = Tuple.Create(indexi, indexj);
            edges.Add(edgeF);
          }

          else if (i.Item2 == j.Item2 && i.Item3 == j.Item3 && Math.Abs(j.Item1 - i.Item1) == 1)
          {
            Tuple<int,int> edgeF = Tuple.Create(indexi, indexj);
            edges.Add(edgeF);
          }
        }
        indexj++;
      }
      indexi++;
    }
    A = edges;

  }

  // <Custom additional code> 

  // </Custom additional code> 
}