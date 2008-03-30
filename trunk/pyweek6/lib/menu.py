from pyglet import event
from pyglet import font as pygletfont
from pyglet.window import key

class Menu(event.EventDispatcher):
    def __init__(self):
        self.font = pygletfont.load('Arial', 36)
        self.text = pygletfont.Text(self.font, 
            "Main Menu:\n Enter to start game\n Esc to exit",
            x = 40, y= 400)
    
    def update(self,dt):
        self.text.draw()
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.dispatch_event('on_new_game')

Menu.register_event_type('on_new_game')
Menu.register_event_type('on_resume_game')
