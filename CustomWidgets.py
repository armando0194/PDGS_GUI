import Tkinter as tk


class EntryWithPlaceholder(object, tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        
        tk.Entry.__init__(self, master)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()
    
    def put_text(self, text):
        self.delete('0', 'end')
        self.insert(0, text)
        self['fg'] = self.default_fg_color
        
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

class CircularButton(tk.Canvas):
    def __init__(self, parent, width, height, color, command=None):
        tk.Canvas.__init__(self, parent, borderwidth=1, 
            relief="raised", highlightthickness=0)
        self.command = command

        padding = 4
        id = self.create_oval((padding,padding,
            width+padding, height+padding), outline=color, fill=color)
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0) + padding
        height = (y1-y0) + padding
        self.configure(width=width, height=height)

class RhombusButton(tk.Canvas):
    def __init__(self, parent, width, height, color, command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0, 
            relief="raised", highlightthickness=0)
        self.command = command

        padding = 4
        x = 0
        y = 0
        
        id = self.create_polygon(x,             y+(height/2),
                                 x+(width/2),   y,
                                 x+width,       y+(height/2),
                                 x+(width/2),   y+height,
                                 outline='black', fill='lightgrey')
                                 
        self.create_text(width/2, height/2,fill="black",
                         font="verdana 12 bold", text="Expression")
        
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0) + padding
        height = (y1-y0) + padding
        self.configure(width=width, height=height)
    
class ArrowButton(tk.Canvas):
    def __init__(self, parent, width, height, color, command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0, 
            relief="raised", highlightthickness=0)
        self.command = command

        padding = 4
        x = 0
        y = 0
        
        id = self.create_polygon(x,             y+30,
                                 x+width,       y+30,
                                 x+width,       y,
                                 x+width+50,    y+45,
                                 x+width,       y+90,
                                 x+width,       y+60,
                                 x,             y+60,
                                 outline='black', fill='black')
                                 
        
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0) + padding
        height = (y1-y0) + padding
        self.configure(width=width, height=height)

