import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from game_abstraction.math.vec2 import Vec2


def test_stores_coordinates_and_formats_values():
    vector = Vec2(5, 8)

    assert vector.x == 5
    assert vector.y == 8
    assert str(vector) == "(5,8)"


def test_creates_vector_from_subtraction():
    vector = Vec2.from_sub((1, 2), (4, 6))

    assert (vector.x, vector.y) == (3, 4)
