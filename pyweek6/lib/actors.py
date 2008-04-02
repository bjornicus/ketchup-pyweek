from pyglet import event
from widget import ClickableActor
from actor import Actor
    
class Conveyor(ClickableActor): # should inherit from actors as well so we can call update
    def __init__(self, parent):
        ClickableActor.__init__(self, parent, 'dummy.png', x=0, y=200, width=630, height=80)

    def do_click_action(self,x,y):
        print "clicked the conveyor at (%i,%i) " %(x,y)

class Robot(ClickableActor):
    def __init__(self,parent, imageName):
        ClickableActor.__init__(self, parent, imageName)
    
class Claw(Actor):
    def __init__(self):
        Actor.__init__(self,imageName='dummy.png', x=200,y=400)
    
class PartsBin(ClickableActor):
    def __init__(self,parent,imageName,x,y,width,height):
        ClickableActor.__init__(self, parent, imageName, x, y, width, height)
    
class FinishedBin(ClickableActor):
    def __init__(self,parent): 
        ClickableActor.__init__(self, parent,x=630, y=340, width=150, height=110)

class RandomPartGenerator(Actor):
    def __init__(self):
        Actor.__init__(self,y=370)

class Clock(Actor):
    def __init__(self):
        Actor.__init__(self,x=632,y=450)
