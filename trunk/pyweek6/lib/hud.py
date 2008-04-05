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
        self.robotsordered = RobotsOrdered(self)
        self.money = Money(self)
        self.clock = Clock(self)
        self.add_actor(self.robotsordered)
        self.add_actor(self.money)
        self.add_actor(self.clock)
    
    def update(self, dt):
        self.draw()
        for actor in self.actors:
            actor.update(dt)
    
    def add_actor(self, actor):
        actor.push_handlers(self)
        self.actors.append(actor)
        self.dispatch_event('add_actor_for_listening',actor)
    
    def remove_actor(self, actor):
        self.actors.remove(actor)
        
HUD.register_event_type('add_actor_for_listening')

class RobotsOrdered(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=200, y=parent.y)
        self.font = pygletfont.load('Arial',30)
        self.remaining = 0
        self.ordered = 0
        self.y = 600 - self.font.ascent
    
    def update(self, dt):
        text = pygletfont.Text(self.font, "R %i" %(self.remaining), self.x, self.y)
        text.color = (0,1.0,0,1.0)
        text.draw()
    
    def set(self, amount):
        self.ordered = int(amount)
        self.remaining = self.ordered
    
    def decrease(self, amount = 1):
        if self.remaining >= 1:
            self.remaining -= amount
        
        if self.remaining < 0:
            self.remaining = 0

class Clock(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=10, y=parent.y)
        self.font = pygletfont.load('Arial',30)
        self.timer = Timer()
        self.timer.on_expire = self.on_expire
        self.y = 600 - self.font.ascent
    
    def on_expire(self):
        self.dispatch_event('on_level_over')
        
    def update(self,dt):
        self.timer.update(dt)
        text = pygletfont.Text(self.font, "T %i:%02i" %(self.timer.getMinutes() ,self.timer.getSeconds()), self.x, self.y)
        if self.timer.remainingTime > 30:
            text.color = (0,1.0,0,1.0)
        else:
            text.color = (1.0,0,0,1.0)
        text.draw()
        
    def on_level_begin(self,level):
        self.timer.set(0,self.timer.duration,True)
        
Clock.register_event_type('on_level_over')

class Money(Actor):
    def __init__(self, parent):
        Actor.__init__(self, x=10, y=parent.y)
        self.font = pygletfont.load('Arial',30)
        self.set()
        self.y=590 - (self.font.ascent*2)
    
    def update(self, dt):
        text = pygletfont.Text(self.font, "$ %i" %(self.balance), self.x, self.y)
        if self.balance > 0:
            text.color = (0,1.0,0,1.0)
        elif self.balance == 0:
            text.color = (1.0,1.0,0,1.0)
        else:
            text.color = (1.0,0,0,1.0)
        text.draw()
    
    def set(self, amount = 0):
        self.balance = amount
    
    def withdraw(self, amount = 1):
        self.balance -= int(amount)
    
    def deposit(self, amount = 1):
        self.balance += int(amount)