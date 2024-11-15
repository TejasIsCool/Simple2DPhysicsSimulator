import py5
from py5 import Py5Vector


class CollidableObject:
    mass: float
    restitution_coefficient: float
    pos: py5.Py5Vector
    vel: py5.Py5Vector
    acc: py5.Py5Vector
    accumulated_acceleration: py5.Py5Vector

    def update_point(self, dt: float):
        self.acc = self.accumulated_acceleration
        self.vel = self.vel + self.acc*dt
        self.pos = self.pos + self.vel*dt
        self.accumulated_acceleration = py5.Py5Vector(0,0)

    def apply_force(self, force: py5.Py5Vector):
        # Should it be +=?
        self.accumulated_acceleration += (force/self.mass)

    def dampen(self, coefficient: float):
        self.apply_force((self.vel*(-1*coefficient)))

    def apply_gravity(self, magnitude: float):
        self.apply_force(py5.Py5Vector(0,self.mass*magnitude))


    def constraint_in_bound(self, bounds: tuple[Py5Vector, Py5Vector]):
        """
        Constraint the object within this square region, define by bound
        :param bounds: tuple(Vec of top left corner, Vec of top right corner)
        :return:
        """
        # X Axis
        if self.x < bounds[0].x:
            self.vel.x *= -1
        if self.x > bounds[1].x:
            self.vel.x *= -1

        # Y axis (Positive is down)
        if self.y < bounds[0].y:
            self.vel.y *= -1
        if self.y > bounds[1].y:
            self.vel.y *= -1

    @property
    def x(self) -> float:
        """
        Shorthand for self.pos.x
        :return: self.pos.x
        """
        return self.pos.x

    @x.setter
    def x(self, value: float):
        self.pos.x = value

    @property
    def y(self) -> float:
        """
        Shorthand for self.pos.y
        :return: self.pos.y
        """
        return self.pos.y

    @y.setter
    def y(self, value: float):
        self.pos.y = value