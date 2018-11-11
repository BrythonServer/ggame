# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Frame, Color, LineStyle, LineAsset, CircleAsset, Sprite, App
from ggame import TextAsset, ImageAsset, PolygonAsset, RectangleAsset
from abc import ABCMeta, abstractmethod
from operator import add
from collections import namedtuple

from math import sin, cos, sqrt, pi
from time import time



class _MathDynamic(metaclass=ABCMeta):
    
    def __init__(self):
        self._dynamic = False  # not switched on, by default!
    
    def destroy(self):
        MathApp._removeDynamic(self)

    def step(self):
        pass
    
    def Eval(self, val):
        if callable(val):
            self._setDynamic() # dynamically defined .. must step
            return val
        else:
            return lambda : val  
            
    def _setDynamic(self):
        MathApp._addDynamic(self)
        self._dynamic = True
            

class _MathVisual(Sprite, _MathDynamic, metaclass=ABCMeta):
    
    posinputsdef = []  # a list of names (string) of required positional inputs
    nonposinputsdef = []  # a list of names (string) of required non positional inputs
    defaultsize = 15
    defaultwidth = 200
    defaultcolor = Color(0, 1)
    defaultstyle = LineStyle(1, Color(0, 1))
    
    
    def __init__(self, asset, *args, **kwargs):
        """
        Required inputs
        
        * **asset** a ggame asset
        * **args** the list of required positional and nonpositional arguments,
          as named in the posinputsdef and nonposinputsdef lists
        * **kwargs** all other optional keyword arguments:
          positioning - logical (default) or physical, size, width, color, style
          movable
        
        """
        
        MathApp._addVisual(self)
        #Sprite.__init__(self, asset, args[0])
        _MathDynamic.__init__(self)
        self._movable = False
        self._selectable = False
        self._strokable = False
        self.selected = False
        self.mouseisdown = False
        # 
        self.positioning = kwargs.get('positioning', 'logical')
        # positional inputs
        self.PI = namedtuple('PI', self.posinputsdef)
        # nonpositional inputs
        self.NPI = namedtuple('NPI', self.nonposinputsdef)
        # standard inputs (not positional)
        standardargs = ['size','width','color','style']
        self.SI = namedtuple('SI', standardargs)
        # correct number of args?
        if len(args) != len(self.posinputsdef) + len(self.nonposinputsdef):
            raise TypeError("Incorrect number of parameters provided")
        self.args = args
        # generated named tuple of functions from positional inputs
        self.posinputs = self.PI(*[self.Eval(p) for p in args][:len(self.posinputsdef)])
        self._getPhysicalInputs()
        # first positional argument must be a sprite position!
        Sprite.__init__(self, asset, self.pposinputs[0])
        # generated named tuple of functions from nonpositional inputs
        if len(self.nonposinputsdef) > 0:
            self.nposinputs = self.NPI(*[self.Eval(p) for p in args][(-1*len(self.nonposinputsdef)):])
        else:
            self.nposinputs = []
        self.stdinputs = self.SI(self.Eval(kwargs.get('size', self.defaultsize)),
                                    self.Eval(kwargs.get('width', self.defaultwidth)),
                                    self.Eval(kwargs.get('color', self.defaultcolor)),
                                    self.Eval(kwargs.get('style', self.defaultstyle)))
        self.sposinputs = self.PI(*[0]*len(self.posinputs))
        self.spposinputs = self.PI(*self.pposinputs)
        self.snposinputs = self.NPI(*[0]*len(self.nposinputs))
        self.sstdinputs = self.SI(*[0]*len(self.stdinputs))

    def step(self):
        self._touchAsset()
        
    def _saveInputs(self, inputs):
        self.sposinputs, self.spposinputs, self.snposinputs, self.sstdinputs = inputs
        
    def _getInputs(self):
        self._getPhysicalInputs()
        return (self.PI(*[p() for p in self.posinputs]),
            self.PI(*self.pposinputs),
            self.NPI(*[p() for p in self.nposinputs]),
            self.SI(*[p() for p in self.stdinputs]))

    
    def _getPhysicalInputs(self):
        """
        Translate all positional inputs to physical
        """
        pplist = []
        if self.positioning == 'logical':
            for p in self.posinputs:
                pval = p()
                try:
                    pp = MathApp.logicalToPhysical(pval)
                except AttributeError:
                    pp = MathApp._scale * pval
                pplist.append(pp)
        else:
            # already physical
            pplist = [p() for p in self.posinputs]
        self.pposinputs = self.PI(*pplist)
    
    def _inputsChanged(self, saved):
        return self.spposinputs != saved[1] or self.snposinputs != saved[2] or self.sstdinputs != saved[3]

    
    def destroy(self):
        MathApp._removeVisual(self)
        MathApp._removeMovable(self)
        MathApp._removeStrokable(self)
        _MathDynamic.destroy(self)
        Sprite.destroy(self)

    def _updateAsset(self, asset):
        if type(asset) != ImageAsset:
            visible = self.GFX.visible
            if App._win != None:
                App._win.remove(self.GFX)
                self.GFX.destroy()
            self.asset = asset
            self.GFX = self.asset.GFX
            self.GFX.visible = visible        
            if App._win != None:
                App._win.add(self.GFX)
        self.position = self.pposinputs.pos
            
    @property
    def movable(self):
        return self._movable
        
    @movable.setter
    def movable(self, val):
        if not self._dynamic:
            self._movable = val
            if val:
                MathApp._addMovable(self)
            else:
                MathApp._removeMovable(self)

    @property
    def selectable(self):
        return self._selectable
        
    @selectable.setter
    def selectable(self, val):
        self._selectable = val
        if val:
            MathApp._addSelectable(self)
        else:
            MathApp._removeSelectable(self)

    @property
    def strokable(self):
        return self._strokable
        
    @strokable.setter
    def strokable(self, val):
        self._strokable = val
        if val:
            MathApp._addStrokable(self)
        else:
            MathApp._removeStrokable(self)

    def select(self):
        self.selected = True


    def unselect(self):
        self.selected = False
        
    def mousedown(self):
        self.mouseisdown = True
        
    def mouseup(self):
        self.mouseisdown = False

    def processEvent(self, event):
        pass

    # define how your class responds to mouse clicks - returns True/False
    @abstractmethod
    def physicalPointTouching(self, ppos):
        pass
    
    # define how your class responds to being moved (physical units)
    @abstractmethod
    def translate(self, pdisp):
        pass
    
    # define how your class responds to being stroked (physical units)
    def stroke(self, ppos, pdisp):
        pass
    
    # is the mousedown in a place that will result in a stroke?
    def canstroke(self, ppos):
        return False
    
    def _touchAsset(self, force = False):
        inputs = self._getInputs()
        changed = self._inputsChanged(inputs)
        if changed:
            self._saveInputs(inputs)
        if changed or force:
            self._updateAsset(self._buildAsset())

    
    @abstractmethod
    def _buildAsset(self):
        pass
    

