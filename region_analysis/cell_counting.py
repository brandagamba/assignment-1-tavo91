import numpy as np
import cv2


def blob_coloring(image):
    """Uses the blob coloring algorithm based on 8 pixel window assign region names
    takes a input:
    image: binary image
    return: a list of regions"""

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
            if label:  # 0.0 is not a label
                pixel = [(i, j)]
                labels[label] = labels[label] + pixel if label in labels else pixel

    stats = dict()
    for label in labels:
        area = len(labels[label])

        if area > 15:
            ranges = list(zip(*labels[label]))

            i_min, i_max = min(ranges[0]), max(ranges[0])
            j_min, j_max = min(ranges[1]), max(ranges[1])

            i_center = int((i_min + i_max) / 2)
            j_center = int((j_min + j_max) / 2)

            stat = {
                'area': area,
                'centroid': (i_center, j_center),
                # 'pixels': labels[label]
            }

            stats[label] = stat
            print("Region: {}, Area: {}, Centroid: {}".format(label, area, stat['centroid']))
        # else:
        #     print("Region: {}, Area: {}, Centroid: {}".format(label, area, stat['centroid']))

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
        text = '*'  # "*{}".format(stat['area'])
        center = stat['centroid']
        cv2.putText(image, text, center, cv2.FONT_HERSHEY_SIMPLEX, 0.2, 0)

    return image


def unit_test_blob_coloring_1():
    """
    Performs blob coloring on a dummy binary image.
    It prints the resulting region matrix (labels on "pixels")
    """
    bin_image = np.array([
        [255.0, 255.0,  0.0,    0.0],
        [255.0, 0.0,    0.0,    0.0],
        [255.0, 255.0,  0.0,    0.0],
        [0.0,   0.0,    0.0,    255.0],
        [0.0,   0.0,    255.0,  255.0]
    ])

    regions = blob_coloring(bin_image)

    for i in range(regions.shape[0]):
        print(regions[i, :].tolist())

def unit_test_blob_coloring_2():
    bin_image = np.array([
        [0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	255.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0],
        [0.0,	0.0,	0.0,	0.0,	255.0,	255.0,	255.0,	255.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	0.0,	0.0,	0.0,	0.0],
        [0.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	0.0,	0.0,	0.0,	0.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	0.0,	0.0],
        [0.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	0.0],
        [255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0,	255.0]
    ])

    regions = blob_coloring(bin_image)

    for i in range(regions.shape[0]):
        print(regions[i, :].tolist())

    labels = set(np.reshape(regions, (regions.shape[0] * regions.shape[1])).tolist())
    print(labels)

if __name__ == "__main__":
    # unit_test_blob_coloring_1()
    unit_test_blob_coloring_2()

