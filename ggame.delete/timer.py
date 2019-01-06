"""
MathApp class for creating periodic and timed callbacks.
"""

from ggame.mathapp import MathApp, _MathDynamic


class Timer(_MathDynamic):
    """
    The Timer class instantiates an object whose basic function is to report
    the number of seconds since its creation by calling the object as a
    function with an empty argument list.

    The Timer class accepts no arguments during creation.

    Example of use:

    .. literalinclude:: ../examples/timertimer.py

    """

    def __init__(self):
        super().__init__()
        self._once = []
        self._callbacks = {}
        self._time = 0
        self.reset()
        MathApp.addDynamic(self)  # always dynamically defined

    def reset(self):
        """
        Set the reference time to the MathApp current time. If the timer is reset
        before the app initializes then do nothing.

        :returns: None
        """
        self._reset = MathApp.time

    @property
    def time(self):
        """
        Attribute is always updated with the number of seconds since the
        timer was created.
        """
        return self._time

    @time.setter
    def time(self, value):
        pass

    def step(self):
        nexttimers = []
        calllist = []
        self._time = MathApp.time - self._reset
        while self._once and self._once[0][0] <= MathApp.time:
            tickinfo = self._once.pop(0)
            if tickinfo[1]:  # periodic?
                nexttimers.append(
                    (tickinfo[1], self._callbacks[tickinfo][0])
                )  # delay, callback
            calllist.append(
                self._callbacks[tickinfo].pop(0)
            )  # remove callback and queue it
            if not self._callbacks[tickinfo]:  # if the callback list is empty
                del self._callbacks[tickinfo]  # remove the dictionary entry altogether
        for tickadd in nexttimers:
            self.callAfter(tickadd[0], tickadd[1], True)  # keep it going
        for call in calllist:
            call(self)

    def callAfter(self, delay, callback, periodic=False):
        """
        Set a callback to occur either once or periodically. The callback
        function should accept a single parameter which will be a reference
        to the timer object that called it.

        :param float delay: The number of seconds to wait before executing
            the callback function
        :param function callback: The callback function to call on timer
            expiration
        :param boolean periodic: Set True if the callback function should
            be executed periodically
        :returns: None
        """
        key = (self._time + delay, delay if periodic else 0)
        self._once.append(key)
        callbacklist = self._callbacks.get(key, [])
        callbacklist.append(callback)
        self._callbacks[key] = callbacklist
        self._once.sort()

    def callAt(self, calltime, callback):
        """
        Set a callback to occur at a specific time (seconds since
        the Timer object was created or since its
        :func:`~ggame.timer.Timer.reset` method was called.

        :param float time: The time to wait since timer creation or reset
            before calling the callback function.
        :param function callback: The callback function to call
        :returns: None
        """
        self.callAfter(calltime - self._time, callback)

    def callEvery(self, period, callback):
        """
        Set a callback to occur periodically. The callback
        function should accept a single parameter which will be a reference
        to the timer object that called it.

        :param float period: The number of seconds to wait before each
            execution of the callback function
        :param function callback: The callback function to call on timer
            expiration
        :returns: None
        """
        self.callAfter(period, callback, True)

    def __call__(self):
        return self._time
