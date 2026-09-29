from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..color import Color3, Color4
    from ..math.vec2 import Vec2



class Node2D:
    class Properties:
        def __init__(self):
            self.pos = None
            self.visible = True
            self.modulate:Color3|Color4 = None

    def __init__(
        self,
        pos: "Vec2" = None,
        parent: Node2D | None = None,
        children: list[Node2D] | None = None,
        properties: Properties | None = None,
    ):
        from ..math.vec2 import Vec2
        if pos is None:
            pos = Vec2(0,0)
        
        self.properties = properties if properties is not None else Node2D.Properties()
        self.properties.pos = pos
        self.parent = parent
        self.children = children if children is not None else []
        self.game = None

    def add_child(self, child:Node2D)->None:
        self.children.append(child)

    def wait_for_child(self, childName:str, maxWaitTime:float=5.0)->Node2D:
        ...
        #Tries find first child then waits until a new child is added.
        #Holds execution until found with a max hold of 5 seconds

    def find_first_child(self, childName:str)->Node2D:
        ...
        #Returns first child None if not found

    def _set_game(self, game):
        self.game = game
        for child in self.children:
            child._set_game(game)
