from ggame.timer import Timer
from ggame.mathapp import MathApp


def timercallback(t):
    print("time's up at", t.time, "seconds!")


timer = Timer()
# Execute timercallback after 5 seconds
timer.callAfter(5, timercallback)

ma = MathApp()
ma.run()
