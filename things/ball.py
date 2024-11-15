from typing import NamedTuple, Self, override
import py5
from py5 import Sketch, Py5Vector

from things.collidableobject import CollidableObject
from things.point import Point
from utils.vecutils import VecUtils


class BallProperties(NamedTuple):
    mass: float
    restitution_coefficient: float
    pos: py5.Py5Vector
    vel: py5.Py5Vector = py5.Py5Vector(0,0)
    acc: py5.Py5Vector = py5.Py5Vector(0, 0)
    radius: float = 10



class Ball(CollidableObject):
    def __init__(self, properties: BallProperties):
        self.mass = properties.mass
        self.restitution_coefficient = properties.restitution_coefficient
        self.pos = properties.pos
        self.vel = properties.vel
        self.acc = properties.acc
        self.accumulated_acceleration = self.acc
        self.radius = properties.radius
        self.radius_sq = self.radius ** 2

    @property
    def r(self) -> float:
        """
        Shorthand for self.radius
        :return: self.radius
        """
        return self.radius

    @r.setter
    def r(self, value: float):
        self.radius = value


    def draw(self, sketch: Sketch):
        sketch.circle(self.x, self.y, self.radius*2)


    def check_collision(self, obj: CollidableObject) -> bool:
        if type(obj) == Point:
            distance_sq = (self.pos-obj.pos).mag_sq
            if distance_sq <= self.radius_sq:
                return True
            else:
                return False
        if type(obj) == Ball:
            obj: Ball
            distance_sq = (self.pos - obj.pos).mag
            if distance_sq <= (self.radius+obj.radius):
                return True
            else:
                return False

        # If collisions not defined, let them not collide ig
        return False

    def perform_collision(self, obj: CollidableObject):
        if not self.check_collision(obj):
            return
        if type(obj) == Point:
            obj: Point
            self.collide_point(obj)
        if type(obj) == Ball:
            obj: Ball
            self.collide_ball(obj)

    def collide_point(self, obj: Point):
        # Relative vector from ball to point
        rel_vec = (obj.pos - self.pos)
        rel_dir = rel_vec.norm
        rel_dir_neg = -rel_dir

        # Line of impact is the line joining the point to the center of ball
        # Direction of velocity of Point along LOI
        # Is a projection vector of its velocity along the relative vector
        point_vel_loi = VecUtils.projection(obj.vel, rel_dir_neg)
        # Likewise for ball
        ball_vel_loi = VecUtils.projection(self.vel, rel_dir)

        resulting_restitution = self.restitution_coefficient*obj.restitution_coefficient

        # v₁ = (m₁−em₂)u̅₁ + (1+e)m₂u̅₂ / (m₁+m₂)
        # v₂ = (m₂−em₁)u̅₂ + (1+e)m₁u̅₁ / (m₁+m₂)
        # Index 1 is self/ball, index 2 is point
        ball_vel_resultant = (
                (self.mass-resulting_restitution*obj.mass)*ball_vel_loi
                +
                (1+resulting_restitution)*obj.mass*point_vel_loi
        ) / (self.mass + obj.mass)

        point_vel_resultant = (
                (obj.mass - resulting_restitution * self.mass) * point_vel_loi
                +
                (1 + resulting_restitution) * self.mass * ball_vel_loi
        ) / (self.mass + obj.mass)

        # Now we replace velocity components along loi with the new ones
        # Do this by subtract the previous, and adding the new

        self.vel -= ball_vel_loi
        self.vel += ball_vel_resultant

        obj.vel -= point_vel_loi
        obj.vel += point_vel_resultant

    def collide_ball(self, obj: Self):
        obj: Point
        # The mathematical part is identical to a point
        self.collide_point(obj)

    @override
    def constraint_in_bound(self, bounds: tuple[Py5Vector, Py5Vector]):
        """
        Constraint the ball within this square region, define by bound
        :param bounds: tuple(Vec of top left corner, Vec of top right corner)
        :return:
        """
        # X Axis
        if (self.x - self.r) < bounds[0].x:
            self.x = bounds[0].x + self.r
            self.vel.x *= -1
        if (self.x + self.r) > bounds[1].x:
            self.x = bounds[1].x - self.r
            self.vel.x *= -1

        # Y axis (Positive is down)
        if (self.y - self.r) < bounds[0].y:
            self.y = bounds[0].y + self.r
            self.vel.y *= -1
        if (self.y + self.r) > bounds[1].y:
            self.y = bounds[1].y - self.r
            self.vel.y *= -1