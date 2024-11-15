import random
from os.path import split

import py5
from py5 import Sketch, mouse_x, mouse_y, Py5Vector
from py5 import Py5Vector as vec
from things.point import Point
from things.spring import Spring, SpringProperties
from things.ball import Ball, BallProperties


class SimulateSprings(Sketch):

    def settings(self):
        self.size(1000, 1000)

    def setup(self):
        self.rect_mode(self.CENTER)
        self.points = [
            Point(1, vec(520,500)),
            Point(1, vec(500,580))
        ]
        self.spring = Spring(
            SpringProperties(
                p1=self.points[0],p2=self.points[1],
                k=2,natural_length=50
            )
        )
        self.frame_rate(60)

    def draw(self):
        self.background(100,100,100)
        self.spring.apply_force()
        self.rect(0,0,10,10)
        self.line(
            self.points[0].pos.x,self.points[0].pos.y,self.points[1].pos.x,self.points[1].pos.y
        )
        for point in self.points:
            point.dampen(1)
            self.rect(point.pos.x, point.pos.y, 20, 20)
            point.update_point(1/60)
        self.points[1].pos = vec(self.mouse_x,self.mouse_y)

class SimulateTwoSprings(Sketch):

    def settings(self):
        self.size(1000, 1000)

    def setup(self):
        self.rect_mode(self.CENTER)
        self.points = [
            Point(1, vec(520,500)),
            Point(1, vec(500,580)),
            Point(1, vec(460,580))
        ]
        self.springs: list[Spring] = []
        for i in range(2):
            new_spr = Spring(
                SpringProperties(
                    p1=self.points[i],
                    p2=self.points[i+1],
                    k=4, natural_length=50
                )
            )
            self.springs.append(new_spr)
        self.frame_rate(60)

    def draw(self):
        self.background(100,100,100)
        for spring in self.springs:
            spring.apply_force()
        self.rect(0,0,10,10)
        for i in range(2):
            self.line(
                self.points[i].pos.x,self.points[i].pos.y,self.points[i+1].pos.x,self.points[i+1].pos.y
            )
        for point in self.points:
            point.apply_gravity(200)
            point.dampen(0.2)
            self.rect(point.pos.x, point.pos.y, 20, 20)
            point.update_point(1/60)
        self.points[0].pos = vec(self.mouse_x,self.mouse_y)


class SpringTower(Sketch):
    def settings(self):
        self.size(1000, 1000)

    def setup(self):
        self.count = 0
        self.numlayers = 8
        mass = 0.01
        k = 1000
        natural_length = 20
        self.tower_width = 40
        self.rect_mode(self.CENTER)
        # Generate points layer by layer
        self.points: list[tuple[Point,Point]] = []
        self.springs: list[Spring] = []
        for i in range(self.numlayers):
            p1 = Point(mass,vec(500-self.tower_width/2,600-natural_length*i))
            p2 = Point(mass,vec(500+self.tower_width/2,600-natural_length*i))
            self.points.append((p1,p2,))
            self.springs.append(Spring(
                SpringProperties(
                    p1=p1, p2=p2, k=k, natural_length=self.tower_width
                )
            ))

        # Springs connecting layers
        for j in range(self.numlayers-1):
            self.springs.append(
                Spring(SpringProperties(
                    self.points[j][0], self.points[j+1][0],
                    k=k, natural_length=natural_length
                ))
            )
            self.springs.append(
                Spring(SpringProperties(
                    self.points[j][1], self.points[j + 1][1],
                    k=k, natural_length=natural_length
                ))
            )
            self.springs.append(
                Spring(SpringProperties(
                    self.points[j][0], self.points[j + 1][1],
                    k=k+100, natural_length=(self.tower_width**2+natural_length**2)**(0.5)
                ))
            )
            self.springs.append(
                Spring(SpringProperties(
                    self.points[j][1], self.points[j + 1][0],
                    k=k+100, natural_length=(self.tower_width**2+natural_length**2)**(0.5)
                ))
            )

        self.frame_rate(120)

    def draw(self):
        dt = 1/600
        for i in range(10):
            self.background(100,100,100)
            # Draw the springs, and also apply force
            for spring in self.springs:
                p1 = spring.p1
                p2 = spring.p2
                self.line(p1.pos.x,p1.pos.y,p2.pos.x,p2.pos.y)
                spring.apply_force()

            self.rect(self.points[0][0].pos.x, self.points[0][0].pos.y, 10, 10)
            self.rect(self.points[0][1].pos.x, self.points[0][1].pos.y, 10, 10)
            # Update all points, except the bottom ones
            for i in range(1,self.numlayers):
                self.points[i][0].update_point(dt)
                self.points[i][0].apply_gravity(10)
                self.points[i][0].dampen(0.05)
                self.points[i][1].update_point(dt)
                self.points[i][1].apply_gravity(10)
                self.points[i][1].dampen(0.05)
                self.rect(self.points[i][0].pos.x, self.points[i][0].pos.y, 4, 4)
                self.rect(self.points[i][1].pos.x, self.points[i][1].pos.y, 4, 4)

            if self.is_mouse_pressed:
                self.circle(self.mouse_x,self.mouse_y,20)
                self.points[self.numlayers-1][1].apply_force((py5.Py5Vector(self.mouse_x,self.mouse_y)-self.points[self.numlayers-1][1].pos)*100)
                self.points[self.numlayers - 1][0].apply_force(
                    (py5.Py5Vector(self.mouse_x, self.mouse_y) - self.points[self.numlayers - 1][0].pos) * 100)

        self.count += 1
        #self.save_frame(f"./output/springtower/{self.count:04}.png")

