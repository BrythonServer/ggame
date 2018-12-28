"""
These MathApp-based digital logic classes are experimental.
"""

from abc import ABCMeta, abstractmethod
from ggame.mathapp import _MathDynamic


# decorator for _getvalue or any value handler that may experience recursion
def _recursiontrap(handler):
    def trapmagic(self):
        """
        An attempt to catch recursion (doesn't work).
        """
        if not self.ingetvalue:
            self.ingetvalue = True
            self.lastget = handler(self)
            self.ingetvalue = False
            return self.lastget
        self.ingetvalue = False
        return self.lastget

    return trapmagic


class _BoolDevice(_MathDynamic, metaclass=ABCMeta):
    """
    Base class for boolean objects.

    :Required Arguments:

    :param int mininputqty: The minimum number of inputs possible.

    :Optional Keyword Arguments:

        * **namedinputs**  (*list[str]*) List of input names.
    """

    def __init__(self, mininputqty, **kwargs):
        self.inp = [None] * mininputqty
        self.enable = True
        namedinputs = kwargs.get("namedinputs", [])
        self._indict = {name: self.eval(None) for name in namedinputs}
        self.ingetvalue = False
        self.lastget = False
        self.resetval = False
        self.firsttime = True
        self._enable = None
        self._input = None
        super().__init__()

    @property
    def inp(self):
        """
        Report the list of input references.
        """
        return self._input

    @inp.setter
    def inp(self, val):
        try:
            self._input = [self.eval(v) for v in list(val)]
        except TypeError:
            self._input = [self.eval(val)]

    # Enable attribute controls the "tri-state" of output
    @property
    def enable(self):
        """
        Report the enable state of the object.
        """
        return self._enable

    @enable.setter
    def enable(self, val):
        self._enable = self.eval(val)

    @abstractmethod
    @_recursiontrap  # MUST use with any implementation that may recurse!
    def _getvalue(self):
        return None

    @staticmethod
    def _inputState(value):
        """
        interprets a value that could be single input or a list of inputs!
        """
        try:
            inputs = [].extend(value)
        except TypeError:
            inputs = [value]
        scalars = [v() for v in inputs]
        ones = scalars.count(True) + scalars.count(1)
        zeros = scalars.count(False) + scalars.count(0)
        if ones > 0 and zeros > 0:
            raise ValueError("Conflicting inputs found")
        if ones > 0:
            return True
        if zeros > 0:
            return False
        return None

    def __call__(self):
        if self.enable:
            return self._getvalue()
        return None

    def getinput(self, inputname):
        """
        Retrieve input by name.

        :param str inputname: Name to look up.
        """
        return self._inputState(self._indict[inputname])

    def setinput(self, inputname, reference):
        """
        Set an input connection.

        :param str inputname: Name to assign.
        :param function reference: Callable object or function connected to input.
        """
        self._indict[inputname] = self.eval(reference)


class _BoolOneInput(_BoolDevice):
    """
    Base class for one-input boolean objects. No required inputs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(1, *args, **kwargs)

    @abstractmethod
    @_recursiontrap  # MUST use with any implementation that may recurse!
    def _getvalue(self):
        return None


class _BoolMultiInput(_BoolDevice):
    """
    Base class for multiple-input boolean objects. No required inputs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(2, *args, **kwargs)

    @abstractmethod
    @_recursiontrap  # MUST use with any implementation that may recurse!
    def _getvalue(self):
        return None


class BoolNOT(_BoolOneInput):
    """
    Logical NOT boolean gate.
    """

    @_recursiontrap
    def _getvalue(self):
        inval = self._inputState(self.inp[0])
        if inval is None:
            return True  # equivalent to an "open" input
        return not inval


class BoolAND(_BoolMultiInput):
    """
    Logical AND boolean gate. Multiple inputs.
    """

    @_recursiontrap
    def _getvalue(self):
        for v in self._input:
            if not self._inputState(v):
                return False
        return True


class BoolNOR(_BoolMultiInput):
    """
    Logical NOR boolean gate. Multiple inputs.
    """

    @_recursiontrap
    def _getvalue(self):
        for v in self._input:
            if self._inputState(v):
                return False
        return True


class BoolNAND(_BoolMultiInput):
    """
    Logical NAND boolean gate. Multiple inputs.
    """

    @_recursiontrap
    def _getvalue(self):
        for v in self._input:
            if not self._inputState(v):
                return True
        return False


class BoolSRFF(_BoolOneInput):
    """
    Logical Set/Reset (SR) FlipFlop.

    :Optional Keyword Arguments:

    :param class gateclass: One of BoolNAND or BoolNOR (default).
    """

    def __init__(self, *args, **kwargs):
        kwargs["namedinputs"] = ["R", "S"]
        super().__init__(*args, **kwargs)
        gate = kwargs.get("gateclass", BoolNOR)
        self.ic1 = gate()
        self.ic2 = gate()

    # we can only assign IC1 and IC2 inputs when this device's inputs are set
    def setinput(self, inputname, reference):
        super().setinput(inputname, reference)
        if inputname == "R":
            self.ic1.In = reference, self.ic2
        elif inputname == "S":
            self.ic2.In = reference, self.ic1

    def _getvalue(self):
        return self.ic1()

    # pylint: disable=invalid-name
    def q_(self):
        """
        Report value of Q_ output.
        """
        return self.ic2()

    # pylint: disable=invalid-name
    def q(self):
        """
        Report value of Q output.
        """
        return self._getvalue()
