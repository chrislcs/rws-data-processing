# -*- coding: utf-8 -*-
"""
Python3

@author: chrisl
"""

import os
import argparse
import subprocess
from osgeo import ogr


def call_pdal(path, las, out, srs, wkt):
    if len(wkt) > 30000:
        subprocess.call(['pdal', 'pipeline',
                         '{}/pdal_pipeline.json'.format(path),
                         '--readers.las.filename={}'.format(las),
                         '--writers.las.filename={}'.format(out),
                         '--writers.las.a_srs={}'.format(srs)])
    else:
        subprocess.call(['pdal', 'pipeline',
                         '{}/pdal_pipeline.json'.format(path),
                         '--readers.las.filename={}'.format(las),
                         '--filters.crop.polygon={}'.format(wkt),
                         '--writers.las.filename={}'.format(out),
                         '--writers.las.a_srs={}'.format(srs)])

def clip_las(input_path, output_path, shp_path, srs):
    input_path = os.path.abspath(input_path).replace('\\', '/')
    output_path = os.path.abspath(output_path).replace('\\', '/')

    input_shape = ogr.Open(shp_path)
    layer = input_shape.GetLayer()
    if len(layer) > 1:
        raise ValueError("Shapefiles containing more than 1 feature are not supported at this time")
    else:
        feature = layer.GetNextFeature()
        geometry = feature.GetGeometryRef()
        wkt = geometry.ExportToWkt()

        long_wkt = False
        if len(wkt) > 30000:
            print wkt
            print "Polygon WKT too long, please copy the WKT above manually to the pdal_pipeline.json file."
            print "Press enter to continue.."
            raw_input()

        path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

        if os.path.isdir(input_path):
            for i, f in enumerate(os.listdir(input_path)):
                if f.endswith(".las") or f.endswith(".laz"):
                    las = os.path.join(input_path, f).replace('\\', '/')

                    if os.path.isdir(output_path):
                        output_path = output_path + '/' if output_path[-1] != '/' else output_path
                        basename, ext = os.path.splitext(f)
                        out = '{}{}_clip{}'.format(output_path, basename, ext)
                    else:
                        basename, ext = os.path.splitext(output_path)
                        out = '{}_{}{}'.format(basename, i, ext)

                    call_pdal(path, las, out, srs, wkt)

        elif os.path.isdir(output_path):
            output_path = output_path + '/' if output_path[-1] != '/' else output_path
            basename, ext = os.path.splitext(os.path.basename(input_path))
            out = '{}{}_clip{}'.format(output_path, basename, ext)
            call_pdal(path, input_path, out, srs, wkt)
        else:
            call_pdal(path, input_path, output_path, srs, wkt)


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
    clip_las(args.input, args.output, args.polygon, args.las_srs)

if __name__ == '__main__':
    main()
