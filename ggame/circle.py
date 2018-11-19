from ggame.mathapp import MathApp, _MathVisual
from ggame.asset import CircleAsset, PolygonAsset, Color

class Circle(_MathVisual):
    
    posinputsdef = ['pos']
    nonposinputsdef = ['radius']
    defaultcolor = Color(0,0)
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **pos** center of circle
        * **radius** radius of circle (logical) or point on circle
        
        Optional Inputs
        
        * **style** border line style (thickness, color)
        * **color** fill color
        """
        """
        Radius may be scalar or point
        """
        super().__init__(CircleAsset(0, self.defaultstyle, self.defaultcolor), *args, **kwargs)
        self._touchAsset()
        self.fxcenter = self.fycenter = 0.5


    def _buildAsset(self):
        pcenter = self.spposinputs.pos
        try: 
            pradius = MathApp.distance(self.posinputs.pos(), self.nposinputs.radius()) * MathApp._scale
        except (AttributeError, TypeError):
            pradius = self.nposinputs.radius() * MathApp._scale
        style = self.stdinputs.style()
        fill = self.stdinputs.color()
        ymax = pcenter[1]+pradius
        ymin = pcenter[1]-pradius
        xmax = pcenter[0]+pradius
        xmin = pcenter[0]-pradius
        try:
            if ymin > MathApp.height or ymax < 0 or xmax < 0 or xmin > MathApp.width:
                return CircleAsset(pradius, style, fill)
            elif pradius > 2*MathApp.width:
                # here begins unpleasant hack to overcome crappy circles
                poly = self._buildPolygon(pcenter, pradius)
                if len(poly):
                    passet = PolygonAsset(poly, style, fill)
                    return passet
        except AttributeError:
            return CircleAsset(pradius, style, fill)
        return CircleAsset(pradius, style, fill)

    def _buildPolygon(self, pcenter, pradius):
        """
        pcenter is in screen relative coordinates.
        returns a coordinate list in circle relative coordinates
        """
        xcepts = [self._findIntercepts(pcenter, pradius, 0,0,0,MathApp.height),
            self._findIntercepts(pcenter, pradius, 0,0,MathApp.width,0),
            self._findIntercepts(pcenter, pradius, MathApp.width,0,MathApp.width,MathApp.height),
            self._findIntercepts(pcenter, pradius, 0,MathApp.height, MathApp.width, MathApp.height)]
        ilist = []
        for x in xcepts:
            if x and len(x) < 2:
                ilist.extend(x)
        #ilist is a list of boundary intercepts that are screen-relative
        if len(ilist) > 1:
            xrange = ilist[-1][0] - ilist[0][0]
            yrange = ilist[-1][1] - ilist[0][1]
            numpoints = 20
            inx = 0
            for i in range(numpoints):
                icepts =  self._findIntercepts(pcenter, pradius, 
                    pcenter[0], pcenter[1], 
                    ilist[0][0] + xrange*(i+1)/(numpoints+1),
                    ilist[0][1] + yrange*(i+1)/(numpoints+1))
                if len(icepts):
                    ilist.insert(inx+1, icepts[0])
                    inx = inx + 1
            self._addBoundaryVertices(ilist, pcenter, pradius)
            ilist.append(ilist[0])
            ilist = [(i[0] - pcenter[0], i[1] - pcenter[1]) for i in ilist]
        return ilist
        
    def _addBoundaryVertices(self, plist, pcenter, pradius):
        """
        Sides 0=top, 1=right, 2=bottom, 3=left
        """
        #figure out rotation in point sequence
        cw = 0
        try:
            rtst = plist[0:3]+[plist[0]]
            for p in range(3):
                cw = cw + (rtst[p+1][0]-rtst[p][0])*(rtst[p+1][1]+rtst[p][1])
        except IndexError:
            #print(plist)
            return
        cw = self._sgn(cw)
        cw = 1 if cw < 0 else 0
        vertices = ((-100,-100),
            (MathApp.width+100,-100),
            (MathApp.width+100,MathApp.height+100),
            (-100,MathApp.height+100))
        nextvertex = [(vertices[0],vertices[1]),
                        (vertices[1],vertices[2]),
                        (vertices[2],vertices[3]),
                        (vertices[3],vertices[0])]
        nextsides = [(3,1),(0,2),(1,3),(2,0)]
        edges = ((None,0),(MathApp.width,None),(None,MathApp.height),(0,None))
        endside = startside = None
        for side in range(4):
            if endside is None and (edges[side][0] == round(plist[-1][0]) or edges[side][1] == round(plist[-1][1])):
                endside = side
            if startside is None and (edges[side][0] == round(plist[0][0]) or edges[side][1] == round(plist[0][1])):
                startside = side
        iterations = 0
        while startside != endside:
            iterations = iterations + 1
            if iterations > 20:
                break
            if endside != None and startside != None:   #  and endside != startside
                plist.append(nextvertex[endside][cw])
                endside = nextsides[endside][cw]

    def _sgn(self, x):
        return 1 if x >= 0 else -1

    def _findIntercepts(self, c, r, x1, y1, x2, y2):
        """
        c (center) and x and y values are physical, screen relative.
        function returns coordinates in screen relative format
        """
        x1n = x1 - c[0]
        x2n = x2 - c[0]
        y1n = y1 - c[1]
        y2n = y2 - c[1]
        dx = x2n-x1n
        dy = y2n-y1n
        dr = sqrt(dx*dx + dy*dy)
        D = x1n*y2n - x2n*y1n
        disc = r*r*dr*dr - D*D
        dr2 = dr*dr
        if disc <= 0:  # less than two solutions
            return []
        sdisc = sqrt(disc)
        x = [(D*dy + self._sgn(dy)*dx*sdisc)/dr2 + c[0],  (D*dy - self._sgn(dy)*dx*sdisc)/dr2 + c[0]]
        y = [(-D*dx + abs(dy)*sdisc)/dr2 + c[1], (-D*dx - abs(dy)*sdisc)/dr2 + c[1]]
        getcoords = lambda x, y, c: [(x,y)] if x>=0 and x<=MathApp.width and y>=0 and y<=MathApp.height else []
        res = getcoords(x[0], y[0], c)
        res.extend(getcoords(x[1], y[1], c))
        return res


    @property
    def center(self):
        return self._center()

    @center.setter
    def center(self, val):
        newval = self.Eval(val)
        if newval != self._center:
            self._center = newval
            self._touchAsset()

    @property
    def radius(self):
        return self._radius()

    @radius.setter
    def radius(self, val):
        newval = self.Eval(val)
        if newval != self._radius:
            self._radius = newval
            self._touchAsset()
        
    def step(self):
        self._touchAsset()

    def physicalPointTouching(self, ppos):
        r = MathApp.distance(self._pcenter, ppos)
        inner = self._pradius - self.style.width/2
        outer = self._pradius + self.style.width/2
        return r <= outer and r >= inner

    def translate(self, pdisp):
        pass
