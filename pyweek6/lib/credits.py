from pyglet import event
from pyglet import font as pygletfont
from pyglet.window import key
import data
import fileinput

text_speed = 30.0
text_size = 36
text_offset = 40

class Credits(event.EventDispatcher):
    def __init__(self):
        self.font = pygletfont.load('Arial', text_size)
        
        #load the credits file
        self.textList = list()
        sx = 250
        sy = -text_size
        for line in fileinput.input(data.filepath("credits.txt")):
            self.textList.append(pygletfont.Text(self.font, line, x = 800 / 2, y = sy, halign = pygletfont.Text.CENTER))
            sy -= text_offset
        
    def update(self,dt):
        for text in self.textList:
            text.y += text_speed * dt
            text.draw()
            if text.y > 600:
                self.creditsFinished = True
            else:
                self.creditsFinished = False
        if self.creditsFinished == True:
            self.dispatch_event('on_intro_finish')
            
    def centerText(self, size):
        return (800-(size*18))/2
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_intro_finish')
            return True
            
Credits.register_event_type("on_intro_finish")
