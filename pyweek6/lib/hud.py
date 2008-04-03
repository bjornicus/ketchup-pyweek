from pyglet import event
from pyglet import image
from actor import Actor

class HUD(Actor):
    def __init__(self):
        Actor.__init__(self, imageName = 'dummy.png', y=500)
        
        self.timer = Timer()
        
        self.actors = []
        self.add_actor(RobotsRequired(self))
        self.add_actor(Clock(self))
        self.add_actor(Money(self))
        self.add_actor(Score(self))
    
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
    def __init__(self):
        self.set(0, 58, True)
    
    def update(self, dt):
        if self.active:
            self.remainingTime -= dt
            if self.remainingTime <= 0:
                self.active = False
                # Send "out_of_time" event.
                print "Timer expired."
    
    def set(self, min=1, sec=0, active = False):
        self.duration = ((min*60) + sec)
        self.remainingTime = self.duration
        self.active = active
    
    def getMinutes(self):
        return int(self.remainingTime / 60)
    
    def getSeconds(self):
        return self.remainingTime - (self.getMinutes() * 60)

class RobotsRequired(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=600, y=parent.y + 50)

class Clock(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=700, y=parent.y + 50)

class Money(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=600, y=parent.y)

class Score(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=700, y=parent.y)
