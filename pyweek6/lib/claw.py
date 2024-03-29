from pyglet import event
from widget import ClickableActor
from actor import Actor
from actors import Robot, Conveyor, RecycleBin
from actors import FinishedBin


class Claw(Actor):
    def __init__(self, imageName):
        Actor.__init__(self,imageName, 50, 500, 0.9, 2, 1)
        self.y = self.y - self.image[self.currentFrame].height
        self.tracking = False
        self.holding = False
        self.target = None
        self.heldTarget = None
        self.speed = 150.0
        self.dir = 0
        self.xspeed = 0
        self.yspeed = 0
        self.ydir = 1
        self.xdir = 1
        
    def widget_clicked(self, clickable):
        if not self.heldTarget and not isinstance(clickable, Robot):
            return False
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
            if isinstance(self.target.parent, RecycleBin):
                print "recycled!"
                self.target = None
                self.tracking = False
                self.returnToTop(dt)
            else:
                self.track(dt)
                
        elif self.y < 500 - self.image[self.currentFrame].height:
            self.returnToTop(dt)
            
        if self.heldTarget != None:
            self.heldTarget.move(self.xspeed, self.yspeed)
            
        #perform correction to get the claw into the right position
        if self.y > 500 - self.image[self.currentFrame].height:
            self.yspeed = 500 - self.image[self.currentFrame].height - self.y
            self.move(0,self.yspeed)
            if self.heldTarget:
                self.heldTarget.move(0, self.yspeed)
            
        self.draw()
        
    def finishTracking(self):
        if isinstance(self.target,Robot):
            if self.heldTarget == None: #grab the robot
                self.changeFrame(1)
                self.target.parent.detatch(self.target)
                self.target.parent = None
                self.heldTarget = self.target
                self.heldTarget.z=0.1 #draw above conveyor robots
                self.holding = True
            elif self.target.connect(self.heldTarget): #try to connect these robots together
                self.heldTarget.dispatch_event('remove_actor',self.heldTarget)
                self.heldTarget = None
                self.changeFrame(0)
        elif self.heldTarget: #lets set down the robot
            if self.target.attach(self.heldTarget):
                self.heldTarget.z=0 #default for conveyor belt robots
                self.heldTarget = None
                self.changeFrame(0)
        
        self.target = None
        self.tracking = False
        
    def track(self,dt):
        speed = self.speed * dt
        targetHighY = self.target.centerY() + self.target.height/2
        targetX = self.target.centerX()
        myCenterX = self.x +self.image[self.currentFrame].width/2
        if self.heldTarget != None:
            targetHighY += 25
        selfHighY = self.y + (self.image[0].height / 2)
        
        distance = targetX - myCenterX
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
        #small hack to get the new claw to drop off stuff at the finished bin
        maxYdiff = 2
        if isinstance(self.target,FinishedBin):
            maxYdiff = 64
        if( abs(targetX - myCenterX) < 2 and abs(targetHighY - selfHighY) < maxYdiff ):
            self.finishTracking()
            
    def returnToTop(self,dt):
        speed = self.speed * dt
        self.yspeed = speed * self.ydir * 2
        self.move(0,self.yspeed)
        
        
