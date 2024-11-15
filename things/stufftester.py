from things.point import Point
from py5 import Py5Vector as vec, Py5Vector

P = Point(
    2,
    pos=vec(0,0),
    vel=vec(1,2),
    acc=vec(0,5)
)

print(P.pos, P.vel)
P.update_point(0.1)
print(P.pos, P.vel)
P.apply_force(vec(-0.5,2))
print(P.acc)
P.x = 12
print(P.x, P.y, P.pos)

ayo_vec = Py5Vector(5,6,7)
ayo_vec2 = Py5Vector(1,-5,11)
print(ayo_vec2+ayo_vec-ayo_vec2)

ayo_vec += ayo_vec2*2
print(ayo_vec)

ayo_vec = ayo_vec + ayo_vec
print(ayo_vec)

ayo_vec*=2
print(ayo_vec)

ayo_vec.x *= -1
print(ayo_vec)

