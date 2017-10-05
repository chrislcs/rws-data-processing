# -*- coding: utf-8 -*-
"""
Python3

Chris Lucas
"""

from io import BytesIO
import os
import zipfile
import argparse
import subprocess
import requests
from lxml import etree


def request_data(root, tile_id, output_folder):
    namespaces = {"xmlns": "http://www.w3.org/2005/Atom",
                  "xmlns:georss": "http://www.georss.org/georss"}

    try:
        tile = root.xpath('xmlns:entry[xmlns:id="{}.laz.zip"]'.format(tile_id),
                          namespaces=namespaces)[0]
    except IndexError:
        return False

    url = tile.find('xmlns:link', namespaces=namespaces).attrib['href']
    zipped_data = requests.get(url)
    data = zipfile.ZipFile(BytesIO(zipped_data.content))
    data.extractall(output_folder)
    data.close()

    return True


def request_tile(tile_id, output_folder):
    # uitgefilterd
    r = requests.get('http://geodata.nationaalgeoregister.nl/ahn2/'
                     'atom/ahn2_uitgefilterd.xml')
    root = etree.fromstring(r.content)
    request_data(root, 'u{}'.format(tile_id), output_folder)

    # gefilterd
    r = requests.get('http://geodata.nationaalgeoregister.nl/ahn2/'
                     'atom/ahn2_gefilterd.xml')
    root = etree.fromstring(r.content)
    request_data(root, 'g{}'.format(tile_id), output_folder)


def argument_parser():
    """
    Define and return the arguments.
    """
    description = "Download an AHN2 data tile."
    parser = argparse.ArgumentParser(description=description)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-t', '--tileid',
                                help='The ID of the tile to download.',
                                required=True)
    required_named.add_argument('-o', '--output',
                                help='The folder to write the data to.',
                                required=True)
    parser.add_argument('-m', '--merge',
                        help='Merge the filtered and remaining data'
                             ' (True/False). Requires PDAL.',
                        required=False,
                        default=True)
    args = parser.parse_args()
    return args


def main():
    args = argument_parser()
    request_tile(args.tileid, args.output)
    if args.merge:
        subprocess.call(['pdal', 'merge',
                         '{}/g{}.laz'.format(args.output, args.tileid),
                         '{}/u{}.laz'.format(args.output, args.tileid),
                         '{}/{}.laz'.format(args.output, args.tileid)])
        os.remove('{}/g{}.laz'.format(args.output, args.tileid))
        os.remove('{}/u{}.laz'.format(args.output, args.tileid))


if __name__ == '__main__':
    main()
