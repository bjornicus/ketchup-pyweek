from pyglet import event
from pyglet import clock
from pyglet import image
from widget import ClickableActor
from actor import Actor
from timer import Timer
from pyglet.gl import *
import random
    
FALLSPEED = 500.
ORDER_IMAGE_WIDTH = 48

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
                
    def clearRobots(self):
        #is there an easier way to clear a list?
        while len(self.children) > 0:
            robot = self.children.pop()
            robot.move(0,-800)
            self.dispatch_event('on_recycle_robot',robot)
Conveyor.register_event_type('on_recycle_robot')

class RecycleBin(Actor):
    def __init__(self):
        Actor.__init__(self,imageName = 'recycleBin01.png',x=696,y=1)
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
        self.children.append(PartsButton(self,type,1,x,y+height-PartsButton.HEIGHT))
        self.children.append(PartsButton(self,type,2,x+PartsButton.WIDTH,y+height-PartsButton.HEIGHT))
        self.children.append(PartsButton(self,type,3,x+PartsButton.WIDTH*2,y+height-PartsButton.HEIGHT))
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
        self.dispatch_event('on_parts_ordered')
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
PartsBin.register_event_type('on_parts_ordered')

class PartsButton(ClickableActor):
    HEIGHT = 40
    WIDTH = 60
    buttonImages = {'head':{1:'RedHeadIdle.png', 2:'BlueHeadIdle.png',3:'GreenHeadIdle.png'}, 
                'body':{1:'RedBodyIdle.png', 2:'BlueBodyIdle.png',3:'GreenBodyIdle.png'},
                'legs':{1:'RedLegsIdle.png', 2:'BlueLegsIdle.png',3:'GreenLegsIdle.png'}}
    def __init__(self,parent,type, flavor,x,y):
        imageName = PartsButton.buttonImages[type][flavor] #change this later
        ClickableActor.__init__(self, parent, imageName, x, y, 0, PartsButton.WIDTH, PartsButton.HEIGHT, xframes = 1, yframes = 1)
        self.flavor = flavor
        self.mouseOver = False
        self.prevMouseX = 0
        self.prevMouseY = 0
        
    def do_mouseOver_action(self, x,y,dx,dy):
        return False
        

class FinishedBin(ClickableActor):
    class Order(object):
        def __init__(self,headflavor,bodyflavor,legflavor):
            self.headflavor = headflavor
            self.bodyflavor = bodyflavor
            self.legflavor = legflavor
            self.image = image.create(32,96)
            # there are better ways, but this hack should do the job:
            self.head = Actor(RobotPart.partlist['head'][headflavor])
            self.body = Actor(RobotPart.partlist['body'][bodyflavor])
            self.legs = Actor(RobotPart.partlist['legs'][legflavor])
        def draw(self,x,y):
            self.legs.image[0].blit(x,y,width=ORDER_IMAGE_WIDTH,height=32)
            self.body.image[0].blit(x,y+32,width=ORDER_IMAGE_WIDTH,height=32)
            self.head.image[0].blit(x,y+64,width=ORDER_IMAGE_WIDTH,height=32)
            
    def __init__(self,parent): 
        ClickableActor.__init__(self, parent,x=630, y=340, z=0.5, width=150, height=110)
        self.orderlist = []
        self.shippingRobots = []
    def attach(self,robot):
        if len(robot.parts) != 3:
            self.dispatch_event('on_robot_rejected',robot)
            return True
        for order in self.orderlist:
            if robot.head.flavor == order.headflavor and robot.body.flavor == order.bodyflavor and robot.legs.flavor == order.legflavor:
                self.dispatch_event('on_robot_shipped',robot)
                self.orderlist.remove(order)
                #replace the robot with a tiny, temporary effect
                ta = TimedActor(0,2,'Explode.png')
                ta.x = robot.x + (abs(robot.width-ta.image[0].width)/2)
                ta.y = robot.y + (abs(robot.height-ta.image[0].height)/2)
                #remove the robot and and add the flare
                self.dispatch_event('add_actor',ta)
                self.dispatch_event('remove_actor',robot)
                return True
        self.dispatch_event('on_robot_rejected',robot)
        return True
    def generate_new_order(self,numOrders):
        for x in range(numOrders):
            newOrder = FinishedBin.Order(random.randint(1,3),random.randint(1,3),random.randint(1,3))
            print "head: %d\nBody: %d\nLegs: %d\n"%(newOrder.headflavor,newOrder.bodyflavor,newOrder.legflavor) 
            self.orderlist.append(newOrder)
    def update(self,dt):
        Actor.update(self,dt)
        for i in range(len(self.orderlist)):
            self.orderlist[i].draw((i*ORDER_IMAGE_WIDTH)+304,500)
                
FinishedBin.register_event_type('on_robot_shipped')
FinishedBin.register_event_type('on_robot_rejected')

class RandomPartGenerator(Actor):
    def __init__(self, conveyor):
        Actor.__init__(self,imageName = 'generator01.png',y=371)
        self.targetConveyor = conveyor
        self.currentRobot = None
        clock.schedule_once(self.make_part,0.1)
        clock.schedule_interval(self.make_part, 5.0)
    def make_part(self,dt):
        if self.currentRobot:
            return
        newrobot = Robot(self.targetConveyor, self.x,self.y)
        for i in range(1):
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


class TimedActor(Actor):
    def __init__(self, mins, secs, imageName = 'dummy.png', x = 0, y = 0, z = 0.2, xframes = 1, yframes = 1):
        Actor.__init__(self,imageName,x,y,z,xframes,yframes)
        self.timer = Timer()
        self.timer.set(mins,secs,True)
        
    def update(self,dt):
        self.timer.update(dt)
        if self.timer.active == True:
            self.draw()
        else:
            self.dispatch_event('remove_actor',self)
            
TimedActor.register_event_type('remove_actor')
