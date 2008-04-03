from pyglet import event
from pyglet import image
from actor import Actor

class HUD(Actor):
    def __init__(self, min=1, sec=0):
        Actor.__init__(self, imageName = 'dummy.png', y=500)
        
        self.timer = Timer(min, sec)
        
        self.actors = []
        self.add_actor(RobotsRequired())
        self.add_actor(Clock())
        self.add_actor(Money())
        self.add_actor(Score())
    
    def update(self, dt):
        self.timer.update(dt)
        for actor in self.actors:
            actor.update(dt)
         
        self.draw()
    
    def add_actor(self, actor):
        actor.push_handlers(self)
        self.actors.append(actor)
    
    def remove_actor(self, actor):
        self.actors.remove(actor)

class Timer(event.EventDispatcher):
    def __init__(self, min=1, sec=0):
        self.set(min, sec)
    
    def update(self, dt):
        self.remainingTime -= dt
        if self.remainingTime <= 0:
            pass # Send "out_of_time" event.
    
    def set(self, min=1, sec=0):
        self.duration = (min*60) + sec
        self.remainingTime = self.duration
    
    def getMinutes(self):
        return self.remainingTime / 60
    
    def getSeconds(self):
        return self.remainingTime - (getMinutes * 60)

class RobotsRequired(Actor):
    def __init__(self):
        Actor.__init__(self, x=600, y=550)

class Clock(Actor):
    def __init__(self):
        Actor.__init__(self, x=700, y=550)

class Money(Actor):
    def __init__(self):
        Actor.__init__(self, x=600, y=500)

class Score(Actor):
    def __init__(self):
        Actor.__init__(self, x=700, y=500)
