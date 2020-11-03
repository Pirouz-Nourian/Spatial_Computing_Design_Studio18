using System;
using System.Collections;
using System.Collections.Generic;

using Rhino;
using Rhino.Geometry;

using Grasshopper;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;

using System.IO;
using System.Linq;
using System.Data;
using System.Drawing;
using System.Reflection;
using System.Windows.Forms;
using System.Xml;
using System.Xml.Linq;
using System.Runtime.InteropServices;

using Rhino.DocObjects;
using Rhino.Collections;
using GH_IO;
using GH_IO.Serialization;

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
  private void RunScript(List<Vector3d> SunVecs, List<Mesh> Boxels, List<Point3d> Points, List<Vector3d> Normals, double Percent, List<Mesh> shadowCasters, ref object Blockage, ref object NBlockage, ref object NonBlocking, ref object FBoxels)
  {
                                        /*
  The algorithm is designed based on the following papers:

  [1] F. De Luca, “Solar Form-finding . Subtractive Solar Envelope and Integrated Solar Collection Computational Method for High-rise Bui ....,”
  Proc. 37th Annu. Conf. Assoc. Comput. Aided Des. Archit. (ACADIA 2017), no. November, pp. 212–221, 2017.

  [2] P. Nourian, R. Gonçalves, S. Zlatanova, K. A. Ohori, and A. Vu Vo,
  “Voxelization algorithms for geospatial applications: Computational methods for voxelating spatial datasets of 3D city models containing 3D surface, curve and point data models,”
  MethodsX, vol. 3, pp. 69–86, 2016.

  The code has been written by Pirouz Nourian and is licensed with 'a modified BSD 3-Clause License'
  A full description of the license is privided in the git repository: https://gitlab.com/Pirouz-Nourian/spatial_computing/tree/master
  Copyright (c) 2018, Pirouz Nourian
  All rights reserved.
*/
    int PointCount = Points.Count;
    int NormalCount = Normals.Count;
    int VoxelCount = Boxels.Count;
    if((Percent < 0) || (Percent > 1)){throw new Exception("the percentage tolerance provided must be a number between 0 and 1!");}
    //if((PointCount < 1) || (n < 1) || (VoxelCount < 1)){throw new Exception("The number of items in some inputs is not sufficient!");}
    if(PointCount != NormalCount){throw new Exception("The number of normal vectors and points must be the same!");}

    double[] BlockedFluxes = new double[VoxelCount];
    bool[] IsNotBlocking = new bool[VoxelCount];


    List<Mesh> FilteredBoxels = new List<Mesh>();

    // custom added code (shadowcast)

    int evalLength = 500;
    List<List<Vector3d>> NestedValidSunVecs = new List<List<Vector3d>>();

    for(int k = 0;k < PointCount;k++) //foreach(Point3d Point in Points){
    {
      List<Vector3d> ValidSunVecs = new List<Vector3d>();
      Point3d Point = Points[k];
      foreach (Vector3d SunVec in SunVecs)
      {
        Line solarCurve = new Line(Point, -1 * SunVec, evalLength);
        Curve solarNurb = solarCurve.ToNurbsCurve();
        int counter = 0;

        // if solar curve is not intersecting with buildings in the environment it is allowed to be used in the rest of the evaluation
        foreach (Mesh building in shadowCasters)
        {
          int[] result;
          Rhino.Geometry.Intersect.Intersection.MeshLine(building, solarCurve, out result);
          if (result != null)
          {
            counter++;
          }
        }
        if (counter == 0)
        {
          ValidSunVecs.Add(SunVec);
        }
      }
      NestedValidSunVecs.Add(ValidSunVecs);
    }
    int n = 0;

    // end custom code


    for(int i = 0; i < VoxelCount; i++) //foreach(Mesh Boxel in Boxels){
    {
      Mesh Boxel = Boxels[i];
      double BlockedFlux = 0;
      for(int k = 0;k < PointCount;k++) //foreach(Point3d Point in Points){
      {
        n = NestedValidSunVecs[k].Count;
        Point3d Point = Points[k];
        Vector3d Normal = Normals[k];
        foreach(Vector3d SunVec in NestedValidSunVecs[k])
        {
          Vector3d NSunVec = -SunVec;
          double PotentialFlux = Vector3d.Multiply(NSunVec, Normal);
          if(PotentialFlux > 1)
          {
            throw new Exception("some sunvectors or normal vectors have a norm greater than 1!");
          }
          if(PotentialFlux > 0)
          {
            Ray3d Ray = new Ray3d(Point, NSunVec);
            double RayParameter = Rhino.Geometry.Intersect.Intersection.MeshRay(Boxel, Ray);
            bool Hit = (RayParameter > 0);
            if(Hit)
            {
              BlockedFlux = BlockedFlux + PotentialFlux;
            }
          }
        }
      }
      int Sum = PointCount * n;//in order to relativize the blockage numbers, we divide them all by the total number of rays which could have been blocked
      BlockedFlux = BlockedFlux / Sum;
      BlockedFluxes[i] = BlockedFlux;
      if(BlockedFlux < Percent)
      {
        FilteredBoxels.Add(Boxel);
        IsNotBlocking[i] = true;
      }
      else
      {
        IsNotBlocking[i] = false;
      }
    }


    //normalize (custom code)
    double divider = BlockedFluxes.Max();
    List<double> normalizedValues = new List<double>();

    foreach (double waarde in BlockedFluxes)
    {
      normalizedValues.Add((waarde / divider) * 100);
    }




    Blockage = BlockedFluxes;
    NBlockage = normalizedValues;
    NonBlocking = IsNotBlocking;
    FBoxels = FilteredBoxels;
  }

  // <Custom additional code> 

  // </Custom additional code> 
}