from pyglet import image
from pyglet import event
import data

class Actor(event.EventDispatcher):
    def __init__(self, imageName, x = 0, y = 0, xframes = 1, yframes = 1):
        myimage = image.load(data.filepath(imageName))
        self.image = image.ImageGrid(myimage, xframes, yframes)
        self.x = x
        self.y = y
        #self.xframes = xframes
        #self.yframes = yframes
        self.currentFrame = 0
        self.frameRange = xframes * yframes
        
    def draw(self):
        self.image[self.currentFrame].blit(self.x,self.y)
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def update(self,dt):
        self.draw()
        
    def changeFrame(self,newFrame):
        if(newFrame < self.frameRange):
            self.currentFrame = newFrame
        
    def destroy(self):
        self.dispatch_event('remove_actor', self)    
        
Actor.register_event_type('remove_actor')
