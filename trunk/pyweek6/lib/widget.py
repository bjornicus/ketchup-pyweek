from actor import Actor
from pyglet.gl import *

class Widget(object):
    def __init__(self,parent,x,y,width,height):
        parent.children.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = []
        
    def on_click(self, x, y):
        if not self.contains_point(x,y):
            return False
        for child in self.children:
            if child.on_click:
                return True
        # the children didn't consume the click so take action
        return self.do_click_action(x,y)
        
    def contains_point(self,x,y):
        if x < self.x or x > self.x+self.width:
            return False
        if y < self.y or y > self.y+self.height:
            return False
        return True

    #override this method in inherited class
    def do_click_action(self,x,y):
        return False

class ClickableActor(Actor, Widget):
    def __init__(self,parent, imageName="dummy.png", x=0, y=0, width=1, height=1, xframes = 1, yframes = 1):
        Widget.__init__(self,parent,x,y,width,height)
        Actor.__init__(self,imageName,x,y,xframes,yframes)
    
    def draw(self):
        glColor4f(1, 0, 0, .3) # red
        glRectf(self.x, self.y, self.x+self.width, self.y+self.height) 
        glColor4f(1, 1, 1, .5) 
        Actor.draw(self)
        glColor4f(1, 1, 1, 1) 
        
    def do_click_action(self,x,y):
        self.dispatch_event('widget_clicked',self)

ClickableActor.register_event_type('widget_clicked')
