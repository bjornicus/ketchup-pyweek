from pyglet import event
from widget import Widget
from actor import Actor
    
class Conveyor(Actor, Widget): # should inherit from actors as well so we can call update
    def __init__(self, parent, imageName):
        #find out how big the conveyor is and where it sits then call:
        Widget.__init__(self,parent, 0,200,700,100)
        Actor.__init__(self, imageName, x=0, y=172)

    def do_click_action(self,x,y):
        print "clicked the conveyor at (%i,%i) " %(x,y)

class Robot(Actor, Widget):
    def __init__(self,parent, imageName):
        Actor.__init__(self,imageName)
        Widget.__init__(self,parent)
    
class Claw(Actor):
    def __init__(self, imageName):
        Actor.__init__(self,imageName)
    
class PartsBin(Actor, Widget):
    def __init__(self,parent, imageName):
        Actor.__init__(self,imageName)
        Widget.__init__(self,parent)
    
class FinishedBin(Actor, Widget):
    def __init__(self,parent, imageName): 
        Actor.__init__(self,imageName)
        Widget.__init__(self,parent)

class Clock(Actor):
    def __init__(self, imageName):
        Actor.__init__(self,imageName)
