import argparse
import sys
import time

import matplotlib.pyplot as plt
plt.ioff()

from pi_dawn import hw
from pi_dawn import graphics

from matplotlib.animation import FuncAnimation

steps = 100

def main():
    parser = argparse.ArgumentParser('test sunrise')
    args = parser.parse_args(sys.argv[1:])
    led_screen = hw.LedScreen(width=10, height=32, gamma_r=2.4, gamma_g=2.4, gamma_b=2.4)
    surface = led_screen.make_surface()
    wakeup = graphics.Sunrise(led_screen)

    # def draw(event):
    #     for step in range(0, steps + 1, 5):
    #         timestep = step / steps
    #         print(step, timestep)
    #         wakeup.draw(surface, timestep)
    #         led_screen.draw_surface(surface)
    #         time.sleep(1)
    #
    # plt.connect('button_press_event', draw)

    for step in range(0, steps+1, 1):
        timestep = step / steps
        print(step, timestep)
        wakeup.draw(surface, timestep)
        led_screen.draw_surface(surface)
        time.sleep(10/steps)
    plt.show()
    print("awake")

if __name__ == "__main__":
    main()
