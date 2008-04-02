from pyglet import event
from pyglet.window import key
from pyglet import image
from actors import *
from claw import Claw
import data
"""
at the start of the game we need (as for as actors): 
a clock,
a conveyor, 
a claw, 
3 parts bins, 
a random part generator, 
and a finished robot bin.

Clickables are:
the conveyor, 
parts bins, 
and finish shelf
"""
class Game(event.EventDispatcher):
    def __init__(self):
        self.actors = []
        self.widgets = self.children = []
        self.background = image.load(data.filepath("Env09.png"))
        self.claw = Claw('claw.png')
        self.add_actor(self.claw)
        self.add_actor(Conveyor(self))
        self.add_actor(PartsBin(self,'dummy.png',32,22,188,60)) #for heads
        self.add_actor(PartsBin(self,'dummy.png',240,22,188,60)) #for torsos 
        self.add_actor(PartsBin(self,'dummy.png',444,22,188,60)) #for legs
        self.add_actor(RandomPartGenerator())
        self.add_actor(FinishedBin(self))
        self.add_actor(Clock())

    def update(self,dt):
        self.background.blit(0,0)
        for actor in self.actors:
            actor.update(dt)

    def add_actor(self, actor):
        actor.push_handlers(self)
        self.actors.append(actor)
    
    def remove_actor(self, actor):
        actors.remove(actor)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_quit')
            return True

    def on_mouse_press(self, x, y, button, modifiers):
        #find out which item was clicked
        print "click (%i,%i)" %(x,y)
        for item in self.widgets:
            if item.on_click(x,y):
                return True

Game.register_event_type('on_pause')
Game.register_event_type('on_quit')
