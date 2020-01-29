import attr


@attr.s(init=False)
class Surface:
    def __init__(self, screen):
        self.width = screen.width
        self.height = screen.height
        self.data = [0, 0, 0]
        self.fill(0, 0, 0)

    def fill(self, r, g, b):
        self.data = self.width * self.height * [r, g, b]

    def get_pixel(self, x, y):
        offset = 3 * (y * self.width + x)
        r = self.data[offset]
        g = self.data[offset+1]
        b = self.data[offset+2]
        return r, g, b

    def draw_gradient(self, stops):
        for y in range(self.height):
            pos = y / self.height
            lower_stop = stops[0]
            upper_stop = stops[-1]
            for stop in stops:
                if pos >= stop.pos > lower_stop.pos:
                    lower_stop = stop
                if pos < stop.pos < upper_stop.pos:
                    upper_stop = stop

            pos_diff = upper_stop.pos - lower_stop.pos
            pos_between_stops = (pos - lower_stop.pos) / pos_diff
            pos_between_stops_inverse = 1 - pos_between_stops

            r = round(lower_stop.r * pos_between_stops_inverse + upper_stop.r * pos_between_stops)
            g = round(lower_stop.g * pos_between_stops_inverse + upper_stop.g * pos_between_stops)
            b = round(lower_stop.b * pos_between_stops_inverse + upper_stop.b * pos_between_stops)

            self.draw_line(y, r, g, b)

    def draw_line(self, y, r, g, b):
        offset = 3 * y * self.width
        for x in range(self.width):
            self.data[offset + 3*x] = r
            self.data[offset + 3*x + 1] = g
            self.data[offset + 3*x + 2] = b

    def interpolate(self, other, factor):
        factor_inverse = 1 - factor
        for i in range(len(self.data)):
            self.data[i] = round(self.data[i] * factor + other.data[i] * factor_inverse)
