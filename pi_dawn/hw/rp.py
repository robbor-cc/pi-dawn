import attr

import Adafruit_WS2801
import Adafruit_GPIO.SPI

from pi_dawn import graphics

SPI_PORT = 0
SPI_DEVICE = 0


@attr.s(init=False)
class LedScreen:
    width = attr.ib(type=int)
    height = attr.ib(type=int)
    n = 4

    def __init__(self, width, height, gamma_r=2.4, gamma_g=2.4, gamma_b=2.4):
        self.width = width
        self.height = height
        self.lut_r = self.build_gamma_lut(gamma_r, self.n)
        self.lut_g = self.build_gamma_lut(gamma_g, self.n)
        self.lut_b = self.build_gamma_lut(gamma_b, self.n)
        self.bayer_map = self.build_bayer_map(self.n)
        self.pixels = Adafruit_WS2801.WS2801Pixels(width * height, spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    def make_surface(self):
        return graphics.Surface(self)

    def draw_surface(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                r, g, b = surface.get_pixel(x, y)
                r, g, b = self.lut_r[r], self.lut_g[g], self.lut_b[b]
                # spread of the bayer_map implicit set to 2
                t = self.bayer_map[y % self.n][x % self.n]
                r = max(0, min(255, round(r + t)))
                g = max(0, min(255, round(g + t)))
                b = max(0, min(255, round(b + t)))
                if x % 2 == 0:
                    offset = self.height - y - 1 + x * self.height
                else:
                    offset = y + x * self.height
                self.pixels.set_pixel_rgb(offset, r, b, g)
        self.pixels.show()

    @staticmethod
    def build_gamma_lut(gamma, n):
        max_in = 255
        max_out = 255
        return [max_out * (pow(float(i / max_in), gamma)) for i in range(max_in+1)]

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
            [3, 1],
        ]
        return LedScreen.scale_bayer_map(bmap)

    @staticmethod
    def build_bayer_map3():
        bmap = [
            [0, 7, 3],
            [6, 5, 2]
            [4, 1, 8],
        ]
        return LedScreen.scale_bayer_map(bmap)

    @staticmethod
    def build_bayer_map4():
        bmap = [
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5]
        ]
        return LedScreen.scale_bayer_map(bmap)

    @staticmethod
    def build_bayer_map(n):
        if n is 2:
            return LedScreen.build_bayer_map2()
        elif n is 3:
            return LedScreen.build_bayer_map2()
        elif n is 4:
            return LedScreen.build_bayer_map4()
        raise Exception("bayer map size is not implemented")
