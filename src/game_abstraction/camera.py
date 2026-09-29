from math import atan, tan
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .math.vec2 import Vec2

from .node2d import Node2D
class Camera(Node2D):
    def __init__(self, position:"Vec2", fov=None, zoom=1, sensor_width=1):
        super().__init__(pos=position)
        self.sensor_width = sensor_width
        if fov is None:
            self.zoom = zoom
        else:
            self.fov = fov

    @property
    def fov(self):
        return self._fov

    @fov.setter
    def fov(self, value):
        self._fov = value
        self._zoom = self.sensor_width / (2 * tan(value / 2))

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = value
        self._fov = 2 * atan(self.sensor_width / (2 * value))


# The zoom-to-FOV formula converts a zoom value (in pixels)
# to the field of view angle using the sensor width and the zoom value: 
# zoom = width / (2 × tan(FOV)).