class Label(_MathVisual):
    
    posinputsdef = ['pos']
    nonposinputsdef = ['text']
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **pos** position of label
        * **text** text contents of label
        """
        super().__init__(TextAsset(""), *args, **kwargs)
        self._touchAsset()

    def _buildAsset(self):
        return TextAsset(self.nposinputs.text(), 
                            style="{0}px Courier".format(self.stdinputs.size()),
                            width=self.stdinputs.width(),
                            fill=self.stdinputs.color())

    def __call__(self):
        return self.nposinputs.text()

    def physicalPointTouching(self, ppos):
        _ppos = self.spposinputs.pos
        return (ppos[0] >= _ppos[0] and 
            ppos[0] <= _ppos[0] + self.sstdinputs.width and
            ppos[1] >= _ppos[1] and 
            ppos[1] <= _ppos[1] + self.sstdinputs.size)

    def translate(self, pdisp):
        pass


class InputNumeric(Label):
    
    def __init__(self, pos, val, **kwargs):
        """
        Required Inputs
        
        * **pos** position of button
        * **val** initial value of input
        
        Optional Keyword Input
        * **fmt** a Python format string (default is {0.2})
        """
        self._fmt = kwargs.get('fmt', '{0.2}')
        self._val = self.Eval(val)()  # initialize to simple numeric
        self._savedval = self._val
        self._updateText()
        super().__init__(pos, self._textValue, **kwargs)
        self.selectable = True
        
    def _textValue(self):
        return self._text()

    def _updateText(self):
        self._text = self.Eval(self._fmt.format(self._val))

    def processEvent(self, event):
        if event.key in "0123456789insertdelete":
            key = event.key
            if event.key == 'insert':
                key = '-'
            elif event.key == 'delete':
                key = '.'
            if self._text() == "0":
                self._text = self.Eval("")
            self._text = self.Eval(self._text() + key)
            self._touchAsset()
        elif event.key in ['enter','escape']:
            if event.key == 'enter':
                try:
                    self._val = float(self._text())
                except ValueError:
                    self._val = self._savedval
                self._savedval = self._val
            self.unselect()
            

    def select(self):
        super().select()
        self._savedval = self._val
        self._val = 0
        self._updateText()
        self._touchAsset()
        MathApp.listenKeyEvent("keypress", "*", self.processEvent)

    def unselect(self):
        super().unselect()
        self._val = self._savedval
        self._updateText()
        self._touchAsset()
        try:
            MathApp.unlistenKeyEvent("keypress", "*", self.processEvent)
        except ValueError:
            pass

    def __call__(self):
        return self._val


class InputButton(Label):
    
    def __init__(self, callback, *args,  **kwargs):
        """
        Required Inputs
        
        * **pos** position of button
        * **text** text of button
        * **callback** reference of a function to execute, passing this button object
        """
        super().__init__(*args, **kwargs)
        self._touchAsset()
        self._callback = callback
        self.selectable = True

    def _buildAsset(self):
        return TextAsset(self.nposinputs.text(), 
                            style="bold {0}px Courier".format(self.stdinputs.size()),
                            width=self.stdinputs.width(),
                            fill=self.stdinputs.color())

    def select(self):
        super().select()
        if self._callback: self._callback(self)
        self.unselect()

    def unselect(self):
        super().unselect()


        
class _Point(_MathVisual, metaclass=ABCMeta):

    posinputsdef = ['pos']
    nonposinputsdef = []

    def __init__(self, asset, *args, **kwargs):
        """
        Required Inputs
        
        * **asset** asset object to use
        * **pos** position of point
        """
        super().__init__(asset, *args, **kwargs)
        self._touchAsset()
        self.center = (0.5, 0.5)

    def __call__(self):
        return self.posinputs.pos()

    def step(self):
        pass  # FIXME
        self._touchAsset()

    def physicalPointTouching(self, ppos):
        return MathApp.distance(ppos, self.pposinputs.pos) < self.sstdinputs.size
        
    def translate(self, pdisp):
        ldisp = MathApp.translatePhysicalToLogical(pdisp)
        pos = self.posinputs.pos()
        self.posinputs = self.posinputs._replace(pos=self.Eval((pos[0] + ldisp[0], pos[1] + ldisp[1])))
        self._touchAsset()
        
    def distanceTo(self, otherpoint):
        try:
            pos = self.posinputs.pos
            opos = otherpoint.posinputs.pos
            return MathApp.distance(pos, opos())
        except AttributeError:
            return otherpoint  # presumably a scalar - use this distance




class Point(_Point):


    defaultsize = 5
    defaultstyle = LineStyle(0, Color(0, 1))


    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **pos** position of point
        """
        super().__init__(CircleAsset(self.defaultsize, 
            self.defaultstyle, self.defaultcolor), *args, **kwargs)


    def _buildAsset(self):
        return CircleAsset(self.stdinputs.size(),
                            self.stdinputs.style(),
                            self.stdinputs.color())



