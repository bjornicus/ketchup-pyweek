'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''
from intro import Intro
from menu import Menu
from game import Game
from pyglet import window
from pyglet import clock
from pyglet import event

win = window.Window(resizable=True)

# this for debugging,
# uncomment if you want to see all events output ot the terminal
#from pyglet.window.event import WindowEventLogger
#win.push_handlers(WindowEventLogger())


def main():
    
    stateManager = StateManager()
    while not win.has_exit:
        win.dispatch_events()
        win.clear()
        dt = clock.tick()
        stateManager.update(dt)
        win.flip()

class StateManager(object):
    def __init__(self):
        self.intro = Intro()
        self.intro.push_handlers(self)
        
        self.menu = Menu()
        self.menu.push_handlers(self)
        
        self.game = Game()
        self.game.push_handlers(self)
        
        self.currentState = self.intro
        win.push_handlers(self.intro)
    
    def update(self, dt):
        self.currentState.update(dt)
        
    def show_menu(self):
        win.pop_handlers()
        self.currentState = self.menu
        win.push_handlers(self.menu)
        
    def on_intro_finish(self):
        self.show_menu()

    def on_new_game(self):
        win.pop_handlers()
        self.currentState = self.game
        win.push_handlers(self.game)
        
    def on_quit(self):
        self.show_menu()
        
    
