# Reference: https://stackoverflow.com/a/55899694
# Changes:
# Upgraded PyQt version to PyQt5
# Added some style controls, custom properties and signals

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys

CENTER = -1
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


class Joystick(QWidget):

    stickMoved = pyqtSignal(int, float)

    def __init__(self, parent=None, __pivotRadius=100, __stickRadius=40) -> None:
        super(Joystick, self).__init__(parent)
        self.__pivotRadius = __pivotRadius
        self.__stickRadius = __stickRadius
        maxDistance = self.__pivotRadius + self.__stickRadius
        self.setMinimumSize(maxDistance * 2, maxDistance * 2)
        self.movingOffset = QPointF(0, 0)
        self.grabCenter = False

    def setGeometry(self, a0: QRect):
        self.setMinimumSize(0, 0)
        bound = min(a0.width(), a0.height()) // 2
        maxDistance = self.__pivotRadius + self.__stickRadius
        if maxDistance == 0:
            maxDistance = 1
        self.__pivotRadius = self.__pivotRadius * bound // maxDistance
        self.__stickRadius = self.__stickRadius * bound // maxDistance
        if self.__pivotRadius == 0:
            self.__pivotRadius = 5
        if self.__stickRadius == 0:
            self.__stickRadius = 2
        super().setGeometry(a0)
        maxDistance = self.__pivotRadius + self.__stickRadius
        self.setMinimumSize(maxDistance * 2, maxDistance * 2)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        bounds = QRectF(-self.__pivotRadius, -self.__pivotRadius,
                        self.__pivotRadius * 2, self.__pivotRadius * 2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(Qt.black)
        painter.drawEllipse(self._centerEllipse())

    def _centerEllipse(self) -> QRectF:
        if self.grabCenter:
            return QRectF(-self.__stickRadius, -self.__stickRadius, self.__stickRadius * 2, self.__stickRadius * 2).translated(self.movingOffset)
        return QRectF(-self.__stickRadius, -self.__stickRadius, self.__stickRadius * 2, self.__stickRadius * 2).translated(self._center())

    def _center(self) -> QPointF:
        return QPointF(self.width() / 2, self.height() / 2)

    def _boundJoystick(self, point) -> QPointF:
        limitLine = QLineF(self._center(), point)
        if (limitLine.length() > self.__pivotRadius):
            limitLine.setLength(self.__pivotRadius)
        return limitLine.p2()

    @pyqtProperty(int)
    def pivotRadius(self):
        return self.__pivotRadius

    @pivotRadius.setter
    def pivotRadius(self, pivotRadius):
        if pivotRadius == 0:
            return
        self.__pivotRadius = pivotRadius
        maxDistance = self.__pivotRadius + self.__stickRadius
        geometry = QRect(0, 0, maxDistance * 2, maxDistance * 2)
        geometry.moveCenter(self.geometry().center())
        self.setMinimumSize(0, 0)
        super().setGeometry(geometry)
        self.setMinimumSize(maxDistance * 2, maxDistance * 2)
        self.update()

    def setPivotRadius(self, pivotRadius):
        self.pivotRadius(pivotRadius)

    @pyqtProperty(int)
    def stickRadius(self):
        return self.__stickRadius

    @stickRadius.setter
    def stickRadius(self, stickRadius):
        if stickRadius == 0:
            return
        self.__stickRadius = stickRadius
        maxDistance = self.__pivotRadius + self.__stickRadius
        geometry = QRect(0, 0, maxDistance * 2, maxDistance * 2)
        geometry.moveCenter(self.geometry().center())
        self.setMinimumSize(0, 0)
        super().setGeometry(geometry)
        self.setMinimumSize(maxDistance * 2, maxDistance * 2)
        self.update()

    def setStickRadius(self, stickRadius):
        self.stickRadius(stickRadius)

    def joystickDirection(self) -> tuple[int, float]:
        if not self.grabCenter:
            return (CENTER, 0)
        normVector = QLineF(self._center(), self.movingOffset)
        currentDistance = normVector.length()
        if currentDistance == 0:
            return (CENTER, 0)
        angle = normVector.angle()

        distance = min(currentDistance / self.__pivotRadius, 1.0)
        if 45 <= angle < 135:
            return (UP, distance)
        elif 135 <= angle < 225:
            return (LEFT, distance)
        elif 225 <= angle < 315:
            return (DOWN, distance)
        return (RIGHT, distance)

    def mousePressEvent(self, ev) -> None:
        self.grabCenter = self._centerEllipse().contains(ev.pos())
        super().mousePressEvent(ev)

    def mouseReleaseEvent(self, event) -> None:
        self.grabCenter = False
        self.movingOffset = QPointF(0, 0)
        self.update()
        self.stickMoved.emit(-1, 0)

    def mouseMoveEvent(self, event) -> None:
        if self.grabCenter:
            self.movingOffset = self._boundJoystick(event.pos())
            self.update()
        self.stickMoved.emit(*self.joystickDirection())


if __name__ == '__main__':
    # Create main application window
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Cleanlooks"))
    mw = QMainWindow()
    mw.setWindowTitle('Joystick example')

    # Create and set widget layout
    # Main widget container
    cw = QWidget()
    ml = QGridLayout()
    cw.setLayout(ml)
    mw.setCentralWidget(cw)

    # Create joystick
    joystick1 = Joystick()
    joystick2 = Joystick()

    # ml.addLayout(joystick.get_joystick_layout(),0,0)
    ml.addWidget(joystick1, 0, 0)
    ml.addWidget(joystick2, 1, 0)

    mw.show()

    # Start Qt event loop unless running in interactive mode or using pyside.
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QApplication.instance().exec_()
