from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .node2d import Node2D

class Scene2d(Node2D):
    def __init__(self):
        super.__init__(self)
        self.active_camera = None
        self.scene = self

    def tick(self):
        for child in self.children:
            child.tick()