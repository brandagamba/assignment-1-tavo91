def linear_interpolation(pt1, pt2, int1, int2, unknown):
    """Computes the linear interpolation for the unknown values using pt1 and pt2
    take as input
    pt1: known point pt1 and f(pt1) or intensity value
    pt2: known point pt2 and f(pt2) or intensity value
    unknown: take an unknown location
    return the f(unknown) or intentity at unknown"""

    if pt2 - pt1 != 0:
        term1 = int1 * (pt2 - unknown) / (pt2 - pt1)
        term2 = int2 * (unknown - pt1) / (pt2 - pt1)
        return term1 + term2
    else:
        return int1


def bilinear_interpolation(pt11, pt12, pt21, pt22, unknown):
    """Computes the linear interpolation for the unknown values using pt1 and pt2
                    pt11 --*-- pt21
                           |
                           *   <---- unknown intensity
                           |
                    pt12 --*-- pt22
    take as input
    pt1: dictionary with x, y, and intensity values for point 1
    pt2: dictionary with x, y, and intensity values for point 2
    pt3: dictionary with x, y, and intensity values for point 3
    pt4: dictionary with x, y, and intensity values for point 4
    unknown: dictionary with x and y of the unknown location
    return the f(unknown) or intentity at unknown"""

    i1 = linear_interpolation(pt11['x'], pt21['x'], pt11['intensity'], pt21['intensity'], unknown['x'])
    i2 = linear_interpolation(pt12['x'], pt22['x'], pt12['intensity'], pt22['intensity'], unknown['x'])

    return linear_interpolation(pt11['y'], pt12['y'], i1, i2, unknown['y'])


def test_interpolation():
    # Testing interpolation with class example
    pt1 = {'x': 21.0, 'y': 14.0, 'intensity': 162}
    pt2 = {'x': 21.0, 'y': 15.0, 'intensity': 95}
    pt3 = {'x': 20.0, 'y': 14.0, 'intensity': 91}
    pt4 = {'x': 20.0, 'y': 15.0, 'intensity': 210}
    unk = {'x': 20.2, 'y': 14.5}

    intensity = bilinear_interpolation(pt1, pt2, pt3, pt4, unk)
    expected  = 146.1

    assert expected == round(intensity, 1)
    print("[Unit Test] Interpolation functions running properly")


if __name__ == "__main__":
    test_interpolation()
