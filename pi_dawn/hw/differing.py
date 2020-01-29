
class OrderedDiffering(object):
    def __init__(self, n):
        self.n = n
        self.map = [[0] * n] * n

    def correct(self, pos, rgb):
        if self.n is 1:
            return rgb
        x, y = pos
        u, v = x % self.n, y % self.n
        return rgb + self.map[u][v]

    @staticmethod
    def scale_bayer_map(bmap):
        n = len(bmap)
        norm = 1. / n
        off = n * 0.5
        for x in range(n):
            for y in range(n):
                bmap[y][x] = norm * bmap[y][x] - off
        return bmap

    @staticmethod
    def build_bayer_map2():
        bmap = [
            [0, 2],
            [3, 1]
        ]
        return OrderedDiffering.scale_bayer_map(bmap)

    @staticmethod
    def build_bayer_map3():
        bmap = [
            [0, 7, 3],
            [6, 5, 2],
            [4, 1, 8]
        ]
        return OrderedDiffering.scale_bayer_map(bmap)

    @staticmethod
    def build_bayer_map4():
        bmap = [
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5]
        ]
        return OrderedDiffering.scale_bayer_map(bmap)

    def build_bayer_map(self):
        if self.n is 1:
            self.map = [[1]]
        elif self.n is 2:
            self.map = self.build_bayer_map2()
        elif self.n is 3:
            self.map = self.build_bayer_map3()
        elif self.n is 4:
            self.map = self.build_bayer_map4()
        else:
            raise Exception("bayer map size is not implemented")
