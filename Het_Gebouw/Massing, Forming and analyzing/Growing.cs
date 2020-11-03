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
  private void RunScript(List<System.Object> pointValues, List<System.Object> pointRCoordinates, List<System.Object> edgeConnections, List<double> requestedArea, double voxelArea, double minimalGrade, bool forceGround, ref object A, ref object B, ref object C, ref object D, ref object E, ref object F, ref object G, ref object H, ref object I, ref object J, ref object nestedOutput)
  {

    // growing variables
    int totalIterations = 15;
    double minimalPointGrade = 10 * minimalGrade;

    int force = 0;
    if (forceGround){force = 1;}

    // create ideal starting point
    List<int> bestPointIndex = new List<int>();
    List<List<int>> nestedBestPointIndex = new List<List<int>>();
    List<List<int>> nestedpoints = new List<List<int>>();
    List<int> occupied = new List<int>(new int [pointRCoordinates.Count]); // 0 == free/ 1 == taken


    // open nested values
    List<Tuple<int,int,int>> relativeCoordinatesNew = new List<Tuple<int,int,int>>();
    List<Tuple<int,int>> edgeConnectionsNew = new List<Tuple<int,int>>();
    List<List<double>> pointValuesNew = new List<List<double>>();

    foreach (Tuple<int,int,int> i in pointRCoordinates){relativeCoordinatesNew.Add(i);}
    foreach (Tuple<int,int> i in edgeConnections){edgeConnectionsNew.Add(i);}
    foreach (List<double> i in pointValues) {pointValuesNew.Add(i);}

    // look for ideal points for each function
    foreach (List<double> buildingType in pointValues)
    {
      Tuple<int,double> bestPoint = BestPointIndex(buildingType, occupied, relativeCoordinatesNew, force);
      occupied[bestPoint.Item1] = 1;
      bestPointIndex.Add(bestPoint.Item1);

      List<int> tempList = new List<int>();
      tempList.Add(bestPoint.Item1);
      nestedBestPointIndex.Add(tempList);
    }

    // create information tuples
    List<Tuple<double, double, double, List<double>>> pointFunctionInfo = new List<Tuple<double, double, double, List<double>>>();
    for (int function = 0; function < requestedArea.Count; function++)
    {
      double areaMax = requestedArea[function];
      // create a Tuple with info about every point for eacht function. index == function. Item1 == minimal grade.Item2 == voxelarea. Item3 == required Area. Item4 == every pointvalues
      Tuple <double, double, double, List<double>> info = Tuple.Create(minimalPointGrade, voxelArea, areaMax, pointValuesNew[function]);
      pointFunctionInfo.Add(info);
    }

    // growing functions
    for (int iteration = 0; iteration < totalIterations; iteration++)
    {
      for (int function = 0; function < requestedArea.Count; function++)
      {
        growingStep(occupied, nestedBestPointIndex[function], edgeConnectionsNew, pointFunctionInfo[function]);
      }
    }

    // alert if a area is not satisfied
    for (int function = 0; function < requestedArea.Count; function++)
    {
      if(nestedBestPointIndex[function].Count * pointFunctionInfo[function].Item2 < pointFunctionInfo[function].Item3)
      {
        Component.AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "some function areas are not satisfied");
      }
    }

    // outputs
    A = nestedBestPointIndex[0];
    B = nestedBestPointIndex[1];
    C = nestedBestPointIndex[2];
    D = nestedBestPointIndex[3];
    E = nestedBestPointIndex[4];
    F = nestedBestPointIndex[5];
    G = nestedBestPointIndex[6];
    H = nestedBestPointIndex[7];
    I = nestedBestPointIndex[8];
    J = nestedBestPointIndex[9];
    nestedOutput = nestedBestPointIndex;

  }

  // <Custom additional code> 

  private Tuple<int,double> BestPointIndex (List<double> buildingType, List<int> occupiedList, List<Tuple<int,int,int>> coordinates, int ground)
  {
    int pointIndex = 0;
    double storedValue = 0;
    int localBestPoint = 0;
    foreach (double pointValue in buildingType)
    {
      if (ground == 0)
      {
        if (pointValue > storedValue && occupiedList[pointIndex] == 0)
        {
          storedValue = pointValue;
          localBestPoint = pointIndex;
        }
      }
      else
      {
        if (pointValue > storedValue && occupiedList[pointIndex] == 0 && coordinates[pointIndex].Item3 == 0)
        {
          storedValue = pointValue;
          localBestPoint = pointIndex;
        }
      }
      pointIndex++;
    }
    Tuple<int,double> bestPointInfo = Tuple.Create(localBestPoint, storedValue);
    return bestPointInfo;
  }

  private void growingStep (List<int> occupiedList, List<int> updatePointIndexList, List<Tuple<int,int>> edgeConnections, Tuple<double, double, double, List<double>> staticInfo)
  {
    List<int> potentialPointIndexes = new List<int>();
    foreach (int pointIndex in updatePointIndexList)
    {
      foreach (Tuple<int,int> connection in edgeConnections)
      {
        if (connection.Item1 == pointIndex && occupiedList[connection.Item2] == 0 && staticInfo.Item4[connection.Item2] > staticInfo.Item1)
        {
          if ((updatePointIndexList.Count + potentialPointIndexes.Count) * staticInfo.Item2 < staticInfo.Item3)
          {
            occupiedList[connection.Item2] = 1;
            potentialPointIndexes.Add(connection.Item2);
          }
        }
      }
    }
    foreach (int potentialPointIndex in potentialPointIndexes){updatePointIndexList.Add(potentialPointIndex);}
  }


  // </Custom additional code> 
}