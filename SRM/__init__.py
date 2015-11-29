import numpy

from UnionFind import UnionFind

class SRM:
    def __init__(self, image, Q=32.0):
        self._height = image.shape[0]
        self._width = image.shape[1]
        if image.ndim == 3:
            self._depth = image.shape[2]
        else:
            self._depth = 1
        
        self._n = self._width * self._height
        n = self._n
        self._image = image.reshape(n, -1)
        
        self._logdelta = 2.0 * numpy.log(6.0 * n)
        self._smallregion = int(0.001 * n)
        self._q = Q
    
    def run(self):
        self.initialization()
        self.segmentation()
        return self.finalize()
    
    def initialization(self):
        print "init"
        self._uf = UnionFind()
        uf = self._uf
        n = self._n
        height = self._height
        width = self._width
        depth = self._depth
        
        img = self._image
        self._data = numpy.empty([n, depth + 2])
        self._sizes = numpy.ones(n)
        
        for i in xrange(height):
            for j in xrange(width):
                idx = i * width + j
                uf[idx]
                self._data[idx, 0:depth] = img[idx]
                self._data[idx, depth ] = i
                self._data[idx, depth ] = j
    
    def segmentation(self):
        pairs = self.pairs()
        print "segmentation"
        
        for (r1, r2) in pairs:
            r1 = self._uf[r1]
            r2 = self._uf[r2]
            
            if r1 != r2 and self.predicate(r1, r2):
                self.merge(r1, r2)
        
        self.merge_small_regions()
    
    def pairs(self):
        print "pairs"
        pairs = []
        height = self._height
        width = self._width
        
        # using a C4-connectivity
        for i in xrange(height - 1):
            for j in xrange(width - 1):
                idx = i * width + j
                # left
                pairs.append( ( idx, i * width + j + 1) )
                
                # below
                pairs.append( ( idx, (i + 1) * width + j) )
        
        pairs = self.sort(pairs)
        return pairs
    
    def sort(self, pairs):
        print "sort"
        img = self._image
        def diff(p):
            (r1, r2) = p
            diff = numpy.max(numpy.abs(img[r1] - img[r2]))
            return diff
        return sorted(pairs, key=diff)
    
    def predicate(self, r1, r2):
        g = 256.0
        logdelta = self._logdelta
        
        w = self._sizes
        out = self._data
        
        d2 = (out[r1] - out[r2])**2
        
        log_r1 = min(g, w[r1]) * numpy.log(1.0 + w[r1])
        log_r2 = min(g, w[r2]) * numpy.log(1.0 + w[r2])
        
        q = self._q
        dev1 = g**2 / (2.0 * q * w[r1]) * (log_r1 + logdelta)
        dev2 = g**2 / (2.0 * q * w[r2]) * (log_r2 + logdelta)
        dev = dev1 + dev2
        
        return (d2 < dev).all()
    
    def merge(self, r1, r2):
        r = self._uf.union(r1, r2)
        
        s1 = self._sizes[r1]
        s2 = self._sizes[r2]
        n = s1 + s2
        self._data[r] = (s1 * self._data[r1] \
            + s2 * self._data[r2]) / n
        self._sizes[r] = n
    
    def merge_small_regions(self):
        print "small"
        
        height = self._height
        width = self._width
        smallregion = self._smallregion
        
        for i in xrange(self._height):
            for j in xrange(1, self._width):
                idx = i * width + j
                r1 = self._uf[idx]
                r2 = self._uf[idx - 1]
                
                if r1 != r2 and ( self._sizes[r1] < smallregion or self._sizes[r2] < smallregion):
                    self.merge(r1, r2)
    
    def finalize(self):
        print "finalize"
        
        height = self._height
        width = self._width
        depth = self._depth
        
        uf = self._uf
        data = self._data[:, 0:depth]
        out = numpy.empty([self._n, depth])
        for i in xrange(height):
            for j in xrange(1, width):
                idx = i * width + j
                r1 = uf[idx]
                out[idx] = data[r1]
        
        self._finalized = out.reshape(height, width, -1)
        return self._finalized
    
    def map(self):
        print "map"
        
        height = self._height
        width = self._width
        depth = self._depth
        
        classes = {}
        
        uf = self._uf
        data = self._data[:, 0:depth]
        out = numpy.empty(self._n)
        for i in xrange(height):
            for j in xrange(1, width):
                idx = i * width + j
                r1 = uf[idx]
                if r1 in classes:
                    classes[r1] += 1
                else:
                    classes[r1] = 1
                out[idx] = r1
        
        return classes, out.reshape(height, width)
    
    def exploded(self):
        print "exploded"
        
        out0 = numpy.empty([n, depth])
        out = self._data
        expl = numpy.zeros([2 * self._height, 2 * self._width, self._depth])
        
        for i in xrange(self._height):
            for j in xrange(1, self._width):
                r1 = self._uf[r]
                x = int(self._more[r1, 0])
                y = int(self._more[r1, 1])
                expl[i + x, j + y] = out[r]
        
        return expl

if __name__ == "__main__":
    import sys
    from scipy.misc import imread
    from matplotlib import pyplot
    
    q = int(sys.argv[1])
    im = imread(sys.argv[2])
    
    srm = SRM(im, q)
    
    # srm.initialization()
    # srm.segmentation()
    # classes, map = srm.map()
    # print classes
    # pyplot.imshow(map)
    # pyplot.show()
    
    segmented = srm.run()
    pyplot.imshow(segmented/256)
    pyplot.show()
    
    # exploded = srm.exploded()
    # pyplot.imshow(exploded/256)
    # pyplot.show()
    
