import numpy as np

from resize import interpolation as interp
from math import floor, ceil


def resize(image, fx = None, fy = None, interpolation = None):
    """calls the appropriate funciton to resample an image based on the interpolation method
    image: the image to be resampled
    fx: scale along x direction (eg. 0.5, 1.5, 2.5)
    fx: scale along y direction (eg. 0.5, 1.5, 2.5)
    interpolation: method used for interpolation ('either bilinear or nearest_neighbor)
    returns a resized image based on the interpolation method
    """

    if interpolation == 'bilinear':
        return bilinear_interpolation(image, fx, fy)

    elif interpolation == 'nearest_neighbor':
        return nearest_neighbor(image, fx, fy)

def nearest_neighbor(image, fx, fy):
    """resizes an image using nearest neighbor interpolation approximation for resampling
    image: the image to be resampled
    fx: scale along x direction (eg. 0.5, 1.5, 2.5)
    fx: scale along y direction (eg. 0.5, 1.5, 2.5)
    returns a resized image based on the nearest neighbor interpolation method
    """

    w_old, h_old = image.shape

    w_new = int(w_old * float(fx))
    h_new = int(h_old * float(fy))

    x_scale = w_new / w_old
    y_scale = h_new / h_old

    image_new = np.zeros((w_new, h_new))

    for row in range(w_new):
        for col in range(h_new):

            # i = round(row / x_scale)
            # j = round(col / y_scale)

            i = min(round(row / x_scale), w_old - 1)
            j = min(round(col / y_scale), h_old - 1)

            image_new[row, col] = image[i, j]

    return image_new


def bilinear_interpolation(image, fx, fy):
    """resizes an image using bilinear interpolation approximation for resampling
    image: the image to be resampled
    fx: scale along x direction (eg. 0.5, 1.5, 2.5)
    fx: scale along y direction (eg. 0.5, 1.5, 2.5)
    returns a resized image based on the bilinear interpolation method
    """

    w_old, h_old = image.shape

    w_new = int(w_old * float(fx))
    h_new = int(h_old * float(fy))

    x_scale = w_new / w_old
    y_scale = h_new / h_old

    image_new = np.zeros((w_new, h_new))

    for row in range(w_new):
        for col in range(h_new):

            i = row / x_scale
            j = col / y_scale

            # If it is a known point
            if not (row % x_scale) and not (col % y_scale):
                image_new[row, col] = image[int(i), int(j)]
                continue

            unk = {'x': i, 'y': j}
            p11 = {'x': min(floor(row / x_scale), w_old - 1),
                   'y': min(floor(col / y_scale), h_old - 1)}
            p12 = {'x': min(floor(row / x_scale), w_old - 1),
                   'y': min(floor(col / y_scale) + 1, h_old - 1)}
            p21 = {'x': min(floor(row / x_scale) + 1, w_old - 1),
                   'y': min(floor(col / y_scale), h_old - 1)}
            p22 = {'x': min(floor(row / x_scale) + 1, w_old - 1),
                   'y': min(floor(col / y_scale) + 1, h_old - 1)}

            p11['intensity'] = image[p11['x'], p11['y']]
            p12['intensity'] = image[p12['x'], p12['y']]
            p21['intensity'] = image[p21['x'], p21['y']]
            p22['intensity'] = image[p22['x'], p22['y']]

            image_new[row, col] = interp.bilinear_interpolation(p11, p12, p21, p22, unk)

    return image_new
