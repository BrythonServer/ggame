"""
ggame extensions for modeling spacecraft in planetary orbit
"""

from math import pi, degrees, radians, atan2, sin, cos, sqrt
from ggame.asset import LineStyle, Color
from ggame.mathapp import MathApp
from ggame.circle import Circle
from ggame.point import ImagePoint
from ggame.timer import Timer
from ggame.label import Label


class Planet(MathApp):
    """
    Initialize the Planet object.

    Optional keyword parameters are supported:

    :param float viewscale: Pixels per meter in graphics display. Default is 10.
    :param float radius: Radius of the planet in meters. Default is Earth radius.
    :param float planetmass: Mass of the planet in kg. Default is Earth mass.
    :param int color: Color of the planet. Default is greenish (0x008040).
    :param float viewalt: Altitude of initial viewpoint in meters. Default is rocket
      altitude.
    :param float viewanom: True anomaly (angle) of initial viewpoint in radians.
      Default is the rocket anomaly.
    :param float viewanomd: True anomaly (angle) of initial viewpoing in degrees.
      Default is the rocket anomaly.

    Example:

    .. literalinclude:: ../examples/astroplanet.py

    """

    def __init__(self, **kwargs):
        scale = kwargs.get("viewscale", 10)  # 10 pixels per meter default
        self.radius = kwargs.get("radius", 6.371e6)  # Earth - meters
        self.mass = kwargs.get("planetmass", 5.9722e24)  # Earth - kg
        self.color = kwargs.get("color", 0x008040)  # greenish
        self.viewaltitude = kwargs.get("viewalt", 0)  # how high to look
        self.viewanomaly = kwargs.get("viewanom", pi / 2)  # where to look
        self.viewanomalyd = kwargs.get("viewanomd", degrees(self.viewanomaly))
        self._planetcircle = Circle(
            (0, 0),
            self.radius,
            style=LineStyle(1, Color(self.color, 1)),
            color=Color(self.color, 0.5),
        )
        super().__init__(scale)

    def run(self, userfunc=None):
        """
        Execute the Planet (and Rocket) simulation without setting the initial view.
        """
        self.runWithRocket()

    def runWithRocket(self, rocket=None):
        """
        Execute the Planet (and Rocket) simulation.

        :Optional parameters:

        :param Rocket rocket: Reference to a Rocket object - sets the initial view
        :returns: None
        """
        if rocket:
            self.viewaltitude = rocket.altitude
            self.viewanomaly = rocket.tanomaly
        r = self.radius + self.viewaltitude
        self.view_position = (r * cos(self.viewanomaly), r * sin(self.viewanomaly))
        super().run()


