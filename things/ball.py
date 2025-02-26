from typing import NamedTuple, Self, override
import py5
from py5 import Sketch, Py5Vector

from things.collidableobject import CollidableObject
from things.point import Point
from utils.vecutils import VecUtils


# Fix intersection with forces
# Cause why not?
# Electrostatic prob




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
            self.point_intersection_canceller(obj)
        if type(obj) == Ball:
            obj: Ball
            self.collide_ball(obj)
            self.ball_intersection_canceller(obj)

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


    def ball_intersection_canceller(self, obj: Self):
        """
        During collision, the objects may intersect, and get stuck
        We forcefully set each of them out, in the directions they are at, to avoid this ig
        :param obj:
        :return:
        """
        natural_distance = self.radius + obj.radius
        relative_vector = obj.pos - self.pos
        difference = natural_distance - relative_vector.mag
        # Set them outwards, relative to their masses ig
        # Since outwards,  ↓ is minus 1
        self_outwards = ((-1)*relative_vector.norm)*(difference*self.mass)/(self.mass+obj.mass)
        obj_outwards = relative_vector.norm * (difference * obj.mass) / (self.mass + obj.mass)

        self.pos += self_outwards
        obj.pos += obj_outwards

    # Basically like ball, but the radius of point is 0
    def point_intersection_canceller(self, obj: Point):
        natural_distance = self.radius
        relative_vector = obj.pos - self.pos
        difference = natural_distance - relative_vector.mag
        # Set them outwards, relative to their masses ig
        # Since outwards,  ↓ is minus 1
        self_outwards = ((-1) * relative_vector.norm) * (difference * self.mass) / (self.mass + obj.mass)
        obj_outwards = relative_vector.norm * (difference * obj.mass) / (self.mass + obj.mass)

        self.pos += self_outwards
        obj.pos += obj_outwards


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






    def approximate_multi_particle_drag(self, obj_set: list[Self], force_coefficient: float, ray_count: int = 10):
        # F=6(pi)(nu)rv
        # Or F proportional to r and v
        # Where, (nu) is the viscosity, r is the radius, v is te velocity
        # Then we make rays downwards to see what percent of it intersects another ball
        # 100% intersection means 0 drag, 0% intersection means full drag
        # And then reduce the drag corresponding to this percent
        # IF high percent of it intersects, less the drag will be
        # (Skip calc for balls above it)


        # Positive y is down
        # We only want to check if y is more positive then, aka the obj y should be greater
        # Strict inequality to remove self as well
        possible_drag_reducers: list[Ball] = [obj for obj in obj_set if self.y < obj.y]

        initial_force_magnitude = force_coefficient*self.r*self.vel.y

        # Cast rays downwards
        # Let current particle pos: (a,b)
        # Optimization idea 1: Check if some other particle's center is withing x = a+r1+r2 or a-r1-r2
        # (So we dont have to check down rays through useless particle, which would be slow)
        possible_drag_reducers_2: list[Ball] = [
            obj for obj in possible_drag_reducers if (self.x-self.r-obj.r) < obj.x < (self.x+self.r+obj.r)
        ]

        # Since the rays are downwards
        # Just subdivide the span of the circle into ray_count parts
        all_rays: list[float] = [self.x+(self.r*offset/(ray_count/2)) for offset in range(round(-ray_count/2), round(ray_count/2)+1)]
        # (Actual rays = ray_count+1)
        # We evil like that

        intersect_count = 0
        for ray in all_rays:
            for particle in possible_drag_reducers_2:
                if (particle.x + particle.r) > ray > (particle.x - particle.r):
                    intersect_count += 1
                    break

        percent_intersection = intersect_count/(ray_count+1)

        # 100% (or 1) intersection means 0 drag, 0% (or 0) intersection means full drag
        actual_drag_force = initial_force_magnitude*(1-percent_intersection)
        self.apply_force(py5.Py5Vector(0,-actual_drag_force))


    def approximate_cohesion(self, other: Self, force_coefficient: float, closeness: float = 3):
        # Find list of all spheres within 3r of us ig?
        # This obj_set wont contain us, as for optimization
        # will use this as
        # for i in range(particles):
        #      for j in range(i+1,particles)
        #           ...

        relative_vector = other.pos - self.pos
        rel_vec_mag_sq = relative_vector.mag_sq
        if  rel_vec_mag_sq >= closeness **2 * self.r**2:
            return

        # Cohesion is kinda electrostatic like ig?
        # Its dipole dipole force, so proportional to 1/r^3
        # Ill keep it 1/r^2 tho, cause doesent rly matter, an magsq is quicker to calc

        relative_norm = relative_vector.norm
        force_mag = force_coefficient/rel_vec_mag_sq
        self.apply_force(relative_norm*force_mag)
        other.apply_force(relative_norm*(-1*force_mag))


        pass

if __name__ == "__main__":
    b = Ball(BallProperties(
        mass=1, restitution_coefficient=1,pos=py5.Py5Vector(0,0), radius=1,
        vel=py5.Py5Vector(0,100)
    ))
    b2 = Ball(BallProperties(mass=1, restitution_coefficient=1,pos=py5.Py5Vector(1,1), radius=1))
    b3 = Ball(BallProperties(mass=1, restitution_coefficient=1,pos=py5.Py5Vector(-1.5,1), radius=1))
    b.approximate_multi_particle_drag([b, b2,b3], 1, 10)
    print(b.acc, b.accumulated_acceleration)