from pyglet import event
from pyglet import clock
from widget import ClickableActor
from actor import Actor
from pyglet.gl import *
import random
    
FALLSPEED = 500.

class Conveyor(ClickableActor): # should inherit from actors as well so we can call update
    SPEED = 10. #pixels per second
    def __init__(self, parent):
        ClickableActor.__init__(self, parent, 'dummy.png', x=0, y=200, width=730, height=80)

    def create_recycle_bin(self):
        self.recycleBin = RecycleBin()
        self.dispatch_event('add_actor',self.recycleBin)

    def do_click_action(self,x,y):
        print "clicked the conveyor at (%i,%i) " %(x,y)
        ClickableActor.do_click_action(self,x,y)
        
    def update(self,dt):
        ClickableActor.update(self,dt)
        for robot in self.children:
            robot.move(Conveyor.SPEED*dt,0)
            if robot.x > self.width:
                self.recycleBin.attach(robot)
                self.children.remove(robot)

class RecycleBin(Actor):
    def __init__(self):
        Actor.__init__(self,x=730,y=20)
        self.robots = []
    def attach(self, robot):
        self.robots.append(robot)
    def update(self,dt):
        Actor.update(self,dt)
        for robot in self.robots:
            robot.move(0,-FALLSPEED*dt)
            if robot.y < self.y:
                self.robots.remove(robot)
                self.dispatch_event('remove_actor',robot)
    
    
class RobotPart(Actor):
    partlist = {'head':{1:'RedHead1.png', 2:'BlueHead2.png',3:'GreenHead3.png'}, 
                'body':{1:'RedBody1.png', 2:'BlueBody2.png',3:'GreenBody3.png'},
                'legs':{1:'RedFeet1.png', 2:'BlueLegs02.png',3:'GreenLegs3.png'}}
    def __init__(self, type, flavor):
        Actor.__init__(self, RobotPart.partlist[type][flavor])
        self.type = type
        self.flavor = flavor
        
class Robot(ClickableActor):
    def __init__(self,parent,x,y):
        ClickableActor.__init__(self, parent, x=x, y=y, width=64, height=192)
        self.head = None
        self.body = None
        self.legs = None
        self.parts = []
    
    def move(self, dx, dy):
        Actor.move(self,dx,dy)
        for part in self.parts:
            part.move(dx,dy)
    def draw(self): # we don't actually draw the robot, it just holds the parts
        glColor4f(1, 0, 0, .3) # red
        glRectf(self.x, self.y, self.x+self.width, self.y+self.height) 
        glColor4f(1, 1, 1, .5) 
        glColor4f(1, 1, 1, 1) 
        for part in self.parts:
            part.draw()
        
    def attach_part(self,part):
        if (part.type == 'head'):
            if self.head is not None:
                return False
            self.head = part
            part.x = self.x - 32
        if (part.type == 'body'):
            if self.body is not None:
                return False
            self.body = part
            part.x = self.x
        if (part.type == 'legs'):
            if self.legs is not None:
                return False
            self.legs = part
            part.x = self.x
        part.y = self.y
        self.update_stacking()
        self.parts.append(part)
        return True
        
    def do_click_action(self,x,y):
        print "clicked!"
        self.dispatch_event('widget_clicked',self)
        
    def update_stacking(self):
        legheight = bodyheight = headheight = 0
        if self.legs:
            legheight = self.legs.image.height
        if self.body:
            bodyheight = self.body.image.height
            self.body.y = self.y + legheight
        if self.head:
            headheight = self.head.image.height
            self.head.y = self.y + legheight + bodyheight
        self.height = legheight+bodyheight+headheight
        
Robot.register_event_type('widget_clicked')
    
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
        self.currentRobot = None
        clock.schedule_interval(self.make_part, 5.0)
    def make_part(self,dt):
        if self.currentRobot:
            return
        newrobot = Robot(self.targetConveyor, self.x,self.y)
        for i in range(2):
            type = random.choice(('head','body','legs'))
            flavor = random.choice((1,2,3))
            newrobot.attach_part(RobotPart(type,flavor))
        self.dispatch_event('add_actor',newrobot)
        self.currentRobot = newrobot
    def update(self,dt):
        Actor.update(self,dt)
        if self.currentRobot:
            self.currentRobot.move(0,-FALLSPEED*dt)
            if self.currentRobot.y < self.targetConveyor.y + 10:
                self.currentRobot = None
RandomPartGenerator.register_event_type('add_actor')

class Clock(Actor):
    def __init__(self):
        Actor.__init__(self,x=632,y=450)
