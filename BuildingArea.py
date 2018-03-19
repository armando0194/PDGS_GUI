import Tkinter as tk
import ttk
from CustomWidgets import RhombusButton
from CustomWidgets import ArrowButton
from CustomWidgets import CircularButtonw

def dnd_start(source, event):
    h = DndHandler(source, event)
    if h.root:
        return h
    else:
        return None

class DndHandler:
 
    root = None
 
    def __init__(self, source, event):
        if event.num > 5:
            return
        root = event.widget._root()
        try:
            root.__dnd
            return # Don't start recursive dnd
        except AttributeError:
            root.__dnd = self
            self.root = root
        self.source = source
        self.target = None
        self.initial_button = button = event.num
        self.initial_widget = widget = event.widget
        self.release_pattern = "<B%d-ButtonRelease-%d>" % (button, button)
        self.save_cursor = widget['cursor'] or ""
        widget.bind(self.release_pattern, self.on_release)
        widget.bind("<Motion>", self.on_motion)
        widget['cursor'] = "hand2"
 
    def __del__(self):
        root = self.root
        self.root = None
        if root:
            try:
                del root.__dnd
            except AttributeError:
                pass
 
    def on_motion(self, event):
        x, y = event.x_root, event.y_root
        target_widget = self.initial_widget.winfo_containing(x, y)
        source = self.source
        new_target = None
        while target_widget:
            try:
                attr = target_widget.dnd_accept
            except AttributeError:
                pass
            else:
                new_target = attr(source, event)
                if new_target:
                    break
            target_widget = target_widget.master
        old_target = self.target
        if old_target is new_target:
            if old_target:
                old_target.dnd_motion(source, event)
        else:
            if old_target:
                self.target = None
                old_target.dnd_leave(source, event)
            if new_target:
                new_target.dnd_enter(source, event)
                self.target = new_target
 
    def on_release(self, event):
        self.finish(event, 1)
 
    def cancel(self, event=None):
        self.finish(event, 0)
 
    def finish(self, event, commit=0):
        target = self.target
        source = self.source
        widget = self.initial_widget
        root = self.root
        try:
            del root.__dnd
            self.initial_widget.unbind(self.release_pattern)
            self.initial_widget.unbind("<Motion>")
            widget['cursor'] = self.save_cursor
            self.target = self.source = self.initial_widget = self.root = None
            if target:
                if commit:
                    target.dnd_commit(source, event)
                else:
                    target.dnd_leave(source, event)
        finally:
            source.dnd_end(target, event)

class Section(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)
        self.text = text
        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        tk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = tk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show)
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        
        self.canvas = tk.Canvas(self.sub_frame, height=500)
        self.canvas.pack(fill="both")
        self.canvas.dnd_accept = self.dnd_accept

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')
 
    def dnd_accept(self, source, event):
        return self
 
    def dnd_enter(self, source, event):
        self.canvas.focus_set() # Show highlight border
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = source.canvas.bbox(source.id)#Source Resources and Information.)
        dx, dy = x2-x1, y2-y1
        self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
        self.dnd_motion(source, event)
 
    def dnd_motion(self, source, event):
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
        self.canvas.move(self.dndid, x-x1, y-y1)
 
    def dnd_leave(self, source, event):
        #self.top.focus_set() # Hide highlight border
        self.canvas.delete(self.dndid)
        self.dndid = None
 
    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        x, y = source.where(self.canvas, event)
        source.attach(self.canvas, x, y)

class DrawArea(tk.Frame):
 
    def __init__(self, root):
        tk.Frame.__init__(self, root, bg='white')
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=1)
        self.canvas.dnd_accept = self.dnd_accept
 
    def dnd_accept(self, source, event):
        return self
 
    def dnd_enter(self, source, event):
        self.canvas.focus_set() # Show highlight border
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = source.canvas.bbox(source.id)#Source Resources and Information.)
        dx, dy = x2-x1, y2-y1
        self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
        self.dnd_motion(source, event)
 
    def dnd_motion(self, source, event):
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
        self.canvas.move(self.dndid, x-x1, y-y1)
 
    def dnd_leave(self, source, event):
        self.canvas.delete(self.dndid)
        self.dndid = None
 
    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        x, y = source.where(self.canvas, event)
        source.attach(self.canvas, x, y)
        
        
class Icon:
 
    def __init__(self, name, shape='rect'):
        self.name = name
        self.shape = shape
        self.canvas = self.label = self.id = None
 
    def attach(self, canvas, x=10, y=10):
        if canvas is self.canvas:
            self.canvas.coords(self.id, x, y)
            return
        if self.canvas:
            self.detach()
        if not canvas:
            return zxx
        if 'rect' in self.shape :
            label = tk.Label(canvas, text=self.name,
                                  borderwidth=2, relief="raised", padx=10, pady=10)    
        elif 'circular' in self.shape :
            label = CircularButton(canvas, 50, 50, 'grey')
        elif 'rhombus' in self.shape:
            label = RhombusButton(canvas, 300, 150, 'grey')
        else:
            label = ArrowButton(canvas, 200, 150, 'black')
            
        id = canvas.create_window(x, y, window=label, anchor="nw") 
           
        self.canvas = canvas
        self.label = label
        self.id = id
        label.bind("<ButtonPress>", self.press)
 
    def detach(self):
        canvas = self.canvas
        if not canvas:
            return
        id = self.id
        label = self.label
        self.canvas = self.label = self.id = None
        canvas.delete(id)
        label.destroy()
 
    def press(self, event):
        if dnd_start(self, event):
            # where the pointer is relative to the label widget:
            self.x_off = event.x
            self.y_off = event.y
            # where the widget is relative to the canvas:
            self.x_orig, self.y_orig = self.canvas.coords(self.id)
            copy = Icon(self.name, self.shape)
            copy.attach(self.canvas, self.x_orig, self.y_orig)
 
    def move(self, event):
        x, y = self.where(self.canvas, event)
        self.canvas.coords(self.id, x, y)
 
    def putback(self):
        self.canvas.coords(self.id, self.x_orig, self.y_orig)
 
    def where(self, canvas, event):
        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        # compensate for initial pointer offset
        return x - self.x_off, y - self.y_off
 
    def dnd_end(self, target, event):
        pass

