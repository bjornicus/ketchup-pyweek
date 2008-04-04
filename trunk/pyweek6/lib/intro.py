from pyglet import event
from pyglet import image
from actor import Actor
from timer import Timer
import data


class Intro(event.EventDispatcher):
    background = image.load(data.filepath('intro.png'))
    def __init__(self):
        self.timer = Timer()
        self.timer.expire = self.finish
        self.timer.set(0,5,True)

    def update(self,dt):
        Intro.background.blit(0,0)
        self.timer.update(dt)

    def on_key_press(self, symbol, modifiers):
        self.finish()
        return True

    def on_mouse_press(self, x, y, button, modifiers):
        self.finish()
        return True

    def finish(self):
        self.dispatch_event('on_intro_finish')

Intro.register_event_type('on_intro_finish')
