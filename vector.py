from __future__ import division
import math
class Vector(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return self + (-other)
    def __mul__(self, other):
        return Vector(self.x*other, self.y*other)
    def __neg__(self):
        return Vector(-self.x, -self.y)
    def direction(self):
        if self.x==0:
            if self.y>0:return (math.pi * 0.5)
            elif self.y<0:return (math.pi * 1.5)
            else: return 0
        return math.atan(self.y/self.x)
    def magnitude(self):
        return math.sqrt(self.x**2+self.y**2)
    def truncate(self, maxSpeed):
        if self.magnitude()>maxSpeed:
            v=Vector.fromDandM(self.direction(), maxSpeed)
            self.x, self.y=v.x, v.y
    def normalize(self):
        m=self.magnitude()
        if m==0:return Vector(0,0)
        return Vector(self.x/m, self.y/m)
    def __str__(self):
        return "<"+str(self.x)+","+str(self.y)+">"
    
       
    @classmethod
    def fromDandM(cls,direction, magnitude):
        x=magnitude*math.cos(direction)
        y=magnitude*math.sin(direction)
        return Vector(x, y)