class ImagePoint(_Point):


    def __init__(self, url, *args, **kwargs):
        """
        Required Inputs
        
        * **url** location of image file
        * **pos** position of point
        
        Optional Inputs
        * **frame** sub-frame location of image within file
        * **qty** number of sub-frames, when used as sprite sheet
        * **direction** one of 'horizontal' (default) or 'vertical'
        * **margin** pixels between sub-frames if sprite sheet
        """
        frame = kwargs.get('frame', None)
        qty = kwargs.get('qty', 1)
        direction = kwargs.get('direction', 'horizontal')
        margin = kwargs.get('margin', 0)
        self._imageasset = ImageAsset(url, frame, qty, direction, margin)
        super().__init__(self._imageasset, *args, **kwargs)


    def _buildAsset(self):
        return self._imageasset

    def physicalPointTouching(self, ppos):
        self._setExtents()  # ensure xmin, xmax are correct
        x, y = ppos
        return x >= self.xmin and x < self.xmax and y >= self.ymin and y <= self.ymax


class InputImageButton(ImagePoint):
    
    def __init__(self, url, callback, *args, **kwargs):
        """
        Required Inputs
        
        * **url** location of image file
        * **callback** reference of a function to execute, passing this button object
        * **pos** position of point
        
        Optional Inputs
        * **frame** sub-frame location of image within file
        * **qty** number of sub-frames, when used as sprite sheet
        * **direction** one of 'horizontal' (default) or 'vertical'
        * **margin** pixels between sub-frames if sprite sheet
        """
        super().__init__(url, *args, **kwargs)
        self.center = (0,0)
        self._callback = callback
        self.selectable = True
        self.firstImage()
        self.mousewasdown = self.mouseisdown

    def select(self):
        super().select()
        if self._callback: self._callback(self)
        self.unselect()

    def unselect(self):
        super().unselect()

    def __call__(self):
        # code for controlling the button image state only works if the
        # button state is being monitored!
        if self.mouseisdown != self.mousewasdown:
            if self.mouseisdown:
                self.nextImage()
            else:
                self.firstImage()
            self.mousewasdown = self.mouseisdown
        return self.mouseisdown
        

class InputImageToggle(ImagePoint):

    def __init__(self, url, statelist, initindex, *args, **kwargs):
        """
        Required Inputs
        
        * **url** location of image file
        * **statelist** list of values to correspond with toggle states
        * **initindex** index to initial toggle state
        * **pos** position of point
        
        Optional Inputs
        * **frame** sub-frame location of image within file
        * **direction** for sprite sheet one of 'horizontal' (default) or 'vertical'
        * **margin** pixels between sub-frames if sprite sheet
        * Note the qty of images is equal to length of the statelist
        """
        self.statelist = statelist
        kwargs.setdefault('qty', len(statelist))
        super().__init__(url, *args, **kwargs)
        self.center = (0,0)
        self.selectable = True
        self.togglestate = initindex
        self.setImage(self.togglestate)

    def select(self):
        super().select()
        self.togglestate += 1
        if self.togglestate == len(self.statelist):
            self.togglestate = 0
        self.setImage(self.togglestate)
        self.unselect()

    def __call__(self):
        return self.statelist[self.togglestate]
    
    
