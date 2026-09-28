# Owo
class Vec2:
    """Magnifique implémentation d'un Vec2 ;p"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_sub(start:tuple[float,float], end:tuple[float,float]):
        return Vec2(end[0] - start[0], end[1] - start[1])

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, value:float)->"Vec2":
        return Vec2(self.x * value, self.y * value)

    def __truediv__(self, value:float)->"Vec2":
        return Vec2(self.x / value, self.y / value)
    
    def __str__(self)->str:
        return f"({self.x},{self.y})"

    def clone(self)->"Vec2":
        from copy import deepcopy
        return deepcopy(self)

    @property
    def norm(self)->float:
        magnitude = self.magnitude
        return Vec2(self.x/magnitude,self.y/magnitude)

    @property
    def magnitude(self)->float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @staticmethod
    def dot_product(vec1:"Vec2",vec2:"Vec2")->"Vec2":
        raise(NotImplementedError)

    def __getitem__(self, key:int)->int:
        if key>1:
            return None
        elif key==1:
            return self.y
        elif key==0:
            return self.x

    @property
    def beautiful_str(self):
        from ..ascii_colors import colors
        return f"({colors.RED}{self.x}{colors.RESET},{colors.BRIGHT_GREEN}{self.y}{colors.RESET})"

    def display(self)->None:
        """If there is pygame display on screen"""
        raise NotImplementedError