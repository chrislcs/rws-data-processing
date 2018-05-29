# -*- coding: utf-8 -*-
"""
Python3

Chris Lucas
"""

from io import BytesIO
import sys
import os
import zipfile
import argparse
import subprocess
import requests
import xml.etree.ElementTree as etree


def request_data(root, tile_id, output_folder, verbose=False):
    namespaces = {"xmlns": "http://www.w3.org/2005/Atom",
                  "xmlns:georss": "http://www.georss.org/georss"}

    tile = root.find('xmlns:entry[xmlns:id="{}.laz.zip"]'.format(tile_id),
                     namespaces=namespaces)

    if tile is None:
        return False

    url = tile.find('xmlns:link', namespaces=namespaces).attrib['href']

    zip_file = '{}{}.laz.zip'.format(output_folder, tile_id)
    with open(zip_file, 'wb') as f:
        if not verbose:
            zipped_data = requests.get(url)
            f.write(zipped_data.content)
        else:
            zipped_data = requests.get(url, stream=True, timeout=10)
            total_length = zipped_data.headers.get('content-length')
            if total_length is not None:
                total_length = int(total_length)
            else:
                size = tile.find('xmlns:content', namespaces=namespaces).text
                size = float(size.split(':')[1].split(
                    ' ')[1].replace(',', '.'))
                total_length = int(size * 1048576)

            dl = 0
            chunk = total_length//100 if total_length is not None else 1048576
            for data in zipped_data.iter_content(chunk_size=chunk):
                f.write(data)
                dl += len(data)

                if total_length is not None:
                    done = int(100 * dl / total_length)
                    sys.stdout.write("\r[{}{}] - {}% {}/{} mb".format('=' * done,
                                                                      ' ' *
                                                                      (100 - done),
                                                                      done,
                                                                      dl/1048576,
                                                                      total_length/1048576))
                    sys.stdout.flush()
                elif verbose:
                    sys.stdout.write(
                        "\r {:0.1f} mb downloaded..".format(dl/1048576))
                    sys.stdout.flush()

            if verbose:
                sys.stdout.write("\n")

    if verbose:
        print("Download complete, unzipping..")
    with zipfile.ZipFile(zip_file) as data:
        data.extractall(output_folder)
    os.remove(zip_file)

    return True


def request_tile(tile_id, output_folder, verbose=False):
    # uitgefilterd
    if verbose:
        print("Downloading filtered out AHN 2 data..")

    r = requests.get('http://geodata.nationaalgeoregister.nl/ahn2/'
                     'atom/ahn2_uitgefilterd.xml')
    root = etree.fromstring(r.content)
    success = request_data(root, 'u{}'.format(tile_id), output_folder, verbose)

    if verbose:
        if success:
            print("Complete.")
        else:
            print("Download failed. Tile not found.")

    # gefilterd
    if verbose:
        print("Downloading filtered AHN 2 data..")

    r = requests.get('http://geodata.nationaalgeoregister.nl/ahn2/'
                     'atom/ahn2_gefilterd.xml')
    root = etree.fromstring(r.content)
    success = request_data(root, 'g{}'.format(tile_id), output_folder, verbose)

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
                        help='Merge the filtered and remaining data. '
                             'Requires PDAL.',
                        action='store_true',
                        required=False,
                        default=False)
    parser.add_argument('-v', '--verbose',
                        help='Enable to print out the progress',
                        action='store_true',
                        required=False,
                        default=False)

    args = parser.parse_args()
    return args


def main():
    args = argument_parser()
    args.output.replace('\\', '/')
    args.output = args.output + '/' if args.output[-1] != '/' else args.output
    request_tile(args.tileid, args.output, args.verbose)
    if args.merge:
        if args.verbose:
            print("Merging point clouds..")

        output_file = '{}{}.laz'.format(args.output, args.tileid)
        subprocess.call(['pdal', 'merge',
                         '{}g{}.laz'.format(args.output, args.tileid),
                         '{}u{}.laz'.format(args.output, args.tileid),
                         output_file])

        if os.path.isfile(output_file):
            if args.verbose:
                print("Done, removing old files..")

            os.remove('{}g{}.laz'.format(args.output, args.tileid))
            os.remove('{}u{}.laz'.format(args.output, args.tileid))

            if args.verbose:
                print("Done!")
        elif args.verbose:
            print("Merging failed. File not found. Keeping original files.")


if __name__ == '__main__':
    main()
