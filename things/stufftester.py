from things.point import Point
from py5 import Py5Vector as vec

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
