# Owo
class Vec3:
    """Magnifique implémentation d'un Vec3 ;p"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def from_sub(start:tuple[float,float,float], end:tuple[float,float,float]):
        return Vec3(end[0] - start[0], end[1] - start[1], end[2] - start[2])

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        
    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, value:float)->"Vec3":
        return Vec3(self.x * value, self.y * value, self.z / value)

    def __truediv__(self, value:float)->"Vec3":
        return Vec3(self.x / value, self.y / value, self.z / value)
    
    def __str__(self)->str:
        return f"({self.x},{self.y},{self.z})"

    def clone(self)->"Vec3":
        from copy import deepcopy
        return deepcopy(self)

    @property
    def norm(self)->float:
        magnitude = self.magnitude
        return Vec3(self.x/magnitude,self.y/magnitude,self.z/magnitude)

    @property
    def magnitude(self)->float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @staticmethod
    def dot_product(vec1:"Vec3",Vec3:"Vec3")->"Vec3":
        raise(NotImplementedError)

    def __getitem__(self, key:int)->int:
        match key:
            case 2:
                return self.z
            case 1:
                return self.y
            case 0:
                return self.x
            case _:
                return None 

    @property
    def beautiful_str(self):
        from ..ascii_colors import colors
        return f"({colors.RED}{self.x}{colors.RESET},{colors.BRIGHT_GREEN}{self.y}{colors.RESET},{colors.BLUE}{self.z}{colors.RESET})"

    def display(self)->None:
        """If there is pygame display on screen"""
        raise NotImplementedError