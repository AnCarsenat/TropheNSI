class Matrix:
    def __init__(self, dims: int, value: int | float = 0):
        if dims < 0:
            raise ValueError("dims must be >= 0")
        self.dims = dims
        self.data = self._initiate(dims, value)

    @staticmethod
    def _initiate(dims: int, value: int | float = 0):
        if dims == 0:
            return []
        return [[value for _ in range(dims)] for _ in range(dims)]

    def __str__(self):
        if self.dims == 0:
            return "[]"
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.data)

    def __repr__(self):
        return str(self)

    def __len__(self):
        return self.dims

    def __getitem__(self, key: tuple[int, int]):
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("Matrix indices must be a (row, col) tuple")

        row, col = key
        if not (0 <= row < self.dims and 0 <= col < self.dims):
            raise IndexError("matrix index out of range")

        return self.data[row][col]

    def __setitem__(self, key: tuple[int, int], value: int | float):
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("Matrix indices must be a (row, col) tuple")

        row, col = key
        if not (0 <= row < self.dims and 0 <= col < self.dims):
            raise IndexError("matrix index out of range")

        self.data[row][col] = value

if __name__ == "__main__":
    m = Matrix(2, 1)
    print(m)
    print(m[0, 0])
    m[1, 1] = 7
    print(m)
    print(len(m))