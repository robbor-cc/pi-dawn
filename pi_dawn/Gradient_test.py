import argparse
import sys
import time

from pi_dawn import hw
from pi_dawn import graphics


def draw(wakeup_, surface_, led_screen_, timestep_):
    wakeup_.draw(surface_, timestep_)
    led_screen_.draw_surface(surface_)

parser = argparse.ArgumentParser('test sunrise')
args = parser.parse_args(sys.argv[1:])
led_screen = hw.LedScreen(width=12, height=90, gamma_r=2.4, gamma_g=2.4, gamma_b=2.4)
surface = led_screen.make_surface()
wakeup = graphics.Sunrise(led_screen)
draw(wakeup, surface, led_screen, 0.2)

