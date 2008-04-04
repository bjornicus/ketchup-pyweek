from pyglet import event

class Timer(event.EventDispatcher):
    def __init__(self):
        self.set(0, 0, False)
    
    def update(self, dt):
        if self.active:
            self.remainingTime -= dt
            if self.remainingTime <= 0:
                self.active = False
                self.on_expire()
    
    def set(self, min=1, sec=0, active = False):
        self.duration = ((min*60) + sec)
        self.remainingTime = self.duration
        self.active = active
    
    def getMinutes(self):
        return int(self.remainingTime / 60)
    
    def getSeconds(self):
        return int(self.remainingTime - (self.getMinutes() * 60))
    
    def on_expire(self):
        # overload this function for on timer expire event.
        pass
