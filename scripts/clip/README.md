# LAS Clip

This python script clips a LAS/LAZ file or folder by a shapefile

## Installation

Install python3 (with osgeo library) and [PDAL](https://www.pdal.io/) (with LASzip). The easiest way to install these packages on windows is with [OSGeo4W](https://trac.osgeo.org/osgeo4w/). Choose `advanced install` and select at least the following packages: `pdal`, `laszip`, `python3-core`.

## Usage

Open a command prompt (if you are using OSGeo4W: open a OSGeo4W shell and run `py3_env.bat` located in the `bin` folder in your OSGeo4W installation folder). Run the following command:

    python las_clip.py -h

To see the help.

## Example

    python las_clip.py