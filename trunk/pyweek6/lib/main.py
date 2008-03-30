'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''
import data
from pyglet import window
from pyglet.window.event import WindowEventLogger

win = window.Window(resizable=True)

win.push_handlers(WindowEventLogger())


def main():
    while not win.has_exit:
        win.dispatch_events()
        win.clear()
        win.flip()
