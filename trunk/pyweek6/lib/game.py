from pyglet import event
from pyglet.window import key
#from widget import Widget
from actors import *
import data

class Game(event.EventDispatcher):
    def __init__(self):
        self.actors = []
        self.widgets = self.children = []
        self.claw = Claw('dummy.png')
        self.conveyor = Conveyor(self,'dummy.png')

    def update(self,dt):
        for actor in self.actors:
            actor.update(dt)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_quit')
            return True

    def on_mouse_press(self, x, y, button, modifiers):
        #find out which item was clicked
        for item in self.widgets:
            if item.on_click(x,y):
                return True

Game.register_event_type('on_pause')
Game.register_event_type('on_quit')
