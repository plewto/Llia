# llia.gui.tk.nudge
# A NudgeTool is a button which increments/decrements (or scales)
# a synth control.

import abc



class NudgeTool(object):

    WIDTH = 16
    HEIGHT = 16
    MARGIN = 3
    active_color = 'yellow'
    
    
    def __init__(self, canvas, client, editor, value):
        super(NudgeTool, self).__init__()
        self.canvas = canvas
        self.client = client
        self.editor = editor
        self.value = value

    @abc.abstractmethod
    def nudge(self, event):
        pass

    @abc.abstractmethod
    def render(self, offset=(0,0), fill='black', outline='blue'):
        pass

    @abc.abstractmethod
    def enter_callback(self, *_):
        pass

    def leave_callback(self, *_):
        self.status('')

    @abc.abstractmethod
    def update_callback(self, *_):
        pass
        
    def status(self, msg):
        self.editor.status(msg)
    
    

class IncrementNudgeTool(NudgeTool):

    def __init___(self, canvas, client, editor, value):
        super(IncrementNudgeTool, self).__init__(canvas,client,editor,value)

    def nudge(self, event):
        v0 = self.client.value()
        v1 = v0 + self.value
        return self.client.value(v1)

    def enter_callback(self, *_):
        param = self.client.param
        msg = 'Increment/Decrement %s by %s' % (param, self.value)
        self.status(msg)

    def update_callback(self, *_):
        v0 = self.client.value()
        v1 = v0 + self.value
        param = self.client.param
        self.status("[%s] = %s" % (param, v1))
        return self.client.value(v1)
        
    def render(self, offset=(0,0), fill='black', outline='blue'):
        x0,y0 = offset
        x1,y1 = x0+self.WIDTH, y0+self.HEIGHT
        xc,yc = (x0+x1)/2,(y0+y1)/2
        canvas = self.canvas
        r = canvas.create_rectangle(x0,y0,x1,y1,
                                    fill = fill,
                                    outline = outline,
                                    activeoutline = self.active_color)
        xa,xb = x0+self.MARGIN, x1-self.MARGIN
        if self.value > 0:
            ya,yb = y1-self.MARGIN, y0+self.MARGIN
        else:
            yb,ya = y1-self.MARGIN, y0+self.MARGIN

        chevron = canvas.create_polygon([xa,ya,xc,yb,xb,ya],
                                        fill = '',
                                        outline = outline,
                                        activeoutline = self.active_color)
        for citem in (r,chevron):
            self.canvas.tag_bind(citem,"<Enter>",self.enter_callback)
            self.canvas.tag_bind(citem,"<Leave>",self.leave_callback)
            self.canvas.tag_bind(citem,"<Button-1>",self.update_callback)
            
                                 
        
                                    
    
        

    

        
   
        
        
