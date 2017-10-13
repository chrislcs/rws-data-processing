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
import xml.etree.ElementTree as etree


def request_data(root, tile_id, output_folder):
    namespaces = {"xmlns": "http://www.w3.org/2005/Atom",
                  "xmlns:georss": "http://www.georss.org/georss"}

    tile = root.find('xmlns:entry[xmlns:id="{}.laz.zip"]'.format(tile_id),
                     namespaces=namespaces)

    if tile is None:
        return False

    url = tile.find('xmlns:link', namespaces=namespaces).attrib['href']
    zipped_data = requests.get(url)
    data = zipfile.ZipFile(BytesIO(zipped_data.content))
    data.extractall(output_folder)
    data.close()

    return True


def request_tile(tile_id, output_folder, verbose=False):
    # uitgefilterd
    if verbose:
        print("Downloading filtered out AHN 2 data..")

    r = requests.get('http://geodata.nationaalgeoregister.nl/ahn2/'
                     'atom/ahn2_uitgefilterd.xml')
    root = etree.fromstring(r.content)
    success = request_data(root, 'u{}'.format(tile_id), output_folder)

    if verbose:
        if success:
            print("Download complete.")
        else:
            print("Download failed. Tile not found.")


    # gefilterd
    if verbose:
        print("Downloading filtered AHN 2 data..")

    r = requests.get('http://geodata.nationaalgeoregister.nl/ahn2/'
                     'atom/ahn2_gefilterd.xml')
    root = etree.fromstring(r.content)
    success = request_data(root, 'g{}'.format(tile_id), output_folder)

    if verbose:
        if success:
            print("Download complete.")
        else:
            print("Download failed. Tile not found.")


def argument_parser():
    """
    Define and return the arguments.
    """
    description = "Download an AHN2 data tile by tile id."
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
    parser.add_argument('-v', '--verbose',
                        help='Enable to print out the progress'
                             ' (True/False).',
                        required=False,
                        default=False)

    args = parser.parse_args()
    return args


def main():
    args = argument_parser()
    request_tile(args.tileid, args.output, args.verbose)
    if args.merge:
        if args.verbose:
            print("Merging point clouds..")

        subprocess.call(['pdal', 'merge',
                         '{}/g{}.laz'.format(args.output, args.tileid),
                         '{}/u{}.laz'.format(args.output, args.tileid),
                         '{}/{}.laz'.format(args.output, args.tileid)])

        if args.verbose:
            print("Done, removing old files..")

        os.remove('{}/g{}.laz'.format(args.output, args.tileid))
        os.remove('{}/u{}.laz'.format(args.output, args.tileid))

        if args.verbose:
            print("Done!")

if __name__ == '__main__':
    main()
