# -*- coding: utf-8 -*-
"""
Python3

@author: chrisl
"""

import os
import argparse
import subprocess
from osgeo import ogr


def clip_las(input_path, output_path, shp_path, srs):
    input_shape = ogr.Open(shp_path)
    layer = input_shape.GetLayer()
    if len(layer) > 1:
        raise ValueError("Shapefiles containing more than 1 feature are not supported at this time")
    else:
        feature = layer.GetNextFeature()
        geometry = feature.GetGeometryRef()
        wkt = geometry.ExportToWkt()

        subprocess.call(['pdal', 'pipeline', 'pdal_pipeline.json',
                         '--readers.las.filename={}'.format(input_path),
                         '--filters.crop.polygon={}'.format(wkt),
                         '--writers.las.filename={}'.format(output_path),
                         '--writers.las.a_srs={}'.format(srs)])


def argument_parser():
    """
    Define and return the arguments.
    """
    description = ("")
    parser = argparse.ArgumentParser(description=description)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-i', '--input',
                                help='The input LAS/LAZ file or folder.',
                                required=True)
    required_named.add_argument('-o', '--output',
                                help='The output clipped LAS/LAZ file or folder.',
                                required=True)
    required_named.add_argument('-p', '--polygon',
                                help='The path to the shapefile containing the polygon to clip to.',
                                required=True)
    parser.add_argument('-s', '--las_srs',
                        help='The spatial reference system of the LAS data. (Default: EPSG:28992)',
                        required=False,
                        default='EPSG:28992')

    args = parser.parse_args()
    return args


def main():
    args = argument_parser()
    run_pdal(args.input, args.output, args.polygon, args.las_srs, args.verbose)


if __name__ == '__main__':
    main()