# Tears in my eyes
class SpringTower2ElectricBogaloo(Sketch):
    def settings(self):
        self.size(1000, 1000)

    def setup(self):
        self.count = 0
        self.numlayers = 80
        mass = 0.001
        k = 1000
        natural_length = 4
        self.tower_width = 40
        self.rect_mode(self.CENTER)
        # Generate points layer by layer
        self.points: list[tuple[Point,Point,Point]] = []
        self.springs: list[Spring] = []
        for i in range(self.numlayers):
            p1 = Point(mass,vec(500-self.tower_width/2,600-natural_length*i))
            p2 = Point(mass,vec(500+self.tower_width/2,600-natural_length*i))
            p3 = None
            if i != 0:
                p3 = Point(mass, vec(500, (600+natural_length/2)-natural_length*i))
                self.springs.append(Spring(
                    SpringProperties(
                        p1=p1, p2=p3, k=k, natural_length=((self.tower_width/2)**2+(natural_length/2)**2) ** 0.5
                    )
                ))
                self.springs.append(Spring(
                    SpringProperties(
                        p1=p2, p2=p3, k=k, natural_length=((self.tower_width/2)**2+(natural_length/2)**2) ** 0.5
                    )
                ))

            self.points.append((p1,p2,p3))
            self.springs.append(Spring(
                SpringProperties(
                    p1=p1, p2=p2, k=k, natural_length=self.tower_width
                )
            ))

        # Springs connecting to middle element
        for j in range(self.numlayers-1):
            self.springs.append(
                Spring(SpringProperties(
                    self.points[j][0], self.points[j+1][0],
                    k=k, natural_length=natural_length
                ))
            )
            self.springs.append(
                Spring(SpringProperties(
                    self.points[j][1], self.points[j + 1][1],
                    k=k, natural_length=natural_length
                ))
            )
            self.springs.append(
                Spring(SpringProperties(
                    self.points[j][0], self.points[j + 1][2],
                    k=k+100, natural_length=((self.tower_width/2)**2+(natural_length/2)**2) ** 0.5
                ))
            )
            self.springs.append(
                Spring(SpringProperties(
                    self.points[j][1], self.points[j + 1][2],
                    k=k+100, natural_length=((self.tower_width/2)**2+(natural_length/2)**2) ** 0.5
                ))
            )

        self.frame_rate(120)

    def draw(self):
        dt = 1/6000
        for i in range(1):
            self.background(100,100,100)
            # Draw the springs, and also apply force
            for spring in self.springs:
                p1 = spring.p1
                p2 = spring.p2
                self.line(p1.pos.x,p1.pos.y,p2.pos.x,p2.pos.y)
                spring.apply_force()
            self.rect(self.points[0][0].pos.x, self.points[0][0].pos.y, 10, 10)
            self.rect(self.points[0][1].pos.x, self.points[0][1].pos.y, 10, 10)
            # Update all points, except the bottom ones
            for i in range(1,self.numlayers):
                for j in range(3):
                    if self.points[i][j] is None:
                        continue
                    self.points[i][j].update_point(dt)
                    self.points[i][j].apply_gravity(10)
                    # dampening 0.05 lasts better
                    self.points[i][j].dampen(0.01)
                    self.rect(self.points[i][j].pos.x, self.points[i][j].pos.y, 4, 4)

            if self.is_mouse_pressed:
                self.circle(self.mouse_x,self.mouse_y,20)
                self.points[self.numlayers-1][1].apply_force((py5.Py5Vector(self.mouse_x,self.mouse_y)-self.points[self.numlayers-1][1].pos)*100)
                self.points[self.numlayers - 1][0].apply_force(
                    (py5.Py5Vector(self.mouse_x, self.mouse_y) - self.points[self.numlayers - 1][0].pos) * 100)

        self.count += 1
        #self.save_frame(f"./output/springtower2/parttwo{self.count:04}.png")


class CollisionTesting(Sketch):
    def settings(self):
        self.size(500, 500)
        self.bounds = (Py5Vector(0,0), Py5Vector(self.width, self.height))

    def setup(self):
        self.count = 0
        # Spawn a bunch of collidable balls
        self.num_of_balls = 10

        self.balls_list = []
        self.random_colors = [
            [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            for _ in range(self.num_of_balls)
        ]
        for i in range(self.num_of_balls):
            offset = (self.bounds[1].x - self.bounds[0].x)*(i+0.5)/self.num_of_balls
            mass = random.randint(2,4)
            self.balls_list.append(
                Ball(
                    BallProperties(
                        mass=mass,
                        restitution_coefficient=1,
                        pos=Py5Vector(self.bounds[0].x+offset,self.bounds[0].y+offset),
                        radius=(random.randint(5,6))*mass
                    ))
            )
        self.frame_rate(120)

    def draw(self):
        dt = 1/60
        self.background(100, 100, 100)
        for i in range(self.num_of_balls):
            ball = self.balls_list[i]
            self.push()
            self.fill(self.random_colors[i][0],self.random_colors[i][1],self.random_colors[i][2])
            ball.draw(self)
            self.pop()
            ball.constraint_in_bound(self.bounds)
            ball.update_point(dt)
            for j in range(i+1,self.num_of_balls):
                ball.perform_collision(self.balls_list[j])

        if self.is_mouse_pressed:
            self.balls_list[-1].apply_force((py5.Py5Vector(self.mouse_x, self.mouse_y) - self.balls_list[-1].pos)*5)
            pass

        self.count += 1
        #self.save_frame(f"./output/collisiontest/attempt2/{self.count:04}.png")


# class BallAndSpring(Sketch):
#     pass

simspr = CollisionTesting()
simspr.run_sketch()