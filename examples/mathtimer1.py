from ggame.timer import Timer
from ggame.mathapp import MathApp

def timercallback(t):
    print("time's up!")

timer = Timer()
# Execute timercallback after 0.1 seconds
timer.callAfter(0.1, timercallback)

ma = MathApp()
ma.run()