class MetalToggle(InputImageToggle):
    def __init__(self, initindex, *args, **kwargs):
        """
        Required Inputs
        
        * **initindex** index to initial toggle state
        * **pos** position of toggle
        """
        kwargs.setdefault('frame', Frame(0,0,110,150))
        super().__init__("toggle-up-down.png", [True, False], initindex, *args, **kwargs)
        self.scale = 0.4
        


class GlassButton(InputImageButton):
    
    def __init__(self, callback, *args, **kwargs):
        """
        Required Inputs
        
        * **callback** reference of a function to execute, passing this button object
        * **pos** position of point
        """        
        kwargs.setdefault('frame', Frame(0,0,100,100))
        kwargs.setdefault('qty', 2)
        super().__init__("button-round.png", callback, *args, **kwargs)
        self.scale = 0.3
        
        


class ImageIndicator(_MathVisual):

    posinputsdef = ['pos']
    nonposinputsdef = ['value']

    def __init__(self, url, *args, **kwargs):
        """
        Required Inputs
        
        * **url** location of image file consisting of two image sprite sheet
        * **pos** position of point
        * **value** state of the indicator (True/False or integer)

        Optional Inputs
        * **frame** sub-frame location of image within file
        * **qty** number of sub-frames, when used as sprite sheet
        * **direction** one of 'horizontal' (default) or 'vertical'
        * **margin** pixels between sub-frames if sprite sheet
        """
        kwargs.setdefault('frame', None)
        kwargs.setdefault('qty', 1)
        kwargs.setdefault('direction', 'horizontal')
        kwargs.setdefault('margin', 0)
        super().__init__(
            ImageAsset(url, 
                kwargs['frame'], 
                kwargs['qty'], 
                kwargs['direction'], 
                kwargs['margin']), 
            *args, **kwargs)
        self.center = (0,0)

    def _buildAsset(self):
        inval = self.nposinputs.value()
        if inval == True:
            self.setImage(1)
        elif inval == False:
            self.setImage(0)
        else:
            self.setImage(inval)
        return self.asset

    def physicalPointTouching(self, ppos):
        self._setExtents()  # ensure xmin, xmax are correct
        x, y = ppos
        return x >= self.xmin and x < self.xmax and y >= self.ymin and y <= self.ymax

    def translate(self, pdisp):
        pass


class LEDIndicator(ImageIndicator):
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **pos** position of point
        * **value** state of the indicator (True/False or integer)

        """
        kwargs.setdefault('frame', Frame(0,0,600,600))
        kwargs.setdefault('qty', 2)
        super().__init__("red-led-off-on.png", *args, **kwargs)
        self.scale = 0.05


class LineSegment(_MathVisual):
    
    posinputsdef = ['pos','end']
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **pos** start position of segment
        * **end** end position of segment
        
        Optional Inputs
        
        * **style** line style (thickness, color)
        """
        super().__init__(LineAsset(0,0, self.defaultstyle), *args, **kwargs)
        self._touchAsset()
        
    def _buildAsset(self):
        start = self.pposinputs.pos
        end = self.pposinputs.end
        self.position = start
        return LineAsset(end[0]-start[0],
                            end[1]-start[1],
                            self.stdinputs.style())

    def physicalPointTouching(self, ppos):
        return False

    def translate(self, pdisp):
        pass



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





