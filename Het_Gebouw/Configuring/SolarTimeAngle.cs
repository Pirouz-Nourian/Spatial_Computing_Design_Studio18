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
  private void RunScript(int yr, int mth, int day, double hrs, double tzone, double latitude, double longitude, double northAng, double scaleRad, ref object zenAng, ref object azi, ref object hrAngle, ref object solarElev, ref object eqaTime, ref object solDec, ref object sunPt, ref object sunVec)
  {
    // The Solar Position algorithm is based on National Oceanic and Atmospheric Administration's Solar Position Calculator http://www.srrb.noaa.gov/highlights/sunrise/azel.html
    //Code is ported into vb.net and integrated into Grasshopper by Ted Ngai Jan 30, 2009 www.tedngai.net
    //Translation to C# by Pirouz Nourian
    double hourAngle = 0;
    double haRad = 0;
    double csz = 0;
    double zenith = 0;
    double azDenom = 0;
    double azRad = 0;
    double azimuth = 0;
    double exoatmElevation = 0;
    double refractionCorrection = 0;
    double te = 0;
    double solarZen = 0;
    double elevation = 0;
    double coszen = 0;

    //timenow is GMT time for calculation
    double timenow = hrs - tzone;
    longitude = longitude * -1;

    double JD = calcJD(yr, mth, day);
    double T = calcTimeJulianCent(JD + timenow / 24.0);
    double R = calcSunRadVector(T);
    double alpha = calcSunRtAscension(T);
    double theta = calcSunDeclination(T);
    double Etime = calcEquationOfTime(T);
    //Dim theta As Double = calcGeomMeanLongSun(T)

    double eqTime = Etime;
    double solarDec = theta;
    double earthRadVec = R;

    double solarTimeFix = eqTime - 4.0 * longitude + 60.0 * -tzone;
    double trueSolarTime = hrs * 60 + solarTimeFix;

    if (trueSolarTime > 1440) {
      trueSolarTime -= 1440;
    }

    hourAngle = trueSolarTime / 4.0 - 180.0;
    if (hourAngle < -180) {
      hourAngle = hourAngle + 360;
    }

    haRad = degToRad(hourAngle);

    csz = Math.Sin(degToRad(latitude)) * Math.Sin(degToRad(solarDec)) + Math.Cos(degToRad(latitude)) * Math.Cos(degToRad(solarDec)) * Math.Cos(haRad);
    if (csz > 1.0) {
      csz = 1.0;
    } else if (csz < -1.0) {
      csz = -1;
    }

    zenith = radToDeg(Math.Acos(csz));
    azDenom = (Math.Cos(degToRad(latitude)) * Math.Sin(degToRad(zenith)));


    if (Math.Abs(azDenom) > 0.001) {
      azRad = ((Math.Sin(degToRad(latitude)) * Math.Cos(degToRad(zenith))) - Math.Sin(degToRad(solarDec))) / azDenom;
      if (Math.Abs(azRad) > 1.0) {
        if (azRad < 0) {
          azRad = -1.0;
        } else {
          azRad = 1.0;
        }
      }

      azimuth = 180.0 - radToDeg(Math.Acos(azRad));
      if (hourAngle > 0.0) {
        azimuth = -azimuth;
      }
    } else {
      if (latitude > 0.0) {
        azimuth = 180.0;
      } else {
        azimuth = 0.0;
      }
    }

    if (azimuth < 0.0) {
      azimuth = azimuth + 360;
    }

    exoatmElevation = 90.0 - zenith;
    if (exoatmElevation > 85.0) {
      refractionCorrection = 0.0;
    } else {
      te = Math.Tan(degToRad(exoatmElevation));
      if (exoatmElevation > 5.0) {
        refractionCorrection = 58.1 / te - 0.07 / (te * te * te) + 8.6E-05 / (te * te * te * te * te);
      } else if (exoatmElevation > -0.575) {
        refractionCorrection = 1735.0 + exoatmElevation * (-518.2 + exoatmElevation * (103.4 + exoatmElevation * (-12.79 + exoatmElevation * 0.711)));
      } else {
        refractionCorrection = -20.774 / te;
      }
      refractionCorrection = refractionCorrection / 3600.0;
    }

    solarZen = zenith - refractionCorrection;
    elevation = (Math.Floor(100 * (90.0 - solarZen))) / 100;
    if (solarZen < 108.0) {
      azimuth = (Math.Floor(100 * azimuth)) / 100;

      if (solarZen < 90.0) {
        coszen = (Math.Floor(10000.0 * (Math.Cos(degToRad(solarZen))))) / 10000.0;
      } else {
        coszen = 0.0;
      }
    }
    double ThetaAngle = degToRad(azimuth + northAng);

    zenAng = coszen;
    azi = ThetaAngle;
    hrAngle = hourAngle;
    double PhiAngle = degToRad(elevation);
    solarElev = PhiAngle;
    eqaTime = eqTime;
    solDec = solarDec;

    double x,y,z;
    Plane BasePlane = Plane.WorldXY;
    BasePlane.Rotate(Math.PI / 2, Vector3d.ZAxis);
    x = scaleRad * Math.Cos(PhiAngle) * Math.Cos(-ThetaAngle);
    y = scaleRad * Math.Cos(PhiAngle) * Math.Sin(-ThetaAngle);
    z = scaleRad * Math.Sin(PhiAngle);

    Point3d sunPoint = BasePlane.PointAt(x, y, z);
    sunPt = sunPoint;
    Vector3d sunVector = -(new Vector3d(sunPoint));
    sunVector.Unitize();
    sunVec = sunVector;
  }

  // <Custom additional code> 
  //Basic Functions
  //-----------------------------------------
  //Convert radian angle to degrees
  public double radToDeg(double angleRad)
  {
    return (180.0 * angleRad / Math.PI);
  }
  public double degToRad(double angleDeg)
  {
    return Math.PI * angleDeg / 180.0;
  }
  //Purpose: Julian day from calendar day
  //Arguments:
  //year : 4 digit year
  //month : January = 1
  //day : 1-31
  //Return value: The Julian day corresponding to the date
  //Note: Number is returned for start of day. Fractional days should be added later.
  public double calcJD(int yr, int mth, int day)
  {
    if (mth <= 2) {
      yr = yr - 1;
      mth = mth + 12;
    }
    double A = Math.Floor(yr / 100.0);
    double B = 2 - A + Math.Floor(A / 4.0);
    double JD = Math.Floor(365.25 * (yr + 4716)) + Math.Floor(30.6001 * (mth + 1)) + day + B - 1524.5;
    return JD;
  }
  //Purpose: convert Julian Day to centuries since J2000.0
  //Arguments: jd - the Julian Day to convert
  //Return value: the T value corresponding to the Julian Day
  public double calcTimeJulianCent(double jd)
  {
    double T = (jd - 2451545.0) / 36525.0;
    return T;
  }

  //Functions to calculate Rad Vector
  //--------------------------------
  //Purpose: calculate the Geometric Mean Longitude of the Sun
  //Arguments: t - number of Julian centuries since J2000.0
  //Return value: the Geometric Mean Longitude of the Sun in degrees
  public double calcGeomMeanLongSun(double t)
  {
    double LO = 280.46646 + t * (36000.76983 + 0.0003032 * t);
    while (LO > 360.0) {
      LO -= 360.0;
    }
    while (LO < 0.0) {
      LO += 360;
    }
    return LO;
  }
  //Purpose: calculate the Geometric Mean Anomaly of the Sun
  //Arguments: t - number of Julian centuries since J2000.0
  //Return value: the Geometric Mean Anomaly of the Sun in degrees
  public double calcGeomMeanAnomalySun(double t)
  {
    double M = 357.52911 + t * (35999.05029 - 0.0001537 * t);
    return M;
  }
  //Purpose: calculate the eccentricity of earth's orbit
  //Arguments: t - number of Julian centuries since J2000.0
  //Return value: the unitless eccentricity
  public double calcEccentricityEarthOrbit(double t)
  {
    double e = 0.016708634 - t * (4.2037E-05 + 1.267E-07 * t);
    return e;
  }
  //Purpose: calculate the equation of center for the sun
  //Arguments: t : number of Julian centuries since J2000.0
  //Return value: in degrees
  public double calcSunEqOfCenter(double t)
  {
    double m = calcGeomMeanAnomalySun(t);
    double mrad = degToRad(m);
    double sinm = Math.Sin(mrad);
    double sin2m = Math.Sin(mrad + mrad);
    double sin3m = Math.Sin(mrad + mrad + mrad);

    double C = sinm * (1.914602 - t * (0.004817 + 1.4E-05 + t)) + sin2m * (0.019993 - 0.000101 * t) + sin3m * 0.000289;
    return C;
  }
  //Purpose: calculate the true longitude of the sun
  //Arguments: t : number of Julian centuries since J2000.0
  //Return value: sun's true longitude in degrees
  public double calcSunTrueLong(double t)
  {
    double lo = calcGeomMeanLongSun(t);
    double c = calcSunEqOfCenter(t);
    double O = lo + c;
    return O;
  }
  //Purpose: calculate the true anamoly of the sun
  //Arguments: t : number of Julian centuries since J2000.0
  //Return value: sun's true anamoly in degrees
  public double calcSunTrueAnomaly(double t)
  {
    double m = calcGeomMeanAnomalySun(t);
    double c = calcSunEqOfCenter(t);
    double v = m + c;
    return v;
  }
  //Purpose: calculate the disTance to the sun in AU
  //Arguments: t : number of Julian centuries since J2000.0
  //Return value: sun radius vector in AUs
  public double calcSunRadVector(double t)
  {
    double v = calcSunTrueAnomaly(t);
    double e = calcEccentricityEarthOrbit(t);
    double R = (1.000001018 * (1 - e * e)) / (1 + e * Math.Cos(degToRad(v)));
    return R;
  }

  //Functions to calculate Ascension
  //-----------------------------------------------
  //Purpose: calculate the apparent longitude of the sun
  //Arguments: t : number of Julian centuries since J2000.0
  //Return value: sun's apparent longitude in degrees
  public double calcSunApparentLong(double t)
  {
    double o = calcSunTrueLong(t);
    double omega = 125.04 - 1934.136 * t;
    double lambda = o - 0.00569 - 0.00478 * Math.Sin(degToRad(omega));
    return lambda;
  }
  //Purpose: calculate the mean obliquity of the ecliptic
  //Arguments: t : number of Julian centuries since J2000.
  //Return value: mean obliquity in degrees
  public double calcMeanObliquityOfEcliptic(double t)
  {
    double seconds = 21.448 - t * (46.815 + t * (0.00059 - t * (0.001813)));
    double eO = 23.0 + (26.0 + (seconds / 60.0)) / 60.0;
    return eO;
  }
  //Purpose: calculate the corrected obliquity of the ecliptic
  //Arguments: t : number of Julian centuries since J2000.0
  //Return value: corrected obliquity in degrees
  public double calcObliquityCorrection(double t)
  {
    double eO = calcMeanObliquityOfEcliptic(t);
    double omega = 125.04 - 1934.136 * t;
    double e = eO + 0.00256 * Math.Cos(degToRad(omega));
    return e;
  }
  //Purpose: calculate the right ascension of the sun
  //Arguments: t : number of Julian centuries since J2000.0
  //Return value: sun's right ascension in degrees
  public double calcSunRtAscension(double t)
  {
    double e = calcObliquityCorrection(t);
    double lambda = calcSunApparentLong(t);
    double Tananum = (Math.Cos(degToRad(e)) * Math.Sin(degToRad(lambda)));
    double Tanadenom = (Math.Cos(degToRad(lambda)));
    double alpha = radToDeg(Math.Atan2(Tananum, Tanadenom));
    return alpha;
  }


  //-----------------------------------------
  //Purpose: calculate the declination of the sun
  //Arguments: t : number of Julian centuries since J2000.0
  //Return value: sun's declination in degrees
  public double calcSunDeclination(double t)
  {
    double e = calcObliquityCorrection(t);
    double lambda = calcSunApparentLong(t);
    double sint = Math.Sin(degToRad(e)) * Math.Sin(degToRad(lambda));
    double theta = radToDeg(Math.Asin(sint));
    return theta;
  }


  //------------------------------------
  //Calculate the difference between true solar time and mean solar time
  //Arguments: t : number of Julian centuries since J2000.0
  //Return value: equation of time in minutes of time
  public double calcEquationOfTime(double t)
  {
    double epsilon = calcObliquityCorrection(t);
    double lo = calcGeomMeanLongSun(t);
    double e = calcEccentricityEarthOrbit(t);
    double m = calcGeomMeanAnomalySun(t);
    double y = Math.Tan(degToRad(epsilon) / 2.0);
    y = y * y;
    double sin210 = Math.Sin(2.0 * degToRad(lo));
    double sinm = Math.Sin(degToRad(m));
    double cos210 = Math.Cos(2.0 * degToRad(lo));
    double sin410 = Math.Sin(4.0 * degToRad(lo));
    double sin2m = Math.Sin(2.0 * degToRad(m));

    double Etime = y * sin210 - 2.0 * e * sinm + 4.0 * e * y * sinm * cos210 - 0.5 * y * y * sin410 - 1.25 * e * e * sin2m;
    return radToDeg(Etime) * 4.0;
  }


  //----------------------------------------
  //Return the hour angle for the given location, decl, and time of day
  public double calcHourAngle(double time, double longitude, double eqtime)
  {
    return 15.0 * (time - (longitude / 15.0) - (eqtime / 60.0));
  }

  // </Custom additional code> 
}