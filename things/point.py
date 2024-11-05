import py5


class Point:
    def __init__(
            self, mass: float,
            pos: py5.Py5Vector,
            vel: py5.Py5Vector = py5.Py5Vector(0,0),
            acc: py5.Py5Vector = py5.Py5Vector(0,0)):
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.accumulated_acceleration = acc

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
        self.apply_force(py5.Py5Vector(0,magnitude))