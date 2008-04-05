from pyglet import event
from pyglet import font as pygletfont
from pyglet.window import key
from widget import Widget

class MenuItem(Widget):
    def __init__(self, parent, drawable, action):
        Widget.__init__(self,parent, drawable.x,drawable.y,drawable.width,drawable.height)
        self.drawable = drawable
        self.action = action

    def draw(self):
        self.drawable.draw()
        
    def do_click_action(self,x,y):
        return True

    def setX(self,x):
        self.x = x
        self.drawable.x = x

    def setY(self,y):
        self.y = y
        self.drawable.y = y

class Menu(event.EventDispatcher):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygletfont.load('Arial', 36)
        self.children = []
        self.menuItems = self.children
        MenuItem(self, pygletfont.Text(self.font,"Start Game"),'on_new_game')
        MenuItem(self, pygletfont.Text(self.font,"Story Mode"),'on_new_story_game')
        MenuItem(self, pygletfont.Text(self.font,"Credits"),'on_credits')
        MenuItem(self, pygletfont.Text(self.font,"Exit"),'on_exit_program')
        #only want 'resume game' showing when there is a game to resume
        self.resume_game_item = MenuItem(self, pygletfont.Text(self.font,"Resume Game"),'on_resume_game')
        self.disable_resume() 
        self.align_menu_items()
        
    def align_menu_items(self):
        menuheight = self.menuItems[0].height*(len(self.menuItems))
        topY = self.height - (self.height-menuheight)/2
        for item in self.menuItems:
            item.setY(topY)
            topY -= item.height
            item.setX((self.width-item.width)/2)
    
    def enable_resume(self):
        if not self.resume_game_item in self.menuItems:
            self.menuItems.insert(1,self.resume_game_item)
            self.align_menu_items()
        
    def disable_resume(self):
        self.menuItems.remove(self.resume_game_item) 
        self.align_menu_items()
    
    def update(self,dt):
        for item in self.menuItems:
            item.draw()
        
    def on_key_press(self, symbol, modifiers):
        pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        #find out which item was clicked
        for item in self.menuItems:
            if item.on_click(x,y):
                self.dispatch_event(item.action)
                return True

Menu.register_event_type('on_new_game')
Menu.register_event_type('on_new_story_game')
Menu.register_event_type('on_resume_game')
Menu.register_event_type('on_exit_program')
Menu.register_event_type('on_credits')
