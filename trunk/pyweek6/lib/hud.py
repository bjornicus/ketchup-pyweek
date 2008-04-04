from pyglet import event
from pyglet import image
from actor import Actor
from pyglet import font as pygletfont

class HUD(Actor):
    def __init__(self):
        Actor.__init__(self, imageName = 'dummy.png', y=500)
        
        self.timer = Timer()
        self.actors = []
        
    def initComponents(self):
        self.add_actor(RobotsRequired(self))
        self.add_actor(Money(self))
        self.add_actor(Score(self))
        self.add_actor(Clock(self))
    
    def update(self, dt):
        self.timer.update(dt)
        for actor in self.actors:
            actor.update(dt)
        self.draw()
    
    def add_actor(self, actor):
        actor.push_handlers(self)
        self.actors.append(actor)
        self.dispatch_event('add_actor_for_listening',actor)
    
    def remove_actor(self, actor):
        self.actors.remove(actor)
        
HUD.register_event_type('add_actor_for_listening')

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
        return int(self.remainingTime - (self.getMinutes() * 60))

class RobotsRequired(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=600, y=parent.y + 50)
        
class Clock(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=700, y=parent.y + 50)
        self.font = pygletfont.load('Arial',30)
        self.timer = Timer()
        self.timer.set(1,0,True)
        self.y = 600 - self.font.ascent

        
    def update(self,dt):
        self.timer.update(dt)
        if self.timer.active == False:
            if dt != 0:
                self.dispatch_event('on_level_over')
        text = pygletfont.Text(self.font, "%i:%02i" %(self.timer.getMinutes() ,self.timer.getSeconds()), self.x, self.y)
        text.color = (0,1.0,0,1.0)
        text.draw()
        
    def on_level_begin(self,level):
        self.timer.set(1,0,True)
        
Clock.register_event_type('on_level_over')

class Money(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=600, y=parent.y)

class Score(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=700, y=parent.y)
