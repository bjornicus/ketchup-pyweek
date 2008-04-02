from pyglet import event
from widget import Widget

class Actor(event.EventDispatcher):
    def __init__(self):
        pass
        
    def update(self,dt):
        pass
        
    
class Conveyor(Actor, Widget): # should inherit from actors as well so we can call update
    def __init__(self, parent):
        #find out how big the conveyor is and where it sits then call:
        Widget.__init__(self,parent, 0,200,700,100)
        Actor.__init__(self)

    def do_click_action(self,x,y):
        print "clicked the conveyor at (%i,%i) " %(x,y)

class Robot(Actor, Widget):
    pass
    
class Claw(Actor):
    pass
    
class PartsBin(Actor, Widget):
    pass
    
class FinishedRobotShelf(Widget): #this may need a better name
    pass

class Clock(Actor):
    pass
