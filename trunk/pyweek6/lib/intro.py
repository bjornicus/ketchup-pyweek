from pyglet import event
from pyglet import image
from actor import Actor
import data


class Intro(event.EventDispatcher):
    # Timer duration in seconds.
    timerDuration = 5
    background = image.load(data.filepath('intro.png'))
    def __init__(self):
        # Reset timer.
        self.timerCurrent = 0

    def update(self,dt):
        Intro.background.blit(0,0)
        # Check for timer duration.
        if self.timerCurrent > self.timerDuration:
            self.finish()
        else:
            # Increment timer.
            self.timerCurrent += dt

    def on_key_press(self, symbol, modifiers):
        self.finish()
        return True

    def on_mouse_press(self, x, y, button, modifiers):
        self.finish()
        return True

    def finish(self):
        self.dispatch_event('on_intro_finish')

Intro.register_event_type('on_intro_finish')
