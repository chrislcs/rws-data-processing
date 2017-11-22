# -*- coding: utf-8 -*-
"""
Python3

@author: chrisl
"""

import os
import argparse
import subprocess
import json
import math

def run_pdal(path, input_path, output_path, las_srs, wms_url,
             wms_layer, wms_srs, wms_version, wms_format, divide=1):
    if divide == 1:
        subprocess.call(['pdal', 'pipeline',
                         '{}/pdal_pipeline.json'.format(path),
                         '--readers.las.filename={}'.format(input_path),
                         '--filters.python.script={}/pdal_colorize.py'.format(path),
                         ('--filters.python.pdalargs="{' +
                          '\\\"wms_url\\\": \\\"{}\\\",'.format(wms_url) +
                          '\\\"wms_layer\\\": \\\"{}\\\",'.format(wms_layer) +
                          '\\\"wms_srs\\\": \\\"{}\\\",'.format(wms_srs) +
                          '\\\"wms_version\\\": \\\"{}\\\",'.format(wms_version) +
                          '\\\"wms_format\\\": \\\"{}\\\"}}"'.format(wms_format)),
                         '--writers.las.filename={}'.format(output_path),
                         '--writers.las.a_srs={}'.format(las_srs)])
    else:
        if output_path.find('#') == -1:
            basename, ext = os.path.splitext(output_path)
            output = '{}_#{}'.format(basename, ext)

        lasinfo = json.loads(subprocess.check_output(['pdal', 'info',
                                                      '--metadata',
                                                      input_path]))
        num_points = lasinfo['metadata']['count']
        per_divide = math.ceil(num_points / divide)

        subprocess.call(['pdal', 'pipeline',
                         '{}/pdal_pipeline_divide.json'.format(path),
                         '--readers.las.filename={}'.format(input_path),
                         '--filters.chipper.capacity={}'.format(per_divide),
                         '--filters.python.script={}/pdal_colorize.py'.format(path),
                         ('--filters.python.pdalargs="{' +
                          '\\\"wms_url\\\": \\\"{}\\\",'.format(wms_url) +
                          '\\\"wms_layer\\\": \\\"{}\\\",'.format(wms_layer) +
                          '\\\"wms_srs\\\": \\\"{}\\\",'.format(wms_srs) +
                          '\\\"wms_version\\\": \\\"{}\\\",'.format(wms_version) +
                          '\\\"wms_format\\\": \\\"{}\\\"}}"'.format(wms_format)),
                         '--writers.las.filename={}'.format(output),
                         '--writers.las.a_srs={}'.format(las_srs)])

def process_files(input_path, output_path, las_srs,
                  wms_url, wms_layer, wms_srs,
                  wms_version, wms_format,
                  divide=1):
    """
    Run the pdal pipeline using the given arguments.

    Parameters
    ----------
    input : str
        The path to the input LAS/LAZ file.
    output : str
        The path to the output LAS/LAZ file.
    divide : int
        The number of subsets to create. (optional)
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

                    run_pdal(path, las, out, las_srs, wms_url, wms_layer,
                              wms_srs, wms_version, wms_format, divide)
    else:
        run_pdal(path, input_path, output_path, las_srs, wms_url,
                  wms_layer, wms_srs, wms_version, wms_format, divide)


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
                        help='The spatial reference system of the LAS data. (Default: EPSG:28992)',
                        required=False,
                        default='EPSG:28992')
    parser.add_argument('-w', '--wms_url',
                        help='The url of the WMS service to use.',
                        required=False,
                        default='https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?')
    parser.add_argument('-l', '--wms_layer',
                        help='The layer of the WMS service to use.',
                        required=False,
                        default='2016_ortho25')
    parser.add_argument('-r', '--wms_srs',
                        help='The spatial reference system of the WMS data to request.',
                        required=False,
                        default='EPSG:28992')
    parser.add_argument('-f', '--wms_format',
                        help='The image format of the WMS data to request.',
                        required=False,
                        default='image/png')
    parser.add_argument('-v', '--wms_version',
                        help='The version number of the WMS service.',
                        required=False,
                        default='1.3.0')
    parser.add_argument('-d', '--divide',
                        help='The number of subsets to create. For LAS datasets spanning a large area this parameter can make sure the image requested from the WMS service is not too large. If the resulting point cloud is without color try increasing the amount of divides.',
                        required=False,
                        default=1)
    args = parser.parse_args()
    return args


def main():
    args = argument_parser()
    process_files(args.input, args.output, args.las_srs,
                  args.wms_url, args.wms_layer, args.wms_srs,
                  args.wms_version, args.wms_format,
                  divide=int(args.divide))


if __name__ == '__main__':
    main()
