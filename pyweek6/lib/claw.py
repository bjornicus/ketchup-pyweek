from pyglet import event
from widget import ClickableActor
from actor import Actor
from actors import Robot


class Claw(Actor):
    def __init__(self, imageName):
        Actor.__init__(self,imageName, 50, 500, 2, 1)
        self.y = self.y - self.image[self.currentFrame].height
        self.tracking = False
        self.holding = False
        self.target = None
        self.heldTarget = None
        self.speed = 60.0
        self.dir = 0
        self.xspeed = 0
        self.yspeed = 0
        self.ydir = 1
        self.xdir = 1
        
    def widget_clicked(self, clickable):
        print "event caught!"
        if self.tracking == False:
            self.tracking = True
            self.target = clickable
        return True
   
    def update(self,dt):
        speed = self.speed * dt
        self.xspeed = 0
        self.yspeed = 0
        self.xdir = 1
        self.ydir = 1
        
        if self.tracking == True:
            self.track(dt)
                
        elif self.y < 500 - self.image[self.currentFrame].height:
            self.returnToTop(dt)
            
        if self.heldTarget != None:
            self.heldTarget.move(self.xspeed, self.yspeed)
            self.heldTarget.update(dt)
            
        self.draw()
        
    def finishTracking(self):
        if isinstance(self.target,Robot):
            self.changeFrame(1)
            self.target.parent.children.remove(self.target)
            self.target.parent = None
            self.heldTarget = self.target
            self.holding = True
            
        self.target = None
        self.tracking = False
        
    def track(self,dt):
        speed = self.speed * dt
        targetHighY = self.target.y + self.target.height
        selfHighY = self.y + self.image[0].height
        
        distance = self.target.x - self.x
        self.xdir = distance/abs(distance)
        self.xspeed = speed * self.xdir
        
        distance = targetHighY - selfHighY
        self.ydir = distance/abs(distance)
        self.yspeed = speed * self.ydir
        
        self.move(self.xspeed,self.yspeed)
        if( abs(self.target.x - self.x) < 0.3 and abs(targetHighY - selfHighY) < 0.3 ):
            self.finishTracking()
            
    def returnToTop(self,dt):
        speed = self.speed * dt
        self.yspeed = speed * self.ydir
        self.move(0,self.yspeed)
        
        
