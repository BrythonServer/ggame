from time import time
from ggame.mathapp import MathApp, _MathDynamic

class Timer(_MathDynamic):
    
    def __init__(self):
        super().__init__()
        self.once = []
        self.callbacks = {}
        self.time = 0
        self._reset = None
        MathApp._addDynamic(self)  # always dynamically defined
        
    def reset(self):
        """
        Set the reference time to the MathApp current time. If the timer is reset
        before the app initializes then do nothing.
        
        :returns: None
        """
        if self._reset:
            self._reset = MathApp.time

    def step(self):
        nexttimers = []
        calllist = []
        if not self._reset:
            self._reset = MathApp.time
        self.time = MathApp.time - self._reset
        while self.once and self.once[0][0] <= MathApp.time:
            tickinfo = self.once.pop(0)
            if tickinfo[1]:  # periodic?
                nexttimers.append((tickinfo[1], self.callbacks[tickinfo][0]))  # delay, callback
            calllist.append(self.callbacks[tickinfo].pop(0)) # remove callback and queue it
            if not self.callbacks[tickinfo]: # if the callback list is empty
                del self.callbacks[tickinfo] # remove the dictionary entry altogether
        for tickadd in nexttimers:
            self.callAfter(tickadd[0], tickadd[1], True)  # keep it going
        for call in calllist:
            call(self)

    def callAfter(self, delay, callback, periodic=False):
        key = (MathApp.time + delay, delay if periodic else 0)
        self.once.append(key)
        callbacklist = self.callbacks.get(key, [])
        callbacklist.append(callback)
        self.callbacks[key] = callbacklist
        self.once.sort()
        
    def callAt(self, time, callback):
        self.callAfter(time-self.time, callback)
        
    def callEvery(self, period, callback):
        self.callAfter(period, callback, True)

    def __call__(self):
        return self.time

