from __future__ import division
import pygame, util
import math
class Vector(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def __add__(self, other):
        return Vector((self.x+other.x), (self.y+other.y))
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
            v=self.normalize()*maxSpeed
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
#if all of these die the game ends
vital=[]
def newvitals(n):
    global vital
    for i in range(n):vital.append(util.Group())
def main(_groups, config, *args):
    #_groups should be a dictionary mapping group names to groups
    #config should be a dictionary:
    #   "res":screen resolution in the format (width, height), defaults to (640, 480)
    #   "keydelay":delay in ms before key starts repeating, defaults to 5
    #   "keyinterval":interval in ms before key repeat events, defaults to 5
    #additional arguments are sprites to render and update
    pygame.init()
    try:res=config["res"]
    except KeyError:res=(640, 480)
    try:keydelay=config["keydelay"]
    except KeyError:keydelay=5
    try:keyinterval=config["keyinterval"]
    except KeyError:keyinterval=5
    pygame.key.set_repeat(keydelay, keyinterval)
    if len(vital)<1:vitalneeded=False
    else:vitalneeded=True
    mixer=pygame.mixer
    mixer.init()
    music=mixer.music
    screen=pygame.display.set_mode(res)
    canvas=pygame.Surface(screen.get_size())
    canvas=canvas.convert()
    #add your sprite to this group to have it rendered each time step
    #sprites added first will be drawn first
    rendered=pygame.sprite.OrderedUpdates()
    #add your sprite to this group to have it updated each time step
    #(the update function will be passed a dictionary:
    #events:list of events that happened this time step
    #groups:dictionary of groups that exist
    updated=util.Group()

    #add your group to this dictionary to have it be seen by all sprites
    groups={"rendered":rendered, "updated":updated, "vital":vital}
    groups.update(_groups)
    for sprite in args:
        rendered.add(sprite)
        updated.add(sprite)
    run=1
    while run:
        events=pygame.event.get()
        for event in events:
            #quickly check if we got a QUIT event
            if event.type==pygame.QUIT:
                return
        if vitalneeded:
            for vitalg in vital:
                if len(vitalg.sprites())<1:
                    return
        #OK, send the events to the "updated" group...
        #(update before rendering so image changes can be seen quicker)
        updated.update({"events":events, "groups":groups})
        #...black out the screen...
        canvas.fill((0,0,0))
        #...and draw the "rendered" group.
        rendered.draw(canvas)
        screen.blit(canvas, [0,0])
        pygame.display.flip()
    
