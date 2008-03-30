from pyglet import event
from pyglet.window import key

class Game(event.EventDispatcher):
    def __init__(self):
        pass
        
    def update(self,dt):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_quit')
            return True

Game.register_event_type('on_pause')
Game.register_event_type('on_quit')
