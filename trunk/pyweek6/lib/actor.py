from pyglet import image
from pyglet import event
import data

class DummyImage(object):
    def blit(self,x,y):
        pass

class Actor(event.EventDispatcher):
    ImageDictionary = {"None":[DummyImage()]}
    def __init__(self, imageName = None, x = 0, y = 0, z = 0.2, xframes = 1, yframes = 1):
        if imageName is None:
            imageName = "None"
        if not Actor.ImageDictionary.has_key(imageName):
            myimage = image.load(data.filepath(imageName))
            imageGrid = image.ImageGrid(myimage, yframes, xframes)
            Actor.ImageDictionary[imageName] = image.TextureGrid(imageGrid)
        self.image = Actor.ImageDictionary[imageName]
        self.x = x
        self.y = y
        self.z = z
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
