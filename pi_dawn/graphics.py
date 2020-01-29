import attr
from pi_dawn.surface import Surface
from copy import deepcopy

@attr.s
class GradientStop:
    pos = attr.ib(type=float)
    r = attr.ib(type=int)
    g = attr.ib(type=int)
    b = attr.ib(type=int)


@attr.s
class SunriseAlarmStep:
    time = attr.ib()
    gradient = attr.ib()


@attr.s
class KeyFrame:
    time = attr.ib()
    surface = attr.ib()


@attr.s(init=False)
class Sunrise:

    steps = [
        SunriseAlarmStep(time=0.0, gradient=[
            GradientStop(0.0, -100, -100, -100),
            GradientStop(1.0,    0,    0,    0),
        ]),
        SunriseAlarmStep(time=-0.6, gradient=[
            GradientStop(0.0, -100, -100, -50),
            GradientStop(0.5,  -50,  -50,   0),
            GradientStop(1.0,    0,    0,  50),
        ]),
        SunriseAlarmStep(time=-0.2, gradient=[
            GradientStop(0.0,   0, -100, 100),
            GradientStop(1.0, 100,    10, 50),
        ]),
        SunriseAlarmStep(time=0.2, gradient=[
            GradientStop(0.0,  -50, 100, 255),
            GradientStop(0.5,  150,  50,  80),
            GradientStop(1.0,  100,  100,   0),
        ]),
        SunriseAlarmStep(time=0.4, gradient=[
            GradientStop(0.0, 135, 191, 255),
            GradientStop(0.5, 255, 255, 0),
            GradientStop(1.0, 255, 255, 204),
        ]),
         SunriseAlarmStep(time=0.6, gradient=[
            GradientStop(0.0, 255, 255, 102),
            GradientStop(1.0, 255, 255, 204),
        ]),
        SunriseAlarmStep(time=0.8, gradient=[
            GradientStop(0.0, 255, 255, 204),
            GradientStop(1.0, 255, 255, 204),
        ]),
        SunriseAlarmStep(time=1.00, gradient=[
            GradientStop(0.0, 255, 255, 255),
            GradientStop(1.0, 255, 255, 255),
        ]),
    ]

    def __init__(self, led_screen):
        steps = len(self.steps)-1
        start = 0
        end = 1.0
        step = (end-start)/steps
        for i in range(steps):
            self.steps[i].time = start + i*step


        self.steps.insert(0, deepcopy(self.steps[0]))
        self.steps.append(deepcopy(self.steps[-1]))
        self.steps[0].time = -2.
        self.steps[-1].time = +2.

        self.key_frames = []

        for step in self.steps:
            surface = led_screen.make_surface()
            surface.draw_gradient(step.gradient)
            self.key_frames.append(KeyFrame(step.time, surface))

    def draw(self, surface: Surface, time: float):
        lower_key_frame = self.key_frames[0]
        upper_key_frame = self.key_frames[-1]
        for key_frame in self.key_frames:
            if time >= key_frame.time > lower_key_frame.time:
                lower_key_frame = key_frame
            if time < key_frame.time < upper_key_frame.time:
                upper_key_frame = key_frame
        time_between_key_frames = (time - lower_key_frame.time) / (upper_key_frame.time - lower_key_frame.time)
        surface.data = lower_key_frame.surface.data[:]
        surface.interpolate(upper_key_frame.surface, 1-time_between_key_frames)
