from pyglet import event
from pyglet import clock
from widget import ClickableActor
from actor import Actor
from pyglet.gl import *
import random
    
FALLSPEED = 500.

class Conveyor(ClickableActor): # should inherit from actors as well so we can call update
    SPEED = 30. #pixels per second
    def __init__(self, parent):
        ClickableActor.__init__(self, parent, 'dummy.png', x=0, y=200, z=-0.1, width=730, height=80)

    def do_click_action(self,x,y):
        print "clicked the conveyor at (%i,%i) " %(x,y)
        ClickableActor.do_click_action(self,x,y)
        
    def update(self,dt):
        ClickableActor.update(self,dt)
        for robot in self.children:
            robot.move(Conveyor.SPEED*dt,0)
            if robot.x > self.width:
                self.dispatch_event('on_recycle_robot',robot)
                self.children.remove(robot)
Conveyor.register_event_type('on_recycle_robot')

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
        self.draw_bounding_box()
        for part in self.parts:
            part.draw()
            
    def connect(self,other): #fit two robots together
        if self.head and other.head or self.body and other.body or self.legs and other.legs:
            return False
        for part in other.parts:
            self.attach_part(part)
        return True

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
    def __init__(self,parent,type,x,y,width,height):
        ClickableActor.__init__(self, parent, 'dummy.png', x, y, width, height)
        self.type = type
        self.children.append(PartsButton(self,1,x,y+height-PartsButton.HEIGHT))
        self.children.append(PartsButton(self,2,x+PartsButton.WIDTH,y+height-PartsButton.HEIGHT))
        self.children.append(PartsButton(self,3,x+PartsButton.WIDTH*2,y+height-PartsButton.HEIGHT))
        self.buttons = self.children[:] # make a copy of this list for update function
        for button in self.buttons:
            button.push_handlers(self)
        self.currentRobot = None

    def widget_clicked(self,button):
        newrobot = Robot(self, self.x,self.y)
        newrobot.attach_part(RobotPart(self.type,button.flavor))
        if self.currentRobot:
            self.children.remove(self.currentRobot)
            self.dispatch_event('remove_actor',self.currentRobot)
        self.currentRobot = newrobot
        self.dispatch_event('add_actor',newrobot)
        return True
    def detatch(self,other):
        if self.currentRobot == other:
            self.currentRobot = None
        ClickableActor.detatch(self,other)
    def update(self,dt):
        ClickableActor.update(self,dt)
        for button in self.buttons:
            button.update(dt)
    def do_click_action(self,x,y):
        return False
    
class PartsButton(ClickableActor):
    HEIGHT = 40
    WIDTH = 60
    def __init__(self,parent,flavor,x,y):
        ClickableActor.__init__(self, parent, 'dummy.png', x, y, PartsButton.WIDTH, PartsButton.HEIGHT)
        self.flavor = flavor
class FinishedBin(ClickableActor):
    class Order(object):
        def __init__(self,headflavor,bodyflavor,legflavor):
            self.headflavor = headflavor
            self.bodyflavor = bodyflavor
            self.legflavor = legflavor
    def __init__(self,parent, numOrders = 1): 
        ClickableActor.__init__(self, parent,x=630, y=340, width=150, height=110)
        self.orderlist = []
        for x in range(numOrders):
            self.generate_new_order()
    def attach(self,robot):
        for order in self.orderlist:
            if robot.head.flavor == order.headflavor and robot.body.flavor == order.bodyflavor and robot.legs.flavor == order.legflavor:
                self.dispatch_event('on_robot_shiped',robot)
                self.orderlist.remove(order)
                self.generate_new_order()
                return True
        self.dispatch_event('on_robot_rejected',robot)
    def generate_new_order(self):
        newOrder = FinishedBin.Order(random.randint(1,3),random.randint(1,3),random.randint(1,3))
        print "head: %d\nBody: %d\nLegs: %d\n"%(newOrder.headflavor,newOrder.bodyflavor,newOrder.legflavor) 
        self.orderlist.append(newOrder)
        
FinishedBin.register_event_type('on_robot_shiped')
FinishedBin.register_event_type('on_robot_rejected')

class RandomPartGenerator(Actor):
    def __init__(self, conveyor):
        Actor.__init__(self,y=370)
        self.targetConveyor = conveyor
        self.currentRobot = None
        clock.schedule_once(self.make_part,0.1)
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
