import os

if os.environ.get('DEBUG', '0') == '1':
    from pi_dawn.hw.pygame import LedScreen
elif os.environ.get('DEBUG', '0') == '2':
    from pi_dawn.hw.matplotlib import LedScreen
else:
    from pi_dawn.hw.rp import LedScreen

__ALL__ = [LedScreen]
