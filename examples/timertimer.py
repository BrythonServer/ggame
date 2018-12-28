"""
Example of using the Timer class.
"""

from ggame.timer import Timer
from ggame.mathapp import MathApp


def timercallback(t):
    """
    Callback function to receive notification of timer expiration.
    """
    print("time's up at", t.time, "seconds!")


TIMER = Timer()
# Execute timercallback after 5 seconds
TIMER.callAfter(5, timercallback)

MathApp().run()