class Slider(_MathVisual):
    
    posinputsdef = ['pos']
    nonposinputsdef = ['minval','maxval','initial']

    def __init__(self, *args, **kwargs):
        super().__init__(
            RectangleAsset(1, 1), *args, **kwargs)
        self._val = self.nposinputs.initial()
        self._steps = kwargs.get('steps', 50)
        self._step = (self.nposinputs.maxval()-self.nposinputs.minval())/self._steps
        self._leftctrl = kwargs.get('leftkey', None)
        self._rightctrl = kwargs.get('rightkey', None)
        self._centerctrl = kwargs.get('centerkey', None)
        self.selectable = True  # must be after super init!
        self.strokable = True  # this enables grabbing/slideing the thumb
        self.thumbcaptured = False
        self._thumbwidth = max(self.stdinputs.width()/40, 1)
        self.thumb = Sprite(RectangleAsset(self._thumbwidth, 
            self.stdinputs.size()-2, LineStyle(1, self.stdinputs.color()), self.stdinputs.color()), 
            self.thumbXY())
        self._touchAsset()
        if self._leftctrl:
            MathApp.listenKeyEvent("keydown", self._leftctrl, self.moveLeft)
        if self._rightctrl:
            MathApp.listenKeyEvent("keydown", self._rightctrl, self.moveRight)
        if self._centerctrl:
            MathApp.listenKeyEvent("keydown", self._centerctrl, self.moveCenter)

    def thumbXY(self):
        minval = self.nposinputs.minval()
        maxval = self.nposinputs.maxval()
        return (self.spposinputs.pos[0]+(self._val-minval)*
                (self.sstdinputs.width-self._thumbwidth)/(maxval-minval),
                self.spposinputs.pos[1]+1)
            
    def __call__(self):
        return self._val

    @property
    def value(self):
        return self._val
        
    @value.setter
    def value(self, val):
        self._setval(val)

    def _buildAsset(self):
        self.setThumb()
        return RectangleAsset(
            self.stdinputs.width(), self.stdinputs.size(), 
            line=self.stdinputs.style(), fill=Color(0,0))

    def setThumb(self):
        self.thumb.position = self.thumbXY()
                
    def step(self):
        pass
    
    def _setval(self, val):
        minval = self.nposinputs.minval()
        maxval = self.nposinputs.maxval()
        if val <= minval:
            self._val = minval
        elif val >= maxval:
            self._val = maxval
        else:
            self._val = round((val - minval)*self._steps/(maxval-minval))*self._step + minval
        self.setThumb()
        
    def increment(self, step):
        self._setval(self._val + step)
        
    def select(self):
        super().select()
        if not self._leftctrl:
            MathApp.listenKeyEvent("keydown", "left arrow", self.moveLeft)
        if not self._rightctrl:
            MathApp.listenKeyEvent("keydown", "right arrow", self.moveRight)
        MathApp.listenMouseEvent("click", self.mouseClick)

    def unselect(self):
        super().unselect()
        try:
            if not self._leftctrl:
                MathApp.unlistenKeyEvent("keydown", "left arrow", self.moveLeft)
            if not self._rightctrl:
                MathApp.unlistenKeyEvent("keydown", "right arrow", self.moveRight)
            MathApp.unlistenMouseEvent("click", self.mouseClick)
        except ValueError:
            pass

    def mouseClick(self, event):
        if self.physicalPointTouching((event.x, event.y)):
            if event.x > self.thumb.x + self._thumbwidth:
                self.moveRight(event)
            elif event.x < self.thumb.x:
                self.moveLeft(event)
                
    def moveLeft(self, event):
        self.increment(-self._step)

    def moveRight(self, event):
        self.increment(self._step)
        
    def moveCenter(self, event):
        self._val = (self.snposinputs.minval + self.snposinputs.maxval)/2
        self.setThumb()
        
    def canstroke(self, ppos):
        return self.physicalPointTouchingThumb(ppos)
        
    def stroke(self, ppos, pdisp):
        _ppos = self.spposinputs.pos
        minval = self.snposinputs.minval
        maxval = self.snposinputs.maxval
        xpos = ppos[0] + pdisp[0]
        self.value = (xpos - _ppos[0])*(maxval-minval)/self.sstdinputs.width + minval

    def physicalPointTouching(self, ppos):
        _ppos = self.spposinputs.pos
        return (ppos[0] >= _ppos[0] and 
            ppos[0] <= _ppos[0] + self.sstdinputs.width and
            ppos[1] >= _ppos[1] and 
            ppos[1] <= _ppos[1] + self.sstdinputs.size)

    def physicalPointTouchingThumb(self, ppos):
        thumbpos = self.thumbXY()
        return (ppos[0] >= thumbpos[0] and 
            ppos[0] <= thumbpos[0] + self._thumbwidth + 2 and
            ppos[1] >= thumbpos[1] and 
            ppos[1] <= thumbpos[1] + self.sstdinputs.size - 2)

    def translate(self, pdisp):
        pass

    
class Timer(_MathDynamic):
    
    def __init__(self):
        super().__init__()
        self.once = []
        self.callbacks = {}
        self.reset()
        self.step()
        self._start = self._reset  #first time
        self.next = None
        MathApp._addDynamic(self)  # always dynamically defined
        
    def reset(self):
        self._reset = MathApp.time
        
    def step(self):
        nexttimers = []
        calllist = []
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


class Bunny():
    
    """Bunny class is similar to turtle. Needs refinement.
    
    Example use:
    
        b = Bunny()
        b.PenDown()
        for i in range(100):
            b.Right(1.5)
            b.Move(i/25)

    """
    
    def __init__ (self):
        self.GoTo(0,0)
        self.Color(0)
        self.PenUp() 
        self.SetAngle(0)

    def PenUp(self):
        self.down = False

    def PenDown(self):
        self.down = True
        
    def Color(self, color):
        self.color = Color(color,1)
        
    def GoTo(self, x, y):
        self.pos = (x,y)
        
    def SetAngle(self, a):
        self.angle = a
        
    def Right(self, da):
        self.angle = self.angle - da
        
    def Left(self, da):
        self.angle = self.angle + da
        
    def Move(self, d):
        next = (self.pos[0] + d*cos(self.angle), self.pos[1] + d*sin(self.angle))
        LineSegment(Point(self.pos, 0), Point(next, 0), LineStyle(1, self.color))
        self.pos = next

    #def physicalPointTouching(self, ppos):
    #    return MathApp.distance(ppos, self._ppos) < self._size
        
    #def translate(self, pdisp):
    #    ldisp = MathApp.translatePhysicalToLogical(pdisp)
    #    pos = self._pos()
    #    self._pos = self.Eval((pos[0] + ldisp[0], pos[1] + ldisp[1]))
    #    self._touchAsset()


