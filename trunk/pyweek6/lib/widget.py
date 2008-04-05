from actor import Actor
from pyglet.gl import *

class Widget(object):
    def __init__(self,parent,x,y,width,height):
        if parent:
            parent.children.append(self)
            self.parent = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = []
        self.frame = 1
        
    def on_click(self, x, y):
        # sometimes children are not within the bounds of the parent (i.e. on the conveyor)
        for child in self.children:
            if child.on_click(x,y):
                return True
        if not self.contains_point(x,y):
            return False
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
        
    #code for detecting and responding to mouse overs
    def on_move(self, x, y, dx, dy):
        # sometimes children are not within the bounds of the parent (i.e. on the conveyor)
        for child in self.children:
            if child.on_move(x,y,dx,dy):
                return True
        if not self.contains_point(x,y):
            self.mouseOver = False
            return False
        # the children didn't consume the click so take action
        return self.do_mouseOver_action(x,y,dx,dy)
        
    #override this
    def do_mouseOver_action(self, x,y,dx,dy):
        self.mouseOver = True
        return False

class ClickableActor(Actor, Widget):
    def __init__(self,parent, imageName=None, x=0, y=0, z=0, width=1, height=1, xframes = 1, yframes = 1):
        Widget.__init__(self,parent,x,y,width,height)
        Actor.__init__(self,imageName,x,y,z,xframes,yframes)
        
    #these are next two are for the claw:
    def centerX(self):
        return self.x + self.width/2
    def centerY(self):
        return self.y + self.height/2
    
    def draw(self):
        #self.draw_bounding_box()
        #glColor4f(1, 1, 1, .5) 
        Actor.draw(self)
        #glColor4f(1, 1, 1, 1) 
    def draw_bounding_box(self):
        glColor4f(1, 0, 0, .3) # red
        glBegin(GL_LINE_STRIP);
        glVertex2f(self.x,self.y);
        glVertex2f(self.x+self.width,self.y);
        glVertex2f(self.x+self.width,self.y+self.height);
        glVertex2f(self.x, self.y+self.height);
        glVertex2f(self.x,self.y);
        glEnd();
        glColor4f(1, 1, 1, 1) 
        
    def do_click_action(self,x,y):
        self.dispatch_event('widget_clicked',self)
        return True
        
    def attach(self,other):
        self.children.append(other)
        other.parent = self
        return True
        
    def detatch(self,other):
        if other in self.children:
            self.children.remove(other)
        
ClickableActor.register_event_type('widget_clicked')
