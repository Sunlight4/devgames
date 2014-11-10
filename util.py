from __future__ import division
import pygame, sys
from vector import Vector
class Group(pygame.sprite.Group):pass
class Sprite(pygame.sprite.Sprite):
    kill_on_contact_objs=None
    def check_object(self, group, relpos):
        #checks whether a specified object is at a specified relative position
        #relpos should be a vector, group should be a util.Group
        self.rect.move(relpos.x, relpos.y)
        result=False
        if len(pygame.sprite.spritecollide(self, group, False))>0:
            result=True
        self.rect.move(-relpos.x, -relpos.y)
        return result
    def hide(self, dictionary):
        #pass the dictionary you get each time the update function is called
        #makes the object invisible
        self.remove(dictionary["groups"]["rendered"])
    def show(self, dictionary):
        #pass the dictionary you get each time the update function is called
        #makes the object visible
        self.add(dictionary["groups"]["rendered"])
    def pos(self):
        #returns a Vector of this object's current position
        return Vector(self.rect.x, self.rect.y)
    def update(self, dictionary):
        super(Sprite, self).update(dictionary)
        if self.kill_on_contact_objs!=None:
            if self.check_object(self.kill_on_contact_objs, Vector(0,0)):
                self.kill()
    def killoncontact(self, *sprites):
        if self.kill_on_contact_objs==None:self.kill_on_contact_objs=Group()
        self.kill_on_contact_objs.add(*sprites)
            
        
        
#inherit from this class for physics(recommended)
class PhysicsObject(Sprite):
    def __init__(self, maxSpeed, maxForce, *args, **kw):
        super(PhysicsObject, self).__init__(*args, **kw)
        self.v=Vector(0,0)
        self.forces=[]
        self.maxSpeed=maxSpeed
        self.maxForce=maxForce
        if self.maxForce<=0:self.maxForce=2
    def update(self, dictionary):
        super(PhysicsObject, self).update(dictionary)
        if self.forces:
            netxforce=sum([f.x for f in self.forces])
            netyforce=sum([f.y for f in self.forces])
            netforce=Vector(netxforce, netyforce)
            self.v=self.v+netforce
            
        
        self.rect.x+=self.v.x
        self.rect.y+=self.v.y
        self.forces=[]
        
#an object that dies when it runs out of HP
class HPObject(PhysicsObject):
    def __init__(self, hp, *args, **kw):
        super(HPObject, self).__init__(*args, **kw)
        self.hp=hp
    def update(self, dictionary):
        super(HPObject, self).update(dictionary)
        if self.hp<=0:self.kill()
class KeyboardControlledObject(PhysicsObject):
    def update(self, dictionary):
        super(KeyboardControlledObject, self).update(dictionary)
        for event in dictionary["events"]:
            if event.type==pygame.KEYDOWN:
                self.v=Vector(0,0)
                if event.key==pygame.K_UP:
                    self.forces.append(Vector(0, -2))
                elif event.key==pygame.K_DOWN:
                    self.forces.append(Vector(0, 2))
                elif event.key==pygame.K_LEFT:
                    self.forces.append(Vector(-2, 0))
                elif event.key==pygame.K_RIGHT:
                    self.forces.append(Vector(2, 0))
                    
                
        
        
#a simple FSM
class FSM(Sprite):
    states={}
    state=None
    def __init__(self, *args, **kw):
        super(FSM, self).__init__(*args, **kw)
    def update(self, dictionary):
        super(FSM, self).update(dictionary)
        self.states[self.state](dictionary)
class SolidColorBlock(PhysicsObject):
    #Taken from http://www.pygame.org/docs/ref/sprite.html
    #A solid color block. What more needs to be said?
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height, x, y, maxSpeed=2):
       # Call the parent class (Sprite) constructor
       super(SolidColorBlock, self).__init__(maxSpeed)

       # Create an image of the block, and fill it with a color.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x=x
       self.rect.y=y
class SquareBlock(PhysicsObject):
    #Taken from http://www.pygame.org/docs/ref/sprite.html
    #A solid color block. What more needs to be said?
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, side, x, y, maxSpeed=2, maxForce=2):
       # Call the parent class (Sprite) constructor
       super(SquareBlock, self).__init__(maxSpeed, maxForce)

       # Create an image of the block, and fill it with a color.
       self.image = pygame.Surface([side, side])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x=x
       self.rect.y=y