class Rocket(ImagePoint):
    """
    Rocket is a class for simulating the motion of a projectile through space,
    acted upon by arbitrary forces (thrust) and by gravitaitonal
    attraction to a single planetary object.

    Required parameters:

    :param Planet planet:  Reference to a :class:`Planet` object.

    Optional keyword parameters are supported:

    :param str bitmap:  Url of a suitable bitmap image for the rocket (png
        recommended), default is `images/rocket.png`
    :param float bitmapscale:  Scale factor for bitmap. Default is 0.1
    :param float velocity:  Initial rocket speed. Default is zero.
    :param float directiond:  Initial rocket direction in degrees. Default is zero.
    :param float direction:  Initial rocket direction in radians. Default is zero.
    :param float tanomalyd:  Initial rocket true anomaly in degrees. Default is 90.
    :param float tanomaly:  Initial rocket true anomaly in radians. Default is pi/2.
    :param float altitude:  Initial rocket altitude in meters. Default is zero.
    :param bool showstatus:  Boolean displays flight parameters on screen. Default
        is True.
    :param (int, int) statuspos:  Tuple with screen x,y coordinates of flight
        parameters. Default is upper left.
    :param list[str] statuslist: List of status names to include in flight parameters.
      Default is all, consisting of: "velocity", "acceleration", "course",
      "altitude", "thrust", "mass", "trueanomaly", "scale", "timezoom",
      "shiptime"
    :param str leftkey: A :class:`ggame.event.KeyEvent` key identifier that will serve
        as the "rotate left" key while controlling the ship. Default is 'left arrow'.
    :param str rightkey: A :class:`ggame.event.KeyEvent` key identifier that will serve
        as the "rotate right" key while controlling the ship. Default is 'right arrow'.

    Following parameters may be set as a constant value, or pass in the
    name of a function that will return the value dynamically or the
    name of a `ggmath` UI control that will return the value.

    :param function or float timezoom:  Scale factor for time zoom. Factor =
        10^timezoom
    :param function or float heading:  Direction to point the rocket in (must be
        radians)
    :param fucntion or float mass: Mass of the rocket (must be kg)
    :param function or float thrust: Thrust of the rocket (must be N)

    Animation related parameters may be ignored if no sprite animation:

    :param Frame bitmapframe:  ((x1,y1),(x2,y2)) tuple defines a region in the bitmap
    :param int bitmapqty: Number of bitmaps -- used for animation effects
    :param str bitmapdir: "horizontal" or "vertical" use with animation effects. Default
        is "horizontal"
    :param int bitmapmargin: Pixels between successive animation frames
    :param float tickrate: Frequency of spacecraft dynamics calculations (Hz)

    Example:

    .. literalinclude:: ../examples/astrorocket.py

    """

    def __init__(self, planet, **kwargs):
        self._xy = (1000000, 1000000)
        self.planet = planet
        """Reference to an app object of :class:`Planet` class"""
        self._bmurl = kwargs.get("bitmap", self.getImagePath("rocket.png"))
        """URL of a bitmap image to use for the rocket"""
        self._bitmapframe = kwargs.get("bitmapframe", None)
        """:class:`ggame.asset.Frame` that specifies location of displayed
            image in bitmap image
        """
        self._bitmapqty = kwargs.get("bitmapqty", 1)
        """Number of sub-images in the bitmap image"""
        self._bitmapdir = kwargs.get("bitmapdir", "horizontal")
        """Orientation of the sub-images for animation (one of "horizontal" or
            "vertical")
        """
        self._bitmapmargin = kwargs.get("bitmapmargin", 0)
        """Margin between the sub-images for animation."""
        self.tickrate = kwargs.get("tickrate", 30)
        """Target animation frames per second."""
        # status display
        statusfuncs = [
            self._velocityText,
            self._accelerationText,
            self._courseDegreesText,
            self._altitudeText,
            self._thrustText,
            self._massText,
            self._trueAnomalyDegreesText,
            self._scaleText,
            self._timeZoomText,
            self._shipTimeText,
        ]
        statuslist = [
            "velocity",
            "acceleration",
            "course",
            "altitude",
            "thrust",
            "mass",
            "trueanomaly",
            "scale",
            "timezoom",
            "shiptime",
        ]

        self._showstatus = kwargs.get("showstatus", True)
        """Boolean: True to show stats on screen, else False."""
        self._statuspos = kwargs.get("statuspos", [10, 10])
        """Location on screen for showing the stats."""
        self._statusselect = kwargs.get("statuslist", statuslist)
        """Reference to a list of statuses to display."""
        self.localheading = 0
        """Heading (angle) of travel"""
        # dynamic parameters
        self.timezoom = self.eval(kwargs.get("timezoom", 0))
        """Reference to a function that will dynamically determine the
        time zoom factor. An integer: 1,2,3 faster, -1, slower.
        """
        self.heading = self.eval(kwargs.get("heading", self._getheading))
        """Reference to a function that will dynamically calculate spaceship
        orientation or heading (in radians)
        """
        self.mass = self.eval(kwargs.get("mass", 1))
        """Reference to a function that will dynamically calculate the
        spaceship mass (in kg).
        """
        self.thrust = self.eval(kwargs.get("thrust", 0))
        """Reference to a funtion that will dynamically calculate the rocket
        thrust (in N).
        """
        # end dynamic
        super().__init__(
            self._bmurl,
            self._getposition,
            frame=self._bitmapframe,
            qty=self._bitmapqty,
            direction=self._bitmapdir,
            margin=self._bitmapmargin,
        )
        self.scale = kwargs.get("bitmapscale", 0.1)  # small
        initvel = kwargs.get("velocity", 0)  # initial velocity
        initdird = kwargs.get("directiond", 0)  # initial direction, degrees
        initdir = kwargs.get("direction", radians(initdird))
        tanomaly = kwargs.get("tanomaly", pi / 2)  # position angle
        tanomaly = radians(kwargs.get("tanomalyd", degrees(tanomaly)))
        altitude = kwargs.get("altitude", 0)  #
        r = altitude + self.planet.radius
        self._xy = (r * cos(tanomaly), r * sin(tanomaly))
        # default heading control if none provided by user
        leftkey = kwargs.get("leftkey", "left arrow")
        rightkey = kwargs.get("rightkey", "right arrow")
        if self.heading == self._getheading:  # pylint: disable=comparison-with-callable
            Planet.listenKeyEvent("keydown", leftkey, self._turn)
            Planet.listenKeyEvent("keydown", rightkey, self._turn)
        self._timer = Timer()
        self.shiptime = 0  # track time on shipboard
        self._timer.callEvery(1 / self.tickrate, self._dynamics)
        self._lasttime = self._timer.time
        self._v_vect = [initvel * cos(initdir), initvel * sin(initdir)]
        self._a_vect = [0, 0]
        # keep track of on-screen resources
        self._labels = []
        # set up status display
        if self._showstatus:
            self.addStatusReport(statuslist, statusfuncs, self._statusselect)

    @staticmethod
    def _vadd(v1, v2):
        """
        Vector add utility.
        """
        return [v1[i] + v2[i] for i in (0, 1)]

    @staticmethod
    def _vmul(s, v):
        """
        Scalar vector multiplication utility.
        """
        return [s * v[i] for i in (0, 1)]

    @staticmethod
    def _vmag(v):
        """
        Vector magnitude function.
        """
        return sqrt(v[0] ** 2 + v[1] ** 2)

    def _turn(self, event):
        """
         Respond to left/right turning key events.
        """
        increment = pi / 50 * (1 if event.key == "left arrow" else -1)
        self.localheading += increment

    def _getposition(self):
        return self._xy

    # override or define externally!
    def _getheading(self):
        """
        User override function for dynamically determining the heading.

        :returns: float
        """
        return self.localheading

    # functions available for reporting flight parameters to UI
    def _velocityText(self):
        """
        Report the velocity in m/s as a text string.
        """
        return "Velocity:     {0:8.1f} m/s".format(self.velocity)

    def _accelerationText(self):
        """
        Report the acceleration in m/s as a text string.
        """
        return "Acceleration: {0:8.1f} m/s²".format(self.acceleration)

    def _courseDegreesText(self):
        """
        Report the heading in degrees (zero to the right) as a text string.
        """
        return "Course:       {0:8.1f}°".format(
            degrees(atan2(self._v_vect[1], self._v_vect[0]))
        )

    def _thrustText(self):
        """
        Report the thrust level in Newtons as a text string.
        """
        return "Thrust:       {0:8.1f} N".format(self.thrust())

    def _massText(self):
        """
        Report the spacecraft mass in kilograms as a text string.
        """
        return "Mass:         {0:8.1f} kg".format(self.mass())

    def _trueAnomalyDegreesText(self):
        """
        Report the true anomaly in degrees as a text string.
        """
        return "True Anomaly: {0:8.1f}°".format(self.tanomalyd)

    def _trueAnomalyRadiansText(self):
        """
        Report the true anomaly in radians as a text string.
        """
        return "True Anomaly: {0:8.4f}".format(self.tanomaly)

    def _altitudeText(self):
        """
        Report the altitude in meters as a text string.
        """
        return "Altitude:     {0:8.1f} m".format(self.altitude)

    def _radiusText(self):
        """
        Report the radius (distance to planet center) in meters as a text string.
        """
        return "Radius:       {0:8.1f} m".format(self.r)

    def _scaleText(self):
        """
        Report the view scale (pixels/meter) as a text string.
        """
        return "View Scale:   {0:8.6f} px/m".format(self.planet.scale)

    def _timeZoomText(self):
        """
        Report the time acceleration as a text string.
        """
        return "Time Zoom:    {0:8.1f}".format(float(self.timezoom()))

    def _shipTimeText(self):
        """
        Report the elapsed time as a text string.
        """
        return "Elapsed Time: {0:8.1f} s".format(float(self.shiptime))

    def _dynamics(self, timer):
        """
        Perform one iteration of the simulation using runge-kutta 4th order method.
        """
        # set time duration equal to time since last execution
        tick = 10 ** self.timezoom() * (timer.time - self._lasttime)
        self.shiptime = self.shiptime + tick
        self._lasttime = timer.time
        # 4th order runge-kutta method
        # (https://sites.temple.edu/math5061/files/2016/12/final_project.pdf)
        # and http://spiff.rit.edu/richmond/nbody/OrbitRungeKutta4.pdf  (succinct,
        # but with a typo)
        self._a_vect = k1v = self._ar(self._xy)
        k1r = self._v_vect
        k2v = self._ar(self._vadd(self._xy, self._vmul(tick / 2, k1r)))
        k2r = self._vadd(self._v_vect, self._vmul(tick / 2, k1v))
        k3v = self._ar(self._vadd(self._xy, self._vmul(tick / 2, k2r)))
        k3r = self._vadd(self._v_vect, self._vmul(tick / 2, k2v))
        k4v = self._ar(self._vadd(self._xy, self._vmul(tick, k3r)))
        k4r = self._vadd(self._v_vect, self._vmul(tick, k3v))
        self._v_vect = [
            self._v_vect[i] + tick / 6 * (k1v[i] + 2 * k2v[i] + 2 * k3v[i] + k4v[i])
            for i in (0, 1)
        ]
        self._xy = [
            self._xy[i] + tick / 6 * (k1r[i] + 2 * k2r[i] + 2 * k3r[i] + k4r[i])
            for i in (0, 1)
        ]
        if self.altitude < 0:
            self._v_vect = [0, 0]
            self._a_vect = [0, 0]
            self.altitude = 0

    # generic force as a function of position
    def _fr(self, pos):
        """
        Compute the net force vector on the rocket, as a function of the
        position vector.
        """
        self.rotation = self.heading()
        t = self.thrust()
        g = 6.674e-11
        r = Planet.distance((0, 0), pos)
        uvec = (-pos[0] / r, -pos[1] / r)
        fg = g * self.mass() * self.planet.mass / r ** 2
        vf = [x * fg for x in uvec]
        return [vf[0] + t * cos(self.rotation), vf[1] + t * sin(self.rotation)]

    # geric acceleration as a function of position
    def _ar(self, pos):
        """
        Compute the acceleration vector of the rocket, as a function of the
        position vector.
        """
        m = self.mass()
        vf = self._fr(pos)
        return [vf[i] / m for i in (0, 1)]

    # add a status reporting function to status display
    def addStatusReport(self, statuslist, statusfuncs, statusselect):
        """
        Accept list of all status names, all status text functions, and
        the list of status names that have been selected for display.

        :param list[str] statuslist: List of status names to include in flight
            parameters. Default is all, consisting of: "velocity", "acceleration",
            "course", "altitude", "thrust", "mass", "trueanomaly", "scale", "timezoom",
            and "shiptime".
        :param list[func] statusfuncs: List of function references corresponding
            to statuslist parameter.
        :param list[str] statusselect: List of names chosen from statuslist to display.

        :returns: None
        """
        statusdict = {n: f for n, f in zip(statuslist, statusfuncs)}
        for name in statusselect:
            if name in statusdict:
                self._labels.append(
                    Label(
                        self._statuspos[:],
                        statusdict[name],
                        size=15,
                        positioning="physical",
                        width=250,
                    )
                )
                self._statuspos[1] += 25

    @property
    def xyposition(self):
        """
        Report the x,y tuple for logical position of the spaceship.
        """
        return self._xy

    @xyposition.setter
    def xyposition(self, pos):
        self._xy = pos
        # self._touchAsset()

    @property
    def tanomalyd(self):
        """
        Report/set the spaceship position as a direction relative to central body
        (degrees).
        """
        return degrees(self.tanomaly)

    @tanomalyd.setter
    def tanomalyd(self, angle):
        self.tanomaly = radians(angle)

    @property
    def altitude(self):
        """
        Report/set the spaceship altitude of planet surface in meters.
        """
        alt = Planet.distance(self._xy, (0, 0)) - self.planet.radius
        return alt

    @altitude.setter
    def altitude(self, alt):
        r = alt + self.planet.radius
        self._xy = (r * cos(self.tanomaly), r * sin(self.tanomaly))

    @property
    def velocity(self):
        """
        Report the spaceship velocity scalar in m/s.
        """
        return self._vmag(self._v_vect)

    @property
    def acceleration(self):
        """
        Report the spaceship acceleration scalar in m/s.
        """
        return self._vmag(self._a_vect)

    @property
    def tanomaly(self):
        """
        Report/set the spaceship position as a direction relative to central body
        (radians).
        """
        # pos = self._pos()
        return atan2(self._xy[1], self._xy[0])

    @tanomaly.setter
    def tanomaly(self, angle):
        r = self.r
        self._xy = (r * cos(angle), r * sin(angle))
        self.touchAsset()

    @property
    def r(self):
        """
        Report the spaceship distance (radius) from central body center of mass.
        """
        return self.altitude + self.planet.radius
