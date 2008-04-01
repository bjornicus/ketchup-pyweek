from pyglet import event
from pyglet import image
import data

# Timer duration in seconds.
timerDuration = 5

class Intro(event.EventDispatcher):
    def __init__(self):
        # Reset timer.
        self.timerCurrent = 0

    def update(self,dt):
        self.image.blit(0,0)
        # Check for timer duration.
        if self.timerCurrent > timerDuration:
            self.finish()
        else:
            # Increment timer.
            self.timerCurrent += dt

    def on_key_press(self, symbol, modifiers):
        self.finish()
        return True

    def finish(self):
        self.dispatch_event('on_intro_finish')

Intro.image = image.load(data.filepath('intro.png'))
Intro.register_event_type('on_intro_finish')