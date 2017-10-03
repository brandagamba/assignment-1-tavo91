import numpy as np
import cv2
from collections import Counter


def _get_sq_window(image, x, y):
    coords = []
    subimg = []
    n, m = image.shape
    sq_window = [(-1, -1), (-1, 0), (-1, 1),
                 ( 0, -1), ( 0, 0), ( 0, 1),
                 ( 1, -1), ( 1, 0), ( 1, 1)]
    for i, j in sq_window:
        xx = x + i
        yy = y + j

        ii = xx if 0 <= xx < n else 0 if xx < n else n - 1
        jj = yy if 0 <= yy < m else 0 if yy < m else m - 1

        coords.append((ii, jj))
        subimg.append(image[ii, jj] if 0 <= xx < n and 0 <= yy < m else 0.0)

    return coords, subimg

def _pick_from_candidates(regions):
    counter = Counter(regions)
    reg, count = counter.most_common(1)[0]

    # Pick the most common color
    if reg != 0.0 and count > 2:
        return reg

    # Pick the first region that comes across
    for region in regions:
        if region:
            return region
    return 0.0

def blob_coloring(image, win='8px'):
    """Uses the blob coloring algorithm based on 8 pixel window assign region names
    takes a input:
    image: binary image
    return: a list of regions"""

    if win == '3px':
        return _blob_coloring_3px(image)  # Implementation of 3 pixel window
    elif win == '8px':
        return _blob_coloring_8px(image)  # Implementation of 8 pixel window


def _blob_coloring_8px(image):
    k = 1
    regions = np.zeros(image.shape)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):

            px_curr = image[i, j]
            coords, window = _get_sq_window(image, i, j)

            # Order matters for priority
            candidates = [regions[coords[0]], regions[coords[1]], regions[coords[2]], regions[coords[3]]]
            cand_color = _pick_from_candidates(candidates)

            if cand_color and px_curr:
                for l, px in enumerate(window[:]):  # Tagging all the neighbors or just the seen ones yielded the same
                    if px:
                        regions[coords[l]] = cand_color
            elif px_curr:
                regions[i, j] = k
                k += 1

    return regions

def _blob_coloring_3px(image):
    k = 1
    regions = np.zeros(image.shape)

    def use_new_tag_if(condition):
        if condition:
            nonlocal k
            regions[i, j] = k
            k += 1

    def use_top_tag_if(condition):
        if condition:
            regions[i, j] = regions[i - 1, j]

    def use_lft_tag_if(condition):
        if condition:
            regions[i, j] = regions[i, j - 1]

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):

            curr = image[i, j]
            abov = image[i - 1, j] if i >= 0 else curr
            prev = image[i, j - 1] if j >= 0 else curr

            # Nothing to evaluate with the square window
            if not (curr or abov or prev):
                continue

            # Left-top corner pixel
            if not i and not j:
                use_new_tag_if(curr)

            # Left border pixels
            if i and not j:
                use_top_tag_if(curr and abov)
                use_new_tag_if(curr and not abov)

            # Top border pixels
            if not i and j:
                use_lft_tag_if(curr and prev)
                use_new_tag_if(curr and not prev)

            # Left and top pixels available
            if i and j:
                use_new_tag_if(curr and not prev and not abov)
                use_top_tag_if(curr and not prev and abov)
                use_lft_tag_if(curr and prev and not abov)
                use_top_tag_if(curr and prev and abov)  # TODO: We lose info when cells are streched horizontally

                lft = regions[i, j - 1]
                top = regions[i - 1, j]

                if lft and top and lft != top:
                    regions[i, j - 1] = top  # TODO: Which label is better to keep? Probably need a better window..
                    # regions[i-1, j] = lft
    return regions

def compute_statistics(region, filter=15):
    """Compute cell statistics area and location
    takes as input
    region: a list of pixels in a region
    returns: area"""

    labels = dict()
    rows = region.shape[0]
    cols = region.shape[1]

    for i in range(rows):
        for j in range(cols):
            label = region[i, j]
            if label:  # 0.0 is not a label
                pixel = [(i, j)]
                labels[label] = labels[label] + pixel if label in labels else pixel

    stats = dict()
    for label in labels:
        area = len(labels[label])

        if area > filter:
            ranges = list(zip(*labels[label]))

            i_center = int(sum(ranges[0]) / area)
            j_center = int(sum(ranges[1]) / area)

            stat = {
                'area': area,
                'centroid': (i_center, j_center)
            }

            stats[label] = stat
            print("Region: {},\tArea: {},\tCentroid: {}".format(label, area, stat['centroid']))

    return stats

def mark_regions_image(regions, stats):
    """Creates a new image with computed stats
    takes as input
    image: a list of pixels in a region
    stats: stats regarding location and area
    returns: image marked with center and area"""

    image = np.zeros(regions.shape)

    for i in range(regions.shape[0]):
        for j in range(regions.shape[1]):
            if regions[i, j] in stats:
                image[i, j] = 255

    for stat in stats.values():
        text = '*' + str(stat['area'])
        x, y = stat['centroid']
        cv2.putText(image, text, (y, x), cv2.FONT_HERSHEY_PLAIN, 0.5, 0)
    return image


def _unit_test_blob_coloring():
    """
    Performs blob coloring on a dummy binary image.
    """
    bin_image = np.array([
        [255., 255.,  0.,    255.],
        [255., 0.,    255.,    0.],
        [255., 255.,  0.,      0.],
        [0.,   0.,    0.,    255.],
        [255., 0.,    255.,  255.]
    ])

    regions = blob_coloring(bin_image)

    print("Output matrix:")
    print(regions)

    num_objects = 3

    labels = set(np.reshape(regions, (regions.shape[0] * regions.shape[1])).tolist())
    assert len(labels) - 1 == num_objects, "Test failed! The algorithm found {} object(s) but there are {}!".format(len(labels) - 1, num_objects)

    print("Test passed!")


if __name__ == "__main__":
    _unit_test_blob_coloring()

