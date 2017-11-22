# AHN2 Downloader

Downloads AHN2 data using a tile id.

## Installation

Install python3 (with requests module)

## Usage

Open a command prompt. Run the following command:

    python3 ahn2_downloader.py -h

To see the help.

To get the tile id of a tile use the [AHN2 WFS service by PDOK](https://www.pdok.nl/nl/service/wfs-actueel-hoogtebestand-nederland-ahn2)

## Example

    python3 ahn2_downloader.py -t 25bz2 -o ../../data/25bz2/
