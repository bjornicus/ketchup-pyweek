from pyglet import event
from actor import Actor
from pyglet import font as pygletfont
from pyglet.window import key
from timer import Timer
import data

class Story(event.EventDispatcher):
    def __init__(self):
        self.stages = []
        self.stages.append(Actor("story01.png"))
        self.stages.append(Actor("story02.png"))
        self.stages.append(Actor("story03.png"))
        self.stages.append(Actor("story04.png"))
        self.currentStage = 0
        self.timer = Timer()
        self.timer.set(0,5,True)
    
    def update(self,dt):
        self.timer.update(dt)
        if self.timer.active == False:
            self.nextStage()
            
        if self.currentStage >= len(self.stages):
            self.finish()
        else:
            self.stages[self.currentStage].update(dt)
            
    def on_key_press(self, symbol, modifiers):
        self.nextStage()
        return True

    def on_mouse_press(self, x, y, button, modifiers):
        self.nextStage()
        return True

    def finish(self):
        self.dispatch_event('on_new_game')
        
    def nextStage(self):
        self.currentStage += 1
        self.timer.set(0,5,True)
        

Story.register_event_type('on_new_game')
        
