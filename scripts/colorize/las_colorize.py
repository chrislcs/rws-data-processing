# -*- coding: utf-8 -*-
"""
Python3

@author: Chris Lucas
"""

import sys
import os
import argparse
import subprocess
import json
import math


def run_pdal(path, input_path, output_path, las_srs, wms_url,
             wms_layer, wms_srs, wms_version, wms_format, wms_ppm,
             wms_max_image_size):
    subprocess.call(['pdal', 'pipeline',
                    '{}/pdal_pipeline.json'.format(path),
                    '--readers.las.filename={}'.format(input_path),
                    '--filters.python.script={}/pdal_colorize.py'.format(path),
                    ('--filters.python.pdalargs="{' +
                    '\\\"wms_url\\\": \\\"{}\\\",'.format(wms_url) +
                    '\\\"wms_layer\\\": \\\"{}\\\",'.format(wms_layer) +
                    '\\\"wms_srs\\\": \\\"{}\\\",'.format(wms_srs) +
                    '\\\"wms_version\\\": \\\"{}\\\",'.format(wms_version) +
                    '\\\"wms_format\\\": \\\"{}\\\",'.format(wms_format) +
                    '\\\"wms_ppm\\\": \\\"{}\\\",'.format(wms_ppm) +
                    '\\\"wms_max_image_size\\\": \\\"{}\\\"}}"'.format(wms_max_image_size)),
                    '--writers.las.filename={}'.format(output_path),
                    '--writers.las.a_srs={}'.format(las_srs)])


def process_files(input_path, output_path, las_srs,
                  wms_url, wms_layer, wms_srs,
                  wms_version, wms_format, wms_ppm,
                  wms_max_image_size, verbose=False):
    """
    Run the pdal pipeline using the given arguments.

    Parameters
    ----------
    input : str
        The path to the input LAS/LAZ file.
    output : str
        The path to the output LAS/LAZ file.
    """
    path = os.path.dirname(os.path.realpath(__file__))

    if os.path.isdir(input_path):
        for i, f in enumerate(os.listdir(input_path)):
            if f.endswith(".las") or f.endswith(".laz"):
                las = os.path.join(input_path, f).replace('\\', '/')

                if os.path.isdir(output_path):
                    output_path = output_path + '/' if output_path[-1] != '/' else output_path
                    basename, ext = os.path.splitext(f)
                    out = '{}{}_color{}'.format(output_path, basename, ext)
                else:
                    basename, ext = os.path.splitext(output_path)
                    out = '{}_{}{}'.format(basename, i, ext)

                if verbose:
                    print('Colorizing {} ..'.format(las))
                run_pdal(path, las, out, las_srs, wms_url, wms_layer, wms_srs,
                         wms_version, wms_format, wms_ppm,  wms_max_image_size)
    else:
        if verbose:
            print('Colorizing {} ..'.format(input_path))
        run_pdal(path, input_path, output_path, las_srs, wms_url, wms_layer,
                 wms_srs, wms_version, wms_format, wms_ppm, wms_max_image_size)


def argument_parser():
    """
    Define and return the arguments.
    """
    description = ("Colorize a las or laz file with a WMS service. "
                   "By default uses PDOK aerial photography.")
    parser = argparse.ArgumentParser(description=description)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-i', '--input',
                                help='The input LAS/LAZ file or folder.',
                                required=True)
    required_named.add_argument('-o', '--output',
                                help='The output colorized LAS/LAZ file or folder.',
                                required=True)
    parser.add_argument('-s', '--las_srs',
                        help='The spatial reference system of the LAS data. (str, default: EPSG:28992)',
                        required=False,
                        default='EPSG:28992')
    parser.add_argument('-w', '--wms_url',
                        help='The url of the WMS service to use. (str, default: https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?)',
                        required=False,
                        default='https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?')
    parser.add_argument('-l', '--wms_layer',
                        help='The layer of the WMS service to use. (str, default: Actueel_ortho25)',
                        required=False,
                        default='Actueel_ortho25')
    parser.add_argument('-r', '--wms_srs',
                        help='The spatial reference system of the WMS data to request. (str, default: EPSG:28992)',
                        required=False,
                        default='EPSG:28992')
    parser.add_argument('-f', '--wms_format',
                        help='The image format of the WMS data to request. (str, default: image/png)',
                        required=False,
                        default='image/png')
    parser.add_argument('-v', '--wms_version',
                        help='The version number of the WMS service. (str, default: 1.3.0)',
                        required=False,
                        default='1.3.0')
    parser.add_argument('-p', '--wms_ppm',
                        help='The approximate desired pixels per meter of the requested image. (int, default: 4)',
                        required=False,
                        default=4)
    parser.add_argument('-m', '--wms_max_image_size',
                        help='The maximum size in pixels of the largest side of the requested image. (int, default: sys.maxsize)',
                        required=False,
                        default=sys.maxsize)
    parser.add_argument('-V', '--verbose', default=False, action="store_true",
                        help='Set verbose.')
    args = parser.parse_args()
    return args


def main():
    args = argument_parser()
    process_files(args.input, args.output, args.las_srs,
                  args.wms_url, args.wms_layer, args.wms_srs,
                  args.wms_version, args.wms_format,
                  args.wms_ppm, args.wms_max_image_size,
                  args.verbose)


if __name__ == '__main__':
    main()
