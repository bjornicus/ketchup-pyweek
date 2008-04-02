from pyglet import event
from widget import ClickableActor
from actor import Actor
    
class Conveyor(ClickableActor): # should inherit from actors as well so we can call update
    def __init__(self, parent):
        ClickableActor.__init__(self, parent, 'dummy.png', x=0, y=170, width=630, height=85)

    def do_click_action(self,x,y):
        print "clicked the conveyor at (%i,%i) " %(x,y)

class Robot(ClickableActor):
    def __init__(self,parent, imageName):
        ClickableActor.__init__(self, parent, imageName)
    
class Claw(Actor):
    def __init__(self, imageName):
        Actor.__init__(self,imageName)
    
class PartsBin(ClickableActor):
    def __init__(self,parent, imageName):
        ClickableActor.__init__(self, parent, imageName)
    
class FinishedBin(ClickableActor):
    def __init__(self,parent, imageName): 
        ClickableActor.__init__(self, parent, imageName)

class Clock(Actor):
    def __init__(self, imageName):
        Actor.__init__(self,imageName)
