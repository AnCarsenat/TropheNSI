class Color4:
    def __init__(self,value:tuple[int,int,int,int],mode:"255"|"0"="255"):
        self.mode = mode

        assert len(value)==3 or 4
        assert all(val is not None for val in value)
        
        self.r = value[0]
        self.g = value[1]
        self.b = value[2]
        self.a = value[3]
        
        if not self.a:
            if mode == "255":
                self.a == 255
            elif mode == "0":
                self.a == 1


    @property
    def r(self):
        return self._r
    @r.setter
    def r(self, value):
        if self.mode == "255":
            assert 0<=value<=255
        elif self.mode == "0":
            assert 0<=value<=1
        self._r = value 

    @property
    def g(self):
        return self._g
    @g.setter
    def g(self, value):
        if self.mode == "255":
            assert 0<=value<=255
        elif self.mode == "0":
            assert 0<=value<=1
        self._g = value 

    @property
    def b(self):
        return self._b
    @b.setter
    def b(self, value):
        if self.mode == "255":
            assert 0<=value<=255
        elif self.mode == "0":
            assert 0<=value<=1
        self._b = value 

    
    @property
    def a(self):
        return self._a
    @a.setter
    def a(self, value):
        if self.mode == "255":
            assert 0<=value<=255
        elif self.mode == "0":
            assert 0<=value<=1
        self._a = value 



    def __getitem__(self, key):
        match key:
            case 0:
                return self.r
            case 1:
                return self.g
            case 2:
                return self.b
            case _:
                raise IndexError("Index out of range (0<=x<=2)")
            
    def __str__(self):
        return str((self.r,self.g,self.b))
   
    @property
    def beautiful_str(self):
        from ..ascii_colors import ascii_colors as colors
        return f"({colors.RED}{self.r}{colors.RESET},{colors.GREEN}{self.g}{colors.RESET},{colors.BLUE}{self.b}{colors.RESET})"