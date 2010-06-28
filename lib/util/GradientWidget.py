# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class GradientWidget(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        
        self.gradRect = QtGui.QGraphicsRectItem(QtCore.QRectF(0, -10, 100, 10))
        self.gradient = QtGui.QLinearGradient(QtCore.QPointF(0,0), QtCore.QPointF(100,0))
        self.gradient.setColorAt(0, QtGui.QColor(0,0,0))
        self.gradient.setColorAt(1, QtGui.QColor(255,0,0))
        self.gradRect.setBrush(QtGui.QBrush(self.gradient))
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.scene.addItem(self.gradRect)
        
        self.ticks = []
        self.addTick(0, QtGui.QColor(0,0,0), True)
        self.addTick(1, QtGui.QColor(255,0,0), True)
        self.setMaximumHeight(40)
        self.setFrameStyle(QtGui.QFrame.NoFrame | QtGui.QFrame.Plain)
        self.setBackgroundRole(QtGui.QPalette.NoRole)
     
        
    def addTick(self, x, c=None, e=False):
        if c is None:
            c = self.getColor(x)
        tick = Tick(self, [x*100, 0], c, e)
        self.ticks.append(tick)
        self.scene.addItem(tick)
        #tick.connect(QtCore.SIGNAL('tickChanged'), self.tickChanged)
        
    def tickChanged(self, tick=None, delete=False):
        #print "tick changed"
        if delete:
            #tick.disconnect(QtCore.SIGNAL('tickChanged'), self.tickChanged)
            self.ticks.remove(tick)
            self.scene.removeItem(tick)
        self.ticks.sort(lambda a,b: cmp(a.pos().x(), b.pos().x()))
        self.gradient = self.getGradient()
        self.gradRect.setBrush(QtGui.QBrush(self.gradient))
        self.emit(QtCore.SIGNAL('gradientChanged'), self)
        
    def resizeEvent(self, ev):
        self.fitInView(QtCore.QRectF(-6, -17, 112, 17), QtCore.Qt.KeepAspectRatio)
        
    def mousePressEvent(self, ev):
        QtGui.QGraphicsView.mousePressEvent(self, ev)
        if ev.button() == QtCore.Qt.LeftButton and len(self.items(ev.pos())) < 1:
            self.ignoreRelease = False
        else:
            self.ignoreRelease = True
        
    def mouseReleaseEvent(self, ev):
        #QtGui.QGraphicsView.mouseReleaseEvent(self, ev)
        if not self.ignoreRelease:  #ev.button() == QtCore.Qt.LeftButton and len(self.items(ev.pos())) < 1:
            pos = self.mapToScene(ev.pos())
            if pos.x() < 0 or pos.x() > 100:
                return
            pos.setX(min(max(pos.x(), 0), 100))
            self.addTick(pos.x()/100.)
            self.tickChanged()
        QtGui.QGraphicsView.mouseReleaseEvent(self, ev)
        
    def getGradient(self):
        g = QtGui.QLinearGradient(QtCore.QPointF(0,0), QtCore.QPointF(100,0))
        
        g.setStops([(t.x(), QtGui.QColor(t.color)) for t in self.ticks])
        return g
        
    def getColor(self, x):
        if x <= 0:
            return QtGui.QColor(self.ticks[0].color)  # always copy colors before handing them out
        if x >= 1:
            return QtGui.QColor(self.ticks[-1].color)
            
        x2 = self.ticks[0].x()
        for i in range(1,len(self.ticks)):
            x1 = x2
            x2 = self.ticks[i].x()
            if x1 <= x and x2 >= x:
                dx = (x2-x1)
                if dx == 0:
                    f = 0.
                else:
                    f = (x-x1) / dx
                c1 = self.ticks[i-1].color
                c2 = self.ticks[i].color
                r = c1.red() * (1.-f) + c2.red() * f
                g = c1.green() * (1.-f) + c2.green() * f
                b = c1.blue() * (1.-f) + c2.blue() * f
                return QtGui.QColor(r, g, b)
                
                
            
        
## Multiple inheritance not allowed in PyQt. Retarded workaround:
#class QObjectWorkaround:
    #def __init__(self):
        #self._qObj_ = QtCore.QObject()
    #def connect(self, *args):
        #return QtCore.QObject.connect(self._qObj_, *args)
    #def disconnect(self, *args):
        #return QtCore.QObject.disconnect(self._qObj_, *args)
    #def emit(self, *args):
        #return QtCore.QObject.emit(self._qObj_, *args)
        
        
class Tick(QtGui.QGraphicsPolygonItem):
    def __init__(self, view, pos, color, endTick=False, scale=7):
        #QObjectWorkaround.__init__(self)
        self.view = view
        self.scale = scale
        self.color = color
        self.endTick = endTick
        self.pg = QtGui.QPolygonF([QtCore.QPointF(0,0), QtCore.QPointF(-scale/3**0.5,scale), QtCore.QPointF(scale/3**0.5,scale)])
        QtGui.QGraphicsPolygonItem.__init__(self, self.pg)
        self.setPos(pos[0], pos[1])
        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsSelectable)
        self.setBrush(QtGui.QBrush(QtGui.QColor(self.color)))
        if endTick:
            self.setZValue(0)
        else:
            self.setZValue(1)

    def x(self):
        return self.pos().x()/100.

    def mouseMoveEvent(self, ev):
        #print self, "move", ev.scenePos()
        if self.endTick:
            return
        if not ev.buttons() & QtCore.Qt.LeftButton:
            return
            
            
        newPos = ev.scenePos() + self.mouseOffset
        newPos.setY(self.pos().y())
        newPos.setX(min(max(newPos.x(), 0), 100))
        self.setPos(newPos)
        self.view.tickChanged(self)
        #self.emit(QtCore.SIGNAL('tickChanged'), self)
        ev.accept()

    def mousePressEvent(self, ev):
        #print self, "press", ev.scenePos()
        if ev.button() == QtCore.Qt.LeftButton:
            ev.accept()
            self.mouseOffset = self.pos() - ev.scenePos()
            self.pressPos = ev.scenePos()
        elif ev.button() == QtCore.Qt.RightButton:
            ev.accept()
            if self.endTick:
                return
            self.view.tickChanged(self, delete=True)
            #self.emit(QtCore.SIGNAL('tickChanged'), self, True)
            
    def mouseReleaseEvent(self, ev):
        #print self, "release", ev.scenePos()
        if ev.button() == QtCore.Qt.LeftButton and ev.scenePos() == self.pressPos:
            color = QtGui.QColorDialog.getColor(self.color, None, "Select Color", QtGui.QColorDialog.ShowAlphaChannel)
            if color.isValid():
                self.color = color
                self.setBrush(QtGui.QBrush(QtGui.QColor(self.color)))
                #self.emit(QtCore.SIGNAL('tickChanged'), self)
                self.view.tickChanged(self)
        