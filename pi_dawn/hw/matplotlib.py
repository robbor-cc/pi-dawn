import attr
import matplotlib.pyplot as plt
plt.ioff()

import numpy as np

from pi_dawn import graphics

from pi_dawn.hw.gamma import GammaCorrection
from pi_dawn.hw.differing import OrderedDiffering

@attr.s(init=False)
class LedScreen:
    width = attr.ib(type=int)
    height = attr.ib(type=int)

    def __init__(self, width, height, gamma_r=1, gamma_g=1, gamma_b=1):
        self.width = width
        self.height = height
        self.gamma_r = GammaCorrection(0.45)
        self.gamma_g = GammaCorrection(0.38)
        self.gamma_b = GammaCorrection(0.45)

        self.diff = OrderedDiffering(1)
        self.diff.build_bayer_map()

        self.display = plt.figure(figsize=(2, 8))
        self.plot = self.display.add_subplot(111)
        pixels = np.zeros(shape=[self.height, self.width, 3], dtype=int)
        self.image = self.plot.imshow(X=pixels)
        plt.draw()

    def make_surface(self):
        return graphics.Surface(self)

    def draw_surface(self, surface):
        pixels = np.ndarray(shape=[self.height, self.width, 3], dtype=int)
        for y in range(self.height):
            for x in range(self.width):
                pixels[y, x, :] = surface.get_pixel(x, y)
                pixels[y, x, :] = self.diff.correct((x, y), pixels[y, x, :])
                pixels[y, x, :] = np.clip(pixels[y, x, :], 0, 255)
                pixels[y, x, 0] = self.gamma_r.lut_correct(pixels[y, x, 0])
                pixels[y, x, 1] = self.gamma_g.lut_correct(pixels[y, x, 1])
                pixels[y, x, 2] = self.gamma_b.lut_correct(pixels[y, x, 2])

        print("average luminosity {:6.2f}".format(np.sum(pixels)/(self.height * self.width*3)))
        # self.plot.cla()
        # self.image.set_data(pixels)
        # self.image.autoscale()
        plt.imshow(pixels)
        plt.draw()
        # plt.show()
