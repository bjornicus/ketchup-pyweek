from pyglet import event
from actor import Actor

class HUD(Actor):
    def __init__(self):
        Actor.__init__(self,y=500)
        self.timer = Timer()
        
    def update(self, dt):
        self.timer.update(dt)
        self.draw()

class Timer(event.EventDispatcher):
    def __init__(self, min=1, sec=0):
        self.setDuration(min, sec)
    
    def update(self, dt):
        self.remainingTime -= dt
        if self.remainingTime <= 0:
            pass # Send "out_of_time" event.
    
    def setDuration(self, min=1, sec=0):
        self.duration = ((min * 60) + sec)
        self.remainingTime = self.duration
    
    def getMinutes(self):
        return self.remainingTime / 60
    
    def getSeconds(self):
        return self.remainingTime - (getMinutes * 60)