class MathApp(App):
    
    _scale = 200   # pixels per unit
    _xcenter = 0    # center of screen in units
    _ycenter = 0    
    _mathVisualList = [] #
    _mathDynamicList = []
    _mathMovableList = []
    _mathSelectableList = []
    _mathStrokableList = []
    _viewNotificationList = []
    time = time()
    
    def __init__(self, scale=_scale):
        super().__init__()
        MathApp.width = self.width
        MathApp.height = self.height
        MathApp._scale = scale   # pixels per unit
        # register event callbacks
        self.listenMouseEvent("click", self.handleMouseClick)
        self.listenMouseEvent("mousedown", self.handleMouseDown)
        self.listenMouseEvent("mouseup", self.handleMouseUp)
        self.listenMouseEvent("mousemove", self.handleMouseMove)
        self.listenMouseEvent("wheel", self.handleMouseWheel)
        self.mouseDown = False
        self.mouseCapturedObject = None
        self.mouseStrokedObject = None
        self.mouseDownObject = None
        self.mouseX = self.mouseY = None
        self._touchAllVisuals()
        self.selectedObj = None
        MathApp.time = time()

    def step(self):
        MathApp.time = time()
        for spr in self._mathDynamicList:
            spr.step()

    def _touchAllVisuals(self):
        # touch all visual object assets to use scaling
        for obj in self._mathVisualList:
            obj._touchAsset(True)


    @classmethod
    def logicalToPhysical(cls, lp):
        xxform = lambda xvalue, xscale, xcenter, physwidth: int((xvalue-xcenter)*xscale + physwidth/2)
        yxform = lambda yvalue, yscale, ycenter, physheight: int(physheight/2 - (yvalue-ycenter)*yscale)

        try:
            return (xxform(lp[0], cls._scale, cls._xcenter, cls._win.width),
                yxform(lp[1], cls._scale, cls._ycenter, cls._win.height))
        except AttributeError:
            return lp
            
    @classmethod
    def physicalToLogical(cls, pp):
        xxform = lambda xvalue, xscale, xcenter, physwidth: (xvalue - physwidth/2)/xscale + xcenter
        yxform = lambda yvalue, yscale, ycenter, physheight: (physheight/2 - yvalue)/yscale + ycenter

        try:
            return (xxform(pp[0], cls._scale, cls._xcenter, cls._win.width),
                yxform(pp[1], cls._scale, cls._ycenter, cls._win.height))
        except AttributeError:
            return pp
            
    @classmethod
    def translatePhysicalToLogical(cls, pp):
        xxform = lambda xvalue, xscale: xvalue/xscale
        yxform = lambda yvalue, yscale: -yvalue/yscale

        try:
            return (xxform(pp[0], cls._scale), yxform(pp[1], cls._scale))
        except AttributeError:
            return pp

    @classmethod
    def translateLogicalToPhysical(cls, pp):
        xxform = lambda xvalue, xscale: xvalue*xscale
        yxform = lambda yvalue, yscale: -yvalue*yscale

        try:
            return (xxform(pp[0], cls._scale), yxform(pp[1], cls._scale))
        except AttributeError:
            return pp

    def handleMouseClick(self, event):
        found = False
        for obj in self._mathSelectableList:
            if obj.physicalPointTouching((event.x, event.y)):
                found = True
                if not obj.selected: 
                    obj.select()
                    self.selectedObj = obj
        if not found and self.selectedObj:
            self.selectedObj.unselect()
            self.selectedObj = None

    def handleMouseDown(self, event):
        self.mouseDown = True
        self.mouseCapturedObject = None
        self.mouseStrokedObject = None
        for obj in self._mathSelectableList:
            if obj.physicalPointTouching((event.x, event.y)):
                obj.mousedown()
                self.mouseDownObject = obj
                break
        for obj in self._mathMovableList:
            if obj.physicalPointTouching((event.x, event.y)) and not (obj.strokable and obj.canstroke((event.x,event.y))):
                self.mouseCapturedObject = obj
                break
        if not self.mouseCapturedObject:
            for obj in self._mathStrokableList:
                if obj.canstroke((event.x, event.y)):
                    self.mouseStrokedObject = obj
                    break

    def handleMouseUp(self, event):
        if self.mouseDownObject:
            self.mouseDownObject.mouseup()
            self.mouseDownObject = None
        self.mouseDown = False
        self.mouseCapturedObject = None
        self.mouseStrokedObject = None

    def handleMouseMove(self, event):
        if not self.mouseX:
            self.mouseX = event.x
            self.mouseY = event.y
        dx = event.x - self.mouseX
        dy = event.y - self.mouseY
        self.mouseX = event.x
        self.mouseY = event.y
        if self.mouseDown:
            if self.mouseCapturedObject:
                self.mouseCapturedObject.translate((dx, dy))
            elif self.mouseStrokedObject:
                self.mouseStrokedObject.stroke((self.mouseX,self.mouseY), (dx,dy))
            else:
                lmove = self.translatePhysicalToLogical((dx, dy))
                MathApp._xcenter -= lmove[0]
                MathApp._ycenter -= lmove[1]
                self._touchAllVisuals()
                self._viewNotify("translate")
    
    @property
    def viewPosition(self):
        return (MathApp._xcenter, MathApp._ycenter)
        
    @viewPosition.setter
    def viewPosition(self, pos):
        MathApp._xcenter, MathApp._ycenter = pos
        self._touchAllVisuals()
        self._viewNotify("translate")
        
    def handleMouseWheel(self, event):
        zoomfactor = event.wheelDelta/100
        zoomfactor = 1+zoomfactor if zoomfactor > 0 else 1+zoomfactor
        if zoomfactor > 1.2:
            zoomfactor = 1.2
        elif zoomfactor < 0.8:
            zoomfactor = 0.8
        MathApp._scale *= zoomfactor
        self._touchAllVisuals()
        self._viewNotify("zoom")
        
    @classmethod   
    def addViewNotification(cls, handler):
        cls._viewNotificationList.append(handler)
        
    @classmethod   
    def removeViewNotification(cls, handler):
        cls._viewNotificationList.remove(handler)
    
    def _viewNotify(self, viewchange):
        for handler in self._viewNotificationList:
            handler(viewchange = viewchange, scale = self._scale, center = (self._xcenter, self._ycenter))
        
     
    @classmethod   
    def distance(cls, pos1, pos2):
        return sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)
        
    @property
    def scale(self):
        return self._scale
        
    @property
    def width(cls):
        return App._win.width
            
    @classmethod
    def _addVisual(cls, obj):
        """ FIX ME """
        if isinstance(obj, _MathVisual):
            cls._mathVisualList.append(obj)
            
    @classmethod
    def _removeVisual(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathVisualList:
            cls._mathVisualList.remove(obj)

    @classmethod
    def _addDynamic(cls, obj):
        if isinstance(obj, _MathDynamic) and not obj in cls._mathDynamicList:
            cls._mathDynamicList.append(obj)
            
    @classmethod
    def _removeDynamic(cls, obj):
        if isinstance(obj, _MathDynamic) and obj in cls._mathDynamicList:
            cls._mathDynamicList.remove(obj)

    @classmethod
    def _addMovable(cls, obj):
        if isinstance(obj, _MathVisual) and not obj in cls._mathMovableList:
            cls._mathMovableList.append(obj)
            
    @classmethod
    def _removeMovable(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathMovableList:
            cls._mathMovableList.remove(obj)

    @classmethod
    def _addSelectable(cls, obj):
        if isinstance(obj, _MathVisual) and not obj in cls._mathSelectableList:
            cls._mathSelectableList.append(obj)
            
    @classmethod
    def _removeSelectable(cls, obj):
       if isinstance(obj, _MathVisual)  and obj in cls._mathSelectableList:
            cls._mathSelectableList.remove(obj)

    @classmethod
    def _addStrokable(cls, obj):
        if isinstance(obj, _MathVisual) and not obj in cls._mathStrokableList:
            cls._mathStrokableList.append(obj)
            
    @classmethod
    def _removeStrokable(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathStrokableList:
            cls._mathStrokableList.remove(obj)

    @classmethod
    def _destroy(cls, *args):
        """
        This will clean up any class level storage.
        """ 
        App._destroy(*args)  # hit the App class first
        MathApp._mathVisualList = [] 
        MathApp._mathDynamicList = []
        MathApp._mathMovableList = []
        MathApp._mathSelectableList = []
        MathApp._mathStrokableList = []
        MathApp._viewNotificationList = []
        



# test code here
if __name__ == "__main__":
    
    
    """
    
    index = 0
    coordlist = [(1,1), (2,1), (2,0), (1,2), (1,1)]
    
    def nextcoord():
        global index
        if index == len(coordlist):
            index = 0
        retval = coordlist[index]
        index = index + 1
        return retval
        
    def one(t):
        print("one")
        
    def two(t):
        print("two")
        
    def three(t):
        t.callAt(10, ten)
        print("three")
    
    def ten(t):
        print("ten")
        
    def tick(t):
        print("tick")
        
    #pm1 = PointMass((0.1,0))
    
    def rotate(timer):
        ip1.rotation += 0.01
    



    #p1 = Point((0,0))
    #p1.movable = True
    #c1 = Circle(p1, 1.5, LineStyle(3, Color(0x0000ff,1)), Color(0x0000ff,0.3))
    
    #s1 = Slider((200, 400), 0, 10, 2, positioning='physical',
    #    leftkey="a", rightkey="d", centerkey="s")
    
    #p2 = Point((2,0))
    #p2.movable = True
    #p3 = Point((3,0))

    #t = Timer()
    #p4 = Point(lambda :(3, (int(t.time*100) % 400)/100))
    
    #p5 = Point(lambda :nextcoord())

    #ip1 = ImagePoint((0.1,0), 'bunny.png')


    
    #LineSegment(p1,p4)

    #l1 = Label((-4,2), lambda: "Elapsed Time: {0:.0}".format(t.time), size=20, width=400, positioning="logical")
    #i1 = InputNumeric((200,300), 99.9, size=20, positioning="physical")
    #l2 = Label((-4,1), lambda: "{0}".format(i1()), size=20)
    #l3 = Label((-4,1), lambda: "{0:4.2f}".format(s1()), size=20)
    #b1 = InputButton((200,350), "RESET", lambda: t.reset(), size=20, positioning="physical")
    
    
    #t.callAfter(1, one)
    #t.callAfter(2, two)
    #t.callAfter(3, three)
    #t.callAt(10, ten)
    #t.callEvery(1, tick)
    #t.callEvery(0.1, rotate)

    def step(t):
        global vx, vy, x, y
        fx = 0
        fy = mass * g
        ax = thrust()*cos(sat.rotation)
        ay = fy / mass + thrust()*sin(sat.rotation)
        x = x + vx * tick + 0.5 * ax * tick**2
        y = y + vy * tick + 0.5 * ay * tick**2
        vx = vx + ax*tick
        vy = vy + ay*tick
        
        if y < 0:
            y = 0
            vy = 0
            
        vslider.value = vy
        

    def velocitytext():
        return "Velocity: ({0:2.4},{1:2.4})".format(vx,vy)

    def getposition():
        return (x,y)
    
            
    def turnleft(event):
        sat.rotation += 0.01
        
    def turnright(event):
        sat.rotation -= 0.01

    tick = 0.02
    x = 0
    y = 100
    vx = vy = 0
    mass = 1
    g = -9.81
    
    sat = Rocket(getposition)
    sat.rotation = pi/2
    sat.scale = 0.1
    MathApp.listenKeyEvent('keydown', 'left arrow', turnleft)
    MathApp.listenKeyEvent('keydown', 'right arrow', turnright)

    thrust = Slider((100, 100), -50, 50, 0, positioning='physical', steps=200,
        leftkey="down arrow", rightkey="up arrow", centerkey="space")
    vslider = Slider((100, 125), -50, 50, 0, positioning='physical')
    Label((100,150), velocitytext, size=15, positioning="physical")
    #westp = Point((-100000,0))
    #eastp = Point((100000,0))
    #ground = LineSegment(westp, eastp)


    
    #MathApp.addViewNotification(zoomCheck)
    """


    def step(timer):
        print(id(timer))

    def labelcoords():
        return (100 + vslider1(), 175)
        
    def buttoncoords():
        return (300 + vslider1(), 175)
        
    def labelcolor():
        colorval =   vslider1()
        return Color(colorval*256,1)

    def pressbutton(caller):
        print("button pressed: ", caller)

    vslider1 = Slider((100, 150), 0, 250, 125, positioning='physical', steps=10)

    def buttonstatus():
        return "True" if imgbutton() else "False"

    imgbutton = InputImageButton("button-round.png", pressbutton, (0,0), frame=Frame(0,0,100,100), qty=2)
    imgbutton.scale = 0.5

    label = Label(labelcoords, buttonstatus, size=15, positioning="physical", color=labelcolor)
    button = InputButton(pressbutton, buttoncoords, "Press Me", size=15, positioning="physical")
    numinput = InputNumeric((300, 275), 3.14, positioning="physical")

    ip = ImagePoint( 'bunny.png', (0,0))
    ip.movable = True

    p1 = Point((0,0), color=Color(0x008000, 1))
    p1.movable = True
    
    p2 = Point((0,-1))
    
    p3 = Point((1.2,0))
    

    LineSegment(p2,p3, style=LineStyle(3, Color(0,1)))
    LineSegment(p2,p1, style=LineStyle(3, Color(0,1)))
    
    c2 = Circle((-1,-1), p1)
    
    ii = ImageIndicator("red-led-off-on.png", (300,500), imgbutton, positioning="physical", frame=Frame(0,0,600,600), qty=2)
    ii.scale = 0.1
   
    glassbutton = GlassButton(None, (0,-0.5))
    toggle = MetalToggle(0, (0, -1))
    
   
    Li = LEDIndicator((300,450), glassbutton, positioning="physical")
    Lit = LEDIndicator((300,480), toggle, positioning="physical")
   
    def zoomCheck(**kwargs):
        viewtype = kwargs.get('viewchange')
        scale = kwargs.get('scale')
        print(ap.scale)
    
    #pcenter = Point((0, -5000000))
    # c1 = Circle((0,-5000000), 5000000, LineStyle(1, Color(0x008040,1)), Color(0x008400,0.5))


    ap = MathApp()

    #ap.addViewNotification(zoomCheck)
    ap.run()
    
    
    """
    """
    
