
class Widget(object):
    def __init__(self,x,y,width,height):
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
