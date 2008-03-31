from pyglet import event
from pyglet import font as pygletfont
from pyglet.window import key

class Menu(event.EventDispatcher):
    def __init__(self, width, height):
        self.font = pygletfont.load('Arial', 36)
        self.menuItems = []
        self.menuItems.append((pygletfont.Text(self.font,"Start Game"),'on_new_game'))
        self.menuItems.append((pygletfont.Text(self.font,"Resume Game"),'on_resume_game'))
        self.menuItems.append((pygletfont.Text(self.font,"Exit"),'on_exit_program'))
        #maybe the following should be a separate method:
        menuHeight = self.menuItems[0][0].height*(len(self.menuItems))
        topY = height - (height-menuHeight)/2
        for item,action in self.menuItems:
            item.y = topY
            topY -= item.height
            item.x = (width-item.width)/2
    
    def update(self,dt):
        for item, action in self.menuItems:
            item.draw()
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.dispatch_event('on_new_game')
    
    def on_mouse_press(self, x, y, button, modifiers):
        #find out which item was clicked
        for item, action in self.menuItems:
            if item.x < x and item.x+item.width > x and item.y < y and item.y+item.height > y:
                self.dispatch_event(action)
                return True

Menu.register_event_type('on_new_game')
Menu.register_event_type('on_resume_game')
Menu.register_event_type('on_exit_program')
