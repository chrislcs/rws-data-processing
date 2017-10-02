# -*- coding: utf-8 -*-
"""
Python3

@author: chrisl
"""

import argparse
import subprocess


def run_pdal(input, output, divide=1):
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
    if divide == 1:
        subprocess.call(['pdal', 'pipeline', 'pdal_pipeline.json',
                         '--readers.las.filename={}'.format(input),
                         '--writers.las.filename={}'.format(output)])
    else:
        if output.find('#') == -1:
            basename, ext = os.path.splitext(output)
            output = '{}_#{}'.format(basename, ext)

        subprocess.call(['pdal', 'pipeline', 'pdal_pipeline_divide.json',
                         '--readers.las.filename={}'.format(input),
                         '--filters.divider.count={}'.format(divide),
                         '--writers.las.filename={}'.format(output)])

def argument_parser():
    """
    Define and return the arguments.
    """
    description = "Colorize an AHN las or laz file with PDOK aerial photography."
    parser = argparse.ArgumentParser(description=description)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-i', '--input',
                                help='The input LAS/LAZ file.',
                                required=True)
    required_named.add_argument('-o', '--output',
                                help='The output colorized LAS/LAZ file.',
                                required=True)
    parser.add_argument('-d', '--divide',
                        help='The number of subsets to create.',
                        required=False,
                        default=1)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = argument_parser()
    run_pdal(args.input, args.output, divide=args.divide)
