import numpy as np


def blob_coloring(image):
    """Uses the blob coloring algorithm based on 8 pixel window assign region names
    takes a input:
    image: binary image
    return: a list of regions"""

    k = 1
    regions = np.zeros(image.shape)

    def use_new_tag():
        nonlocal k
        regions[i, j] = k
        k += 1

    def use_above_tag():
        regions[i, j] = regions[i - 1, j]

    def use_left_tag():
        regions[i, j] = regions[i, j - 1]

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):

            curr = image[i, j]
            prev = image[i, j - 1] if j else curr
            abov = image[i - 1, j] if i else curr

            # Left-top corner pixel
            if not i and not j:
                if curr:
                    use_new_tag()

            # Left border pixels
            if i and not j:
                if curr and abov:
                    use_above_tag()
                if curr and not abov:
                    use_new_tag()

            # Top border pixels
            if not i and j:
                if curr and prev:
                    use_left_tag()
                if curr and not prev:
                    use_new_tag()

            # Left and top pixels available
            if i and j:
                if curr and not prev and not abov:
                    use_new_tag()
                if curr and not prev and abov:
                    use_above_tag()
                if curr and prev and not abov:
                    use_left_tag()
                if curr and prev and abov:
                    # TODO: We lose information when cells are streched horizontally
                    use_above_tag()
                if regions[i, j - 1] and regions[i - 1, j] and regions[i, j - 1] != regions[i - 1, j]:
                    regions[i, j - 1] = regions[i - 1, j]
    return regions

def compute_statistics(region):
    """Compute cell statistics area and location
    takes as input
    region: a list of pixels in a region
    returns: area"""

    # Please print your region statistics to stdout
    # <region number>: <location or center>, <area>
    # print(stats)

    labels = dict()
    rows = region.shape[0]
    cols = region.shape[1]

    for i in range(rows):
        for j in range(cols):
            label = region[i, j]
            pixel = [(i, j)]
            labels[label] = labels[label] + pixel if label in labels else pixel

    stats = dict()
    for label in labels:
        area = len(labels[label])

        if area > 15:
            ranges = list(zip(*labels[label]))

            i_min, i_max = min(ranges[0]), max(ranges[0])
            j_min, j_max = min(ranges[1]), max(ranges[1])

            i_center = (i_min + i_max) / 2
            j_center = (j_min + j_max) / 2

            stat = {
                'centroid': (i_center, j_center),
                'area': area,
                'pixels': labels[label]
            }

            stats[label] = stat
            print("Region: {}, Area: {}, Centroid: {}".format(label, area, stat['centroid']))

    return stats

def mark_regions_image(image, stats):
    """Creates a new image with computed stats
    takes as input
    image: a list of pixels in a region
    stats: stats regarding location and area
    returns: image marked with center and area"""

    return image


def unit_test_blob_coloring():
    """
    Performs blob coloring on a dummy binary image.
    It prints the resulting region matrix (labels on "pixels")
    """
    bin_image = np.array([
        [0.0,   255.0,  0.0,    0.0],
        [255.0, 255.0,  0.0,    0.0],
        [255.0, 255.0,  0.0,    0.0],
        [0.0,   0.0,    0.0,    255.0],
        [0.0,   0.0,    255.0,  255.0]
    ])

    regions = blob_coloring(bin_image)

    for i in range(regions.shape[0]):
        print(regions[i, :].tolist())


if __name__ == "__main__":
    unit_test_blob_coloring()

