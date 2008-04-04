from pyglet import event
from pyglet import image
from actor import Actor
from pyglet import font as pygletfont
from timer import Timer

class HUD(Actor):
    def __init__(self):
        Actor.__init__(self, imageName = 'dummy.png', y=500)
        self.actors = []
        
    def initComponents(self):
        self.add_actor(RobotsRequired(self))
        self.add_actor(Money(self))
        self.add_actor(Clock(self))
    
    def update(self, dt):
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

class RobotsRequired(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=600, y=parent.y + 50)
        
class Clock(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=700, y=parent.y + 50)
        self.font = pygletfont.load('Arial',30)
        self.timer = Timer()
        self.timer.on_expire = self.on_expire
        self.timer.set(1,0,True)
        self.y = 600 - self.font.ascent
    
    def on_expire(self):
        self.dispatch_event('on_level_over')
        
    def update(self,dt):
        self.timer.update(dt)
        text = pygletfont.Text(self.font, "%i:%02i" %(self.timer.getMinutes() ,self.timer.getSeconds()), self.x, self.y)
        text.color = (0,1.0,0,1.0)
        text.draw()
        
    def on_level_begin(self,level):
        self.timer.set(1,0,True)
        
Clock.register_event_type('on_level_over')

class Money(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=600, y=parent.y)
