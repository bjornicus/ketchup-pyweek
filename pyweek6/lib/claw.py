from pyglet import event
from widget import ClickableActor
from actor import Actor


class Claw(Actor):
    def __init__(self, imageName):
        Actor.__init__(self,imageName, 50, 500, 2, 1)
        self.y = self.y - self.image[self.currentFrame].height
        
    def widget_clicked(self, clickable):
        print "event caught!"
        return True
   
    def update(self,dt):
        self.draw()
