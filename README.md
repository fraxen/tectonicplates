Natural Earth in Wagner VII projection
======================
<p align="center"><img src="example_110mbasemap.png" title="Example map using the WagnerVII projection, basemap using the 110m data" alt="Example map using the WagnerVII projection, basemap using the 110m data" /></p>
For preparing global thematic maps, the *Wagner VII projection, with 10E as the central meridian* (See [here](http://www.georeference.org/doc/wagner_vii.htm) and [here](http://www.mapthematics.com/ProjectionsList.php?Projection=188) for more information) represents a good solution. The projection is *equal-area* and has a decent trade-off in shape distortion. One problem with the projection is that it is not supported in some of the common desktop GIS packages, like ArcGIS and QGis, and when it is (like Saga GIS) data sometimes gets distorted in the view/reprojection process.
By using 10E as the central meridian one avoids the problem of a far sliver of Russia being split up.
The projection definition in WKT is:

    PROJCS["Wagner VII, 10E",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS84",6378137,298.257223563]],PRIMEM["10E",10],UNIT["degree",0.0174532925199433]],PROJECTION["Wagner_VII"],PARAMETER["false_easting",0],PARAMETER["false_northing",0]]

The projection file (ArcInfo style .prj) that Global Mapper generates is:

    Projection     WAGNER VII
    Datum          WGS84
    Zunits         NO
    Units          METERS
    Xshift         0.000000
    Yshift         0.000000
    Parameters
    10 0 0.000 /* longitude of center of projection
    0.000 /* false easting (meters)
    0.000 /* false northing (meters)

Download
-----
To get access to the full database, [download the zip-archive of all the data (some 300 MB)](https://github.com/fraxen/naturalearth_wagnerVII/archive/master.zip), or clone this repo using your favorite git tool. If you are using just using the data, please ignore the 'tools' folder.

Source data - Natural Earth 2.0
-----
The data in this database is the vector datasets from the [Natural Earth dataset/collection](http://naturalearthdata.com). This collection features essential basemap data for small-scale maps, in multiple levels of detail resolutions (1:10m, 1:50m and 1:110m). The data includes coastlines, country boundaries, lakes and rivers and much more. Natural Earth is a collective effort, headed by Nathaniel Kelso and Tom Patterson, and the data has been released in the public domain.

License
----
This collection of data is placed in the public domain, under the unlicense, please refer to [LICENSE.md](LICENSE.md) for more information. Please consider giving Hugo Ahlenius, Nordpil and the Natural Earth team credit and recognition as a data source.

Notes
-----
This collection contains most of the data from Natural Earth 2.0, with the following exceptions/notes:
* The raster datasets has not yet been reprojected. This process is reasonably trivial (doesn't require much cleanup)
* The bathymetry isobaths were skipped. Could also be added fairly easily, so far it is the polygons that has caused most trouble
* Graticules for the 1:50m and 1:110m collection were skipped, used the graticules in the 1:10m folder
* The bounding box is new
* The shapefiles for map units in the ocean has a few polygons that needs to be corrected
* The gdb (ESRI ArcGIS file geodatabase) data in Natural Earth 2.0 has not bee reprojected

These have been noted as issues in this repository and might get dealt with eventually. Feel free to fork and contribute!
Also - the reprojection has been done using Global Mapper 11, there has been notes of slighly different results (offset data) when reprojection using other tools, e.g. proj4, ogr or Saga GIS. Be careful if you need to integrate data from other sources, and review any reprojection. The safest bet is to use Global Mapper when integrating this data.
The _tools_ folder in this repository contains a few files/scripts that were used in preparing the data for publishing, and can safely be ignored/skipped!

Process
-----
All the Natural Earth shapefiles were retrived from http://naturalearthdata.com on April 4, 2014 and reprojected in batch using Global Mapper 11. Further data manipulation was performed in ArcGIS 10.2.
* _Repair Geometry_ run on all datasets
* Each layer visually inspected for any inconsistencies
* Reprojection issues manually edited in ArcGIS
  * Polygons close to the 170E line
  * Polygons around Antarctica
  * Clipped to the world bounding box when needed
  * Graticules manually added in, where missing (close to the edges)

Finishing words
------
This work was performed by Hugo Ahlenius, and I am consultant specializing in GIS and cartography, you can read more about me and my services at http://nordpil.com - where you can also find some examples of thematic maps in Wagner VII projection.
I wish to extend a warm *thanks!* to the Natural Earth team for creating such a wonderful resource!
Please note anything that can be improved in the data, feel free to contribute, and just let me know if there is anything unclear.
