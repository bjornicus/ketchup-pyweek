from pyglet import event
from pyglet import clock
from widget import ClickableActor
from actor import Actor
from pyglet.gl import *
    
class Conveyor(ClickableActor): # should inherit from actors as well so we can call update
    def __init__(self, parent):
        ClickableActor.__init__(self, parent, 'dummy.png', x=0, y=200, width=630, height=80)

    def do_click_action(self,x,y):
        print "clicked the conveyor at (%i,%i) " %(x,y)
        ClickableActor.do_click_action(self,x,y)

class RobotPart(Actor):
    partlist = {'head':{1:'RedHead1.png', 2:'BlueHead2.png',3:'GreenHead3.png'}, 
                'body':{1:'RedBody1.png', 2:'BlueBody2.png',3:'GreenBody3.png'},
                'feet':{1:'RedLegs1.png', 2:'BlueLegs2.png',3:'GreenLegs3.png'}}
    def __init__(self, type, flavor):
        Actor.__init__(self, RobotPart.partlist[type][flavor])
        self.type = type
        self.flavor = flavor
        
class Robot(ClickableActor):
    def __init__(self,parent,x,y):
        ClickableActor.__init__(self, parent, x=x, y=y, width=64, height=192)
        self.head = None
        self.body = None
        self.feet = None
        
    def draw(self): # we don't actually draw the robot, it just holds the parts
        glColor4f(1, 0, 0, .3) # red
        glRectf(self.x, self.y, self.x+self.width, self.y+self.height) 
        glColor4f(1, 1, 1, .5) 
        glColor4f(1, 1, 1, 1) 
        if self.head:
            self.head.draw()
        if self.body:
            self.body.draw()
        if self.feet:
            self.feet.draw()
        
    def attach_part(self,part):
        if (part.type == 'head'):
            if self.head is not None:
                return False
            self.head = part
            part.y = self.y + 128
            part.x = self.x - 32
        if (part.type == 'body'):
            if self.body is not None:
                return False
            self.body = part
            part.y = self.y + 64
            part.x = self.x
        if (part.type == 'feet'):
            if self.feet is not None:
                return False
            self.feet = part
            part.y = self.y
            part.x = self.x
        return True
    
class PartsBin(ClickableActor):
    def __init__(self,parent,imageName,x,y,width,height):
        ClickableActor.__init__(self, parent, imageName, x, y, width, height)
    
class FinishedBin(ClickableActor):
    def __init__(self,parent): 
        ClickableActor.__init__(self, parent,x=630, y=340, width=150, height=110)

class RandomPartGenerator(Actor):
    def __init__(self, conveyor):
        Actor.__init__(self,y=370)
        self.targetConveyor = conveyor
        clock.schedule_once(self.make_part, 1.0)
    def make_part(self,dt):
        # -- begin test robot -- #
        testRobot = Robot(self.targetConveyor, self.x,self.y)
        testRobot.attach_part(RobotPart('head',1))
        testRobot.attach_part(RobotPart('body',2))
        testRobot.attach_part(RobotPart('feet',3))
        self.dispatch_event('add_actor',testRobot)
        # -- end test robot -- #
RandomPartGenerator.register_event_type('add_actor')

class Clock(Actor):
    def __init__(self):
        Actor.__init__(self,x=632,y=450)
