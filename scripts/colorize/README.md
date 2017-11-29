# LAS/LAZ Colorize

This python script adds color to a LAS/LAZ file using a WMS service (Default: PDOK 2016 aerial imagery) and the PDAL library.

## Installation

Install python3 (with numpy, matplotlib, requests and owslib libraries) and [PDAL](https://www.pdal.io/) (with LASzip). The easiest way to install these packages on windows is with [OSGeo4W](https://trac.osgeo.org/osgeo4w/). Choose `advanced install` and select at least the following packages: `pdal`, `laszip`, `python3-core`, `python3-numpy`, `python3-matplotlib`, `python3-requests`, `python3-owslib`.

## Usage

Open a command prompt (if you are using OSGeo4W: open a OSGeo4W shell and run `py3_env.bat` located in the `bin` folder in your OSGeo4W installation folder). Run the following command:

    python las_colorize.py -h

To see the help.

## Example

    python las_colorize.py -i C_25DN2.las -o C_25DN2_color.las