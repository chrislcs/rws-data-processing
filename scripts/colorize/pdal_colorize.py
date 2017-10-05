# -*- coding: utf-8 -*-
"""
Python3

@author: chrisl
"""

from io import BytesIO
import json
import numpy as np
import matplotlib.image as mpimg
from owslib.wms import WebMapService
from requests.exceptions import ReadTimeout


def retrieve_image(min_x, max_x, min_y, max_y,
                   wms_url, wms_layer, wms_srs,
                   wms_version, wms_format):
    """
    Download an orthophoto from the PDOK WMS service.

    Parameters
    ----------
    min_x : float
        The minimal x-coordinate of the requested image.
    max_x : float
        The maximal x-coordinate of the requested image.
    min_y : float
        The minimal y-coordinate of the requested image.
    max_y : float
        The maximal y-coordinate of the requested image.

    Returns
    -------
    out_filename : string
        The path to the output image file.

    Output
    ------
    PNG image
    """
    dif_x = max_x - min_x
    dif_y = max_y - min_y
    aspect_ratio = dif_x / float(dif_y)
    resolution = int(dif_x * 4)
    img_size = (resolution, int(resolution / aspect_ratio))

    retry = 10

    for i in range(retry):
        try:
            wms = WebMapService(wms_url, version=wms_version)
            wms_img = wms.getmap(layers=[wms_layer],
                                 srs=wms_srs,
                                 bbox=(min_x, min_y, max_x, max_y),
                                 size=img_size,
                                 format=wms_format,
                                 transparent=True)
            break
        except ReadTimeout as e:
            if i != retry-1:
                print("ReadTimeout, trying again..")
            else:
                raise e

    img = mpimg.imread(BytesIO(wms_img.read()))

    return img


def las_colorize(ins, outs):
    """
    Adds RGB information to a LAS file by downloading an orthophoto from
    the PDOK WMS service.

    Parameters
    ----------

    """
    wms = pdalargs
    if isinstance(pdalargs, str):
        wms = json.loads(pdalargs)
    X = ins['X']
    Y = ins['Y']

    xdim = [min(X), max(X)]
    ydim = [min(Y), max(Y)]

    img = retrieve_image(xdim[0], xdim[1], ydim[0], ydim[1],
                         wms['wms_url'], wms['wms_layer'],
                         wms['wms_srs'], wms['wms_version'],
                         wms['wms_format'])

    img_size = img.shape[:2]

    x_img = np.round(((X - xdim[0]) / (xdim[1]-xdim[0])) *
                     (img_size[1]-1)).astype(int)
    y_img = np.round(((ydim[1] - Y) / (ydim[1]-ydim[0])) *
                     (img_size[0]-1)).astype(int)

    rgb = img[y_img, x_img] * 255

    outs['Red'] = np.array(rgb[:, 0], dtype=np.uint16)
    outs['Green'] = np.array(rgb[:, 1], dtype=np.uint16)
    outs['Blue'] = np.array(rgb[:, 2], dtype=np.uint16)

    return True
