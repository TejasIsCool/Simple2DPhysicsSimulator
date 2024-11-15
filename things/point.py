import py5
from py5 import Sketch, Py5Vector

from things.collidableobject import CollidableObject


class Point(CollidableObject):
    def __init__(
            self, mass: float,
            pos: py5.Py5Vector,
            vel: py5.Py5Vector = py5.Py5Vector(0,0),
            acc: py5.Py5Vector = py5.Py5Vector(0,0),
            restitution_coefficient: float = 1
    ):
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.restitution_coefficient = restitution_coefficient
        self.accumulated_acceleration = acc

    def draw(self, sketch: Sketch, radius: float = 5):
        sketch.circle(self.x, self.y, radius)

