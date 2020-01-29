
class GammaCorrection(object):
    def __init__(self, gamma, max_in=255, max_out=255):
        self.max_in = max_in
        self.max_out = max_out
        self.lut = self.build_gamma_lut(gamma, self.max_in, self.max_out)

    def lut_correct(self, value):
        return self.lut[int(value)]

    @staticmethod
    def calc_correct(value, gamma=0.4, max_in=255, max_out=255):
        return max_out * (pow(float(value / max_in), gamma))

    @staticmethod
    def build_gamma_lut(gamma, max_in=255, max_out=255):
        return [GammaCorrection.calc_correct(i, gamma, max_in, max_out) for i in range(max_in + 1)]