class DndFrame(tk.Frame):
    def __init__(self, root, text, width=100, height=100):
        tk.Frame.__init__(self, root)
        
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)
        tk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=0)
        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self.sub_frame.pack(fill="both", expand=1)
        self.text = text
        self.root = root
    
        self.canvas = tk.Canvas(self.sub_frame , width=width, height=height)
        self.canvas.pack(fill="both", expand=1)
        self.canvas.dnd_accept = self.dnd_accept
 
    def dnd_accept(self, source, event):
        return self
 
    def dnd_enter(self, source, event):
        self.canvas.focus_set() # Show highlight border
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = source.canvas.bbox(source.id)#Source Resources and Information.)
        dx, dy = x2-x1, y2-y1
        self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
        self.dnd_motion(source, event)
 
    def dnd_motion(self, source, event):
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
        self.canvas.move(self.dndid, x-x1, y-y1)
 
    def dnd_leave(self, source, event):
        self.canvas.delete(self.dndid)
        self.dndid = None
 
    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        x, y = source.where(self.canvas, event)
        source.attach(self.canvas, x, y)
        
class BuildingArea(tk.Frame):
    '''Illustrate how to drag items on a Tkinter canvas'''

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.root = parent
        self.init_gui()
    
    def init_gui(self): 
        
        self.draw_area = DrawArea(self)
        self.pallete = tk.Frame(self)
        
        self.draw_area.grid(row=0, column=0, rowspan=4, columnspan=3, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.pallete.grid(row=0, column=3, rowspan=4, columnspan=1, sticky=(tk.N, tk.S, tk.W, tk.E))
   
        self.fields = Section(self.pallete, text='Fields', relief="raised", borderwidth=1)
        self.fields.pack(fill="x", pady=2, padx=2, anchor="ne")
       
        self.constructs = Section(self.pallete, text='Constructs', relief="raised", borderwidth=1)
        self.constructs.pack(fill="x", expand=1, pady=2, padx=2, anchor="ne")
        
        for r in range(4):
            self.rowconfigure(r, weight=1)
        for c in range(4):
            self.columnconfigure(c, weight=1)
        
        self.init_fields()
        self.init_constructs()

    def init_fields(self):
        self.icons = [
                        Icon("Start Field", shape='circular'),
                        Icon("Field (2 Byte)"),
                        Icon("Field (8 Byte)"),
                        Icon("Field (8 Byte)"),
                        Icon("Field (Var size)"),
                        Icon("Reference List"),
                        Icon("Field (1 Byte)"),
                        Icon("Field (4 Byte)"),
                        Icon("Field (16 Byte)"),
                        Icon("Field (16 Byte)"),
                        Icon("End Field"),
                        Icon("Packet Info.")   
                     ]
               
        for i in range(6):        
            y = i*80+30
            self.icons[i].attach(self.fields.canvas, y=y)  
            self.icons[i+6].attach(self.fields.canvas, x=350, y=y)
    
    def init_constructs(self):
        self.constructs.canvas.destroy()
        
        self.decision = DndFrame(self.constructs.sub_frame, "Decision", height=200)  
        self.expression = Icon("Expression", shape='rhombus')
        self.expression.attach(self.decision.canvas)
        self.decision.pack(fill="x", expand=1)
        
        self.connector = DndFrame(self.constructs.sub_frame, text="Connector", height=200)
        self.arrow = Icon("Constructor", shape='arrow')
        self.arrow.attach(self.connector.canvas)
        self.connector.pack(fill="x", expand=0)
        
        self.expression = DndFrame(self.constructs.sub_frame, text="Expression")
        self.expression.pack(fill="x", expand=0)
        
        self.relational = DndFrame(self.expression, text="Relational Operator")
        self.relational.pack(fill="x", expand=0)
        
        self.rel_icons = [
                        Icon("<"),
                        Icon(">"),
                        Icon("<="),
                        Icon(">="),
                        Icon("=="),
                        Icon("~=")
                     ]
        for i in range(6):        
            x = i*100+10
            self.rel_icons[i].attach(self.relational.canvas, x=x)  
            
        
        self.logical = DndFrame(self.expression, text="Logical Operator")
        self.logical.pack(fill="x", expand=0)
        
        self.log_icons = [
                        Icon("And"),
                        Icon("Or"),
                        Icon("Not"),
                     ]
                     
        for i in range(3):        
            x = i*150+10
            self.log_icons[i].attach(self.logical.canvas, x=x)  
                     
        self.operand = Icon("Operand")
        self.operand.attach(self.expression.canvas)  
