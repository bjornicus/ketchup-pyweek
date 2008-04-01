from pyglet import event
from pyglet.window import key
from widget import Widget
#from actors import *

class Game(event.EventDispatcher):
    def __init__(self):
        self.actors = []
        self.widgets = []
        self.widgets.append(Conveyor())
        
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

#this maybe should move to actors.py, but it doesn't exist yet :D
class Conveyor(Widget): # should inherit from actors as well so we can call update
    def __init__(self):
        #find out how big the conveyor is and where it sits then call:
        Widget.__init__(self,0,200,700,100)

    def do_click_action(self,x,y):
        print "clicked the conveyor at (%i,%i) " %(x,y)
