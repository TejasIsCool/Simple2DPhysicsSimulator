import random
import time
from os.path import split

import py5
from py5 import Sketch, Py5Vector, width
from py5 import Py5Vector as vec

from math import sqrt, sin, cos, pi

from things.ball import Ball, BallProperties

phi = (1 + sqrt(5)) / 2  # golden ratio
class SimulateRainDrop(Sketch):

    particle_set: list[Ball] = []
    count = 0

    def settings(self):
        self.size(1000, 700)

    def setup(self):
        # Start at height 0, a sphere of balls or smth

        # https://stackoverflow.com/questions/5837572/generate-a-random-point-within-a-circle-uniformly
        num_of_balls = 250
        individual_radius = 5.0
        mass = 1
        points_normalized = SimulateRainDrop.sunflower(num_of_balls, alpha=1)
        # Find distance between any two neighbouring points
        # The first and second point are neighbours ig
        # This is the distance between centers in the normalized point set, without considering radii
        # So actual normalized radii is half of this
        norm_dist = sqrt(
            (points_normalized[0][0]-points_normalized[1][0])**2
            +(points_normalized[0][1]-points_normalized[1][1])**2
        )
        scaling_factor = (individual_radius/(norm_dist/2))
        print(norm_dist, scaling_factor)
        # The last point is on the radius ig, the first is basically the center
        intial_drop_radius = sqrt(
            (points_normalized[0][0]-points_normalized[-1][0])**2
            +(points_normalized[0][1]-points_normalized[-1][1])**2
        )*scaling_factor

        drop_center_coords = (self.width/2, intial_drop_radius)

        self.particle_set: list[Ball] = []
        for i in range(num_of_balls):
            new_particle = Ball(
                BallProperties(
                    mass=mass,
                    restitution_coefficient=0.8,
                    pos=py5.Py5Vector(
                        drop_center_coords[0]+points_normalized[i][0]*scaling_factor,
                        drop_center_coords[1] + points_normalized[i][1] * scaling_factor
                    ),
                    radius=individual_radius
                )
            )
            self.particle_set.append(new_particle)
            pass


    def draw(self):
        print(f"Frame numeber: {self.count}")
        self.count+=1
        dt = 0.005
        self.background(100,165,215)
        # Divide the scene into two parts, one large overview, one following the drop

        self.push()
        self.stroke_weight(2)
        self.line(self.width / 2, 0, self.width / 2, self.height)
        self.pop()

        self.text_size(20)
        self.text("Far view", self.width / 8 ,20)
        self.text("Zoomed on view", 5*self.width / 8, 20)

        self.push()
        self.scale(0.25)
        self.translate(self.width/2, 0)
        for i,particle in enumerate(self.particle_set):
            if i == 0:
                self.fill(255,0,0)
            else:
                self.fill(255, 255, 255)
            particle.draw(self)
        self.pop()


        self.push()
        # self.scale(2)
        self.translate(3*self.width/4-self.particle_set[0].x, -self.particle_set[0].y+self.height/2)
        for i, particle in enumerate(self.particle_set):
            if i == 0:
                self.fill(255,0,0)
            else:
                self.fill(255, 255, 255)
            particle.draw(self)
        self.pop()

        for _ in range(25):
            SimulateRainDrop.perform_calc(self.particle_set, dt)

        self.save_frame(f"./output/raindrop3/{self.count:04}.png")




    @staticmethod
    def perform_calc(particle_set: list[Ball], dt):
        for i,particle in enumerate(particle_set):
            particle.apply_gravity(1)
            particle.approximate_multi_particle_drag(particle_set, 0.01, 6)

            for j in range(i + 1, len(particle_set)):
                particle.approximate_cohesion(particle_set[j], 20, closeness=3.5)
                particle.perform_collision(particle_set[j])
            particle.update_point(dt)




    # https://stackoverflow.com/questions/28567166/uniformly-distribute-x-points-inside-a-circle
    @staticmethod
    def sunflower(n: int, alpha=0, geodesic=False) -> list[tuple[float,float]]:
        """
        Returns a list of points in a radius 1 circle arranged uniformly
        :param n: number of points
        :param alpha: number of points on boundary
        :param geodesic: idk what this is
        :return: List of points as a 2d float tuple
        """
        points = []
        angle_stride = 360 * phi if geodesic else 2 * pi / phi ** 2
        b = round(alpha * sqrt(n))  # number of boundary points
        for k in range(1, n + 1):
            r = SimulateRainDrop.radius(k, n, b)
            theta = k * angle_stride
            points.append((r * cos(theta), r * sin(theta)))
        return points

    @staticmethod
    def radius(k, n, b):
        if k > n - b:
            return 1.0
        else:
            return sqrt(k - 0.5) / sqrt(n - (b + 1) / 2)



class SimulateRainDropTest(Sketch):

    particle_set: list[Ball] = []

    def settings(self):
        self.size(1000, 1000)

    def setup(self):
        b1 = Ball(BallProperties(
                        mass=5,
                        restitution_coefficient=0.8,
                        pos=py5.Py5Vector(
                            500,
                            20
                        ),
                        radius=10
        ))

        b2 = Ball(BallProperties(
                        mass=5,
                        restitution_coefficient=0.8,
                        pos=py5.Py5Vector(
                            505,
                            100
                        ),
                        radius=10
        ))

        b3 = Ball(BallProperties(
            mass=5,
            restitution_coefficient=0.8,
            pos=py5.Py5Vector(
                600,
                20
            ),
            radius=10
        ))

        b4 = Ball(BallProperties(
            mass=5,
            restitution_coefficient=0.8,
            pos=py5.Py5Vector(
                200,
                20
            ),
            radius=10
        ))

        b5 = Ball(BallProperties(
            mass=5,
            restitution_coefficient=0.8,
            pos=py5.Py5Vector(
                200,
                400
            ),
            radius=10
        ))
        self.particle_set = [b1,b2,b3, b4, b5]



    def draw(self):
        for i in range(10):
            dt = 0.01
            self.background(100, 100, 100)
            for i, particle in enumerate(self.particle_set):
                particle.draw(self)
                particle.apply_gravity(1)
                particle.approximate_multi_particle_drag(self.particle_set, 0.01, 9)
                for j in range(i + 1, len(self.particle_set)):
                    particle.perform_collision(self.particle_set[j])
                particle.update_point(dt)


rain_drop_sketch = SimulateRainDrop()
# rain_drop_sketch = SimulateRainDropTest()
rain_drop_sketch.run_sketch()