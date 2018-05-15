import Tkinter as tk
import abc

class PopUp(object, tk.Frame):
    """Abstract base class for a popup window"""
    __metaclass__ = abc.ABCMeta
    def __init__(self, parent, root, project=None):
        ''' Constructor '''
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.project = project
        self.root = root
        self.parent.resizable(width=False, height=False) # Disallows window resizing
        self.validate_notempty = (self.register(self.notEmpty), '%P') # Creates Tcl wrapper for python function. %P = new contents of field after the edit.
        self.init_gui()

    @abc.abstractmethod # Must be overwriten by subclasses
    def init_gui(self):
        '''Initiates GUI of any popup window'''
        pass

    @abc.abstractmethod
    def do_something(self):
        '''Does something that all popup windows need to do'''
        pass

    def notEmpty(self, P):
        '''Validates Entry fields to ensure they aren't empty'''
        if P.strip():
            valid = True
        else:
            print("Error: Field must not be empty.") # Prints to console
            valid = False
        return valid

    def close_win(self):
        '''Closes window'''
        self.parent.destroy()

class HeaderFrame(tk.Frame):
    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)
        self.text = text
        self.show = tk.IntVar()
        self.show.set(1)

        self.title_frame = tk.Frame(self, bg='#b8d0e4')
        self.title_frame.pack(fill="x", expand=0)

        tk.Label(self.title_frame, text=text, bg='#b8d0e4').pack(side="left", fill="x", expand=1)

        
        self.toggle_button = tk.Button(self.title_frame, width=2, text='-', bg='#b8d0e4',  command=self.toggle)
        self.toggle_button.pack(side="left")
        
        self.close_button = tk.Button(self.title_frame, width=2, text='X', bg='#b8d0e4', command=self.close)
        self.close_button.pack(side="left")
        
        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self.sub_frame.pack(fill='both', expand=1)

    def toggle(self):
        self.show.set(not self.show.get())
        if bool(self.show.get()):
            self.sub_frame.pack(fill="both", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='-')
    
    def close(self):
        pass
         


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

class RoundedButton(tk.Canvas):
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
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()
            
class CircularButton(tk.Canvas):
    def __init__(self, parent, width, height, color, text='', command=None):
        tk.Canvas.__init__(self, parent, borderwidth=1, 
            relief="raised", highlightthickness=0)
        self.command = command

        padding = 4
        id = self.create_oval((padding,padding,
            width+padding, height+padding), outline=color, fill=color)
        
        self.create_text(width/2, height/2,fill="black",
                         font="verdana 12 bold", text=text)
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

