from typing import NamedTuple
import py5

from things.point import Point


class SpringProperties(NamedTuple):
    p1: Point
    p2: Point
    k: float
    natural_length: float


class Spring:
    def __init__(self, properties: SpringProperties):
        self.p1: Point = properties.p1
        self.p2: Point = properties.p2
        self.k: float = properties.k
        self.natural_length: float = properties.natural_length


    def apply_force(self):
        # Calculating force first
        # F = kΔx, where Δx is the difference in natural length and current length
        # Δx should be signed, for compressive and expansive force
        # And F is the magnitude of force
        # The force is applied for p1 towards p2, and for p2 towards p1
        relative_vector = self.p2.pos-self.p1.pos
        relative_norm = relative_vector.norm
        force_mag = self.k * (relative_vector.mag - self.natural_length)
        self.p1.apply_force(relative_norm*force_mag)
        self.p2.apply_force(relative_norm*(-1*force_mag))

        pass