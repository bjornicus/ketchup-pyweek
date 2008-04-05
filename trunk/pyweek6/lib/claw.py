from pyglet import event
from widget import ClickableActor
from actor import Actor
from actors import Robot


class Claw(Actor):
    def __init__(self, imageName):
        Actor.__init__(self,imageName, 50, 500, 0.9, 2, 1)
        self.y = self.y - self.image[self.currentFrame].height
        self.tracking = False
        self.holding = False
        self.target = None
        self.heldTarget = None
        self.speed = 200.0
        self.dir = 0
        self.xspeed = 0
        self.yspeed = 0
        self.ydir = 1
        self.xdir = 1
        
    def widget_clicked(self, clickable):
        print "event caught by claw!"
        if not self.heldTarget and not isinstance(clickable, Robot):
            return False
        if self.tracking == False or self.heldTarget == None:
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
            
        self.draw()
        
    def finishTracking(self):
        if isinstance(self.target,Robot):
            if self.heldTarget == None:
                self.changeFrame(1)
                self.target.parent.detatch(self.target)
                self.target.parent = None
                self.heldTarget = self.target
                self.holding = True
            elif self.target.connect(self.heldTarget):
                self.heldTarget.dispatch_event('remove_actor',self.heldTarget)
                self.heldTarget = None
                self.changeFrame(0)
        elif self.heldTarget: #lets set down the robot
            self.target.attach(self.heldTarget)
            self.heldTarget = None
            self.changeFrame(0)
        
        self.target = None
        self.tracking = False
        
    def track(self,dt):
        speed = self.speed * dt
        targetHighY = self.target.y + self.target.height
        if self.heldTarget != None:
            targetHighY += 25
        selfHighY = self.y + self.image[0].height
        
        distance = self.target.x - self.x
        if distance == 0:
            self.xdir = 0
        else:
            self.xdir = distance/abs(distance)
        self.xspeed = min(speed,abs(distance)) * self.xdir
        
        distance = targetHighY - selfHighY
        if distance == 0:
            self.ydir = 0
        else:
            self.ydir = distance/abs(distance)
        self.yspeed = min(speed,abs(distance)) * self.ydir
        
        self.move(self.xspeed,self.yspeed)
        if( abs(self.target.x - self.x) < 1 and abs(targetHighY - selfHighY) < 1 ):
            self.finishTracking()
            
    def returnToTop(self,dt):
        speed = self.speed * dt
        self.yspeed = speed * self.ydir
        self.move(0,self.yspeed)
        
        
