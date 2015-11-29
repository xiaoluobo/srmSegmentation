#! /usr/bin/env python

import sys
from scipy.misc import imread
from matplotlib import pyplot
from PIL import Image
from SRM import SRM
#
# q = int(sys.argv[1])
# im = imread(sys.argv[2])
#
# srm = SRM(im, q)
# segmented = srm.run()
#
# pyplot.imshow(segmented/256)
# pyplot.show()
#
# im = imread("../skin_data/melanoma/dermIS/LMM1_orig.jpg")
im = imread("out.jpg")
# print im.size
srm = SRM(im, 256)
segmented = srm.run()


pyplot.imshow(segmented/512)
# segmented.save('srmed.jpg')
# pyplot.savefig("srmed.jpg")
pyplot.show()
segmented.save('srm.jpg')