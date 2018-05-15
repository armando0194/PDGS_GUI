import Tkinter as tk
import ttk
from CustomWidgets import RhombusButton
from CustomWidgets import ArrowButton
from CustomWidgets import CircularButton
from CustomWidgets import PopUp
from CustomWidgets import HeaderFrame
from Menu import OrganizeViews
from Tkinter import Scrollbar



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
        #self.canvas.pack(fill="both", expand=1)
        self.canvas.dnd_accept = self.dnd_accept

        self.hbar = Scrollbar(self.canvas, orient=tk.HORIZONTAL)
        self.hbar.pack(side=tk.BOTTOM,fill=tk.X)
        self.hbar.config(command=self.canvas.xview)
        self.vbar=Scrollbar(self.canvas, orient=tk.VERTICAL)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=5000, height=5000)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.canvas.bind('<ButtonPress-1>', self.draw_line)
        self.canvas.bind('<ButtonRelease-1>', self.draw_line)
    
    def draw_line(self, event):
        if str(event.type) in '4':
            self.canvas.old_coords = event.x, event.y

        elif str(event.type) in '5':
            x, y = event.x, event.y
            x1, y1 = self.canvas.old_coords
            self.canvas.create_line(x, y, x1, y1, arrow="first")

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
    
    def close(self):
        OrganizeViews.diss_flag.set(0)
        self.grid_forget() 
    
    def show_exp(self):
        self.draw_area.grid(row=0, column=0, rowspan=4, columnspan=3, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        
class Icon:
 
    def __init__(self, name, shape='rect', command=None, ba=None, is_copy=False):
        self.name = name
        self.shape = shape
        self.canvas = self.label = self.id = None
        self.command = command
        self.ba = ba
        self.is_copy = is_copy
        self.arrow = False
 
    def attach(self, canvas, x=10, y=10):
        if canvas is self.canvas:
            self.canvas.coords(self.id, x, y)
            return
        if self.canvas:
            self.detach()
        if not canvas:
            return zxx
        
        if self.label is not None:
            self.label.destroy()

        if 'S' in self.name and self.is_copy:
            label = StartField(canvas, self.ba, 'Start')
        elif 'Field' in self.name and self.is_copy:
            label = Variable(canvas, self.ba, 'Field')
        elif 'Reference List' in self.name and self.is_copy:
            label = ReferenceList(canvas, self.ba, 'Reference List')
        elif 'E' in self.name and self.is_copy:
            label = HeaderFrame(canvas, 'End')
        elif 'Packet Info' in self.name and self.is_copy:
            label = PacketInfo(canvas, self.ba, 'Packet')

        elif 'rect' in self.shape :
            label = tk.Label(canvas, text=self.name,
                                  borderwidth=2, relief="raised", padx=10, pady=10)    
        elif 'circular' in self.shape :
            label = CircularButton(canvas, 50, 50, 'grey', self.name)
        elif 'rhombus' in self.shape:
            label = RhombusButton(canvas, 300, 150, 'grey')
        else:
            label = ArrowButton(canvas, 200, 150, 'black')
            self.arrow = True
            
        id = canvas.create_window(x, y, window=label, anchor="nw") 
           
        self.canvas = canvas
        self.label = label
        self.id = id
        if not self.is_copy:
            label.bind("<ButtonPress>", self.press)
        if self.is_copy:
            label.bind("<ButtonPress>", self.press_copy)
 
 
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
            copy = Icon(self.name, self.shape, command=self.command, ba=self.ba)
            copy.attach(self.canvas, self.x_orig, self.y_orig)
            self.is_copy = True
    
    def press_copy(self, event):
        if dnd_start(self, event):
            # where the pointer is relative to the label widget:
            self.x_off = event.x
            self.y_off = event.y
            # where the widget is relative to the canvas:
            self.x_orig, self.y_orig = self.canvas.coords(self.id)
            self.attach(self.canvas, self.x_orig, self.y_orig)
 
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
        if self.command:
            self.command()

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
        
class BuildingArea(HeaderFrame):
    def __init__(self, parent, text):
        HeaderFrame.__init__(self, parent, text)
        self.root = parent
        self.init_gui()
    
    def init_gui(self): 
        self.draw_area = DrawArea(self.sub_frame)
        self.pallete = HeaderFrame(self.sub_frame, 'Palette')
        self.pallete.close = self.hide_pallete
        
        self.draw_area.grid(row=0, column=0, rowspan=4, columnspan=3, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.pallete.grid(row=0, column=3, rowspan=4, columnspan=1, sticky=(tk.N, tk.S, tk.W, tk.E))
   
        self.fields = Section(self.pallete.sub_frame, text='Fields', relief="raised", borderwidth=1)
        self.fields.pack(fill="x", pady=2, padx=2, anchor="ne")
       
        self.constructs = Section(self.pallete.sub_frame, text='Constructs', relief="raised", borderwidth=1)
        self.constructs.pack(fill="x", expand=1, pady=2, padx=2, anchor="ne")
        
        for r in range(4):
            self.sub_frame.rowconfigure(r, weight=1)
        for c in range(4):
            self.sub_frame.columnconfigure(c, weight=1)
        
        self.init_fields()
        self.init_constructs()

    def init_fields(self):
        self.icons = [
                        Icon("S", shape='circular', command=self.start_field_popup, ba=self),
                        Icon("Field (Var size)", command=self.var_popup, ba=self),
                        Icon("Reference List", command=self.ref_popup, ba=self),
                        Icon("E", shape='circular', ba=self),
                        Icon("Packet Info.", command=self.pack_popup, ba=self)   
                     ]
               
        for i in range(2):        
            y = i*80+30
            self.icons[i].attach(self.fields.canvas, y=y)  
            self.icons[i+3].attach(self.fields.canvas, x=350, y=y)
        
        y = 3*80+30
        self.icons[2].attach(self.fields.canvas, y=y)
       
    
    def var_popup(self):
        pass
                
    def start_field_popup(self):
        #self.start_win = tk.Toplevel(self.root) # Set parent
        #StartField(self.start_win, self)
        pass

    def ref_popup(self):
        pass
    
    def pack_popup(self):
        pass     
        
        
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
        
    def hide_pallete(self):
        self.pallete.forget_grid()
        
    def show_pallete(self):
        self.pallete.grid(row=0, column=3, rowspan=4, columnspan=1, sticky=(tk.N, tk.S, tk.W, tk.E))
    
    def close(self):
        self.grid_forget()
    
    def show_build(self):
        self.grid(row=1, column=2, rowspan=15, columnspan=8, sticky=(tk.N, tk.S, tk.W, tk.E))

class Variable(HeaderFrame):
    """ New popup window """
    REF_OPTIONS = ["None","List 1", 'List 2']
    BASE_OPTIONS = ['base.NONE', 'base.DEC', 'base.HEX', 'base.OCT', 'base.DEC_HEX', 'base.HEX_DEC' , 'base.UNIT_STRING' ]
    DATA_TYPE_OPTIONS = ['ftypes.BOOLEAN', 'ftypes.UINT8', 'ftypes.UINT16', 'ftypes.UINT24', 'ftypes.UINT32', 'ftypes.UINT64', 'ftypes.INT8', 'ftypes.INT16', 'ftypes.INT24', 'ftypes.INT32', 'ftypes.INT64', 'ftypes.FLOAT', 'ftypes.DOUBLE', 'ftypes.ABSOLUTE_TIME', 'ftypes.RELATIVE_TIME', 'ftypes.STRING', 'ftypes.STRINGZ', 'ftypes.UINT_STRING', 'ftypes.ETHER', 'ftypes.BYTES', 'ftypes.UINT_BYTES', 'ftypes.IPv4', 'ftypes.IPv6', 'ftypes.IPXNET', 'ftypes.FRAMENUM', 'ftypes.PCRE', 'ftypes.GUID', 'ftypes.OID', 'ftypes.PROTOCOL', 'ftypes.REL_OID', 'ftypes.SYSTEM_ID', 'ftypes.EUI64', 'ftypes.NONE']
    
    def __init__(self, parent, root, text):
        ''' Constructor '''
        HeaderFrame.__init__(self, parent, text)
        self.parent = parent
        self.root = root
        self.init_gui()

    def init_gui(self):
        self.labels = [
            tk.Label(self.sub_frame, text="Name: "),
            tk.Label(self.sub_frame, text="Abbreviation: "),
            tk.Label(self.sub_frame, text="Description: "),
            tk.Label(self.sub_frame, text="Reference List: "),
            tk.Label(self.sub_frame, text="Data Type: "),
            tk.Label(self.sub_frame, text="Base: "),
            tk.Label(self.sub_frame, text="Mask: "),
            tk.Label(self.sub_frame, text="Value Constraints: "),
            tk.Label(self.sub_frame, text="Size: "),
            tk.Label(self.sub_frame, text="Required: ")
        ]
        
        
        self.ref = tk.StringVar(self.sub_frame)
        self.ref.set(self.REF_OPTIONS[0]) # default value
        
        self.base = tk.StringVar(self.sub_frame)
        self.base.set(self.BASE_OPTIONS[0]) # default value
        
        self.data = tk.StringVar(self.sub_frame)
        self.data.set(self.DATA_TYPE_OPTIONS[0]) # default value
        
        self.inputs = [
            tk.Entry(self.sub_frame),
            tk.Entry(self.sub_frame),
            tk.Entry(self.sub_frame),
            tk.OptionMenu(self.sub_frame, self.ref, *self.REF_OPTIONS),
            tk.OptionMenu(self.sub_frame, self.base, *self.BASE_OPTIONS),
            tk.OptionMenu(self.sub_frame, self.data, *self.DATA_TYPE_OPTIONS),
            tk.Entry(self.sub_frame),
            tk.Entry(self.sub_frame),
            tk.Entry(self.sub_frame),
            tk.Checkbutton(self.sub_frame)
        ]
        
        for i in range(len(self.labels)):
            self.labels[i].grid(row=i, column=0)
        for i in range(len(self.labels)):
            self.inputs[i].grid(row=i, column=1, sticky='ew')

        # Padding
        for child in self.sub_frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

    
    def do_something(self):
        self.close_win()

class StartField(HeaderFrame):
    """ New popup window """
    REF_OPTIONS = ["List 1", 'List 2']
    BASE_OPTIONS = ["64", '8', '2']
    DATA_TYPE_OPTIONS = ["Int", 'Str', 'Double']
    
    def __init__(self, parent, root, text):
        ''' Constructor '''
        HeaderFrame.__init__(self, parent, text)
        self.parent = parent
        self.root = root
        self.init_gui()

    def init_gui(self):
        # Create Widgets
        
        self.labels = [
            tk.Label(self.sub_frame, text="Protocol Name: "),
            tk.Label(self.sub_frame, text="Protocol Description: "),
            tk.Label(self.sub_frame, text="Dependent Protocol Name: "),
            tk.Label(self.sub_frame, text="Dependency Pattern: "),
        ]
        
        self.ref = tk.StringVar(self.sub_frame)
        self.ref.set(self.REF_OPTIONS[0]) # default value
        
        self.base = tk.StringVar(self.sub_frame)
        self.base.set(self.BASE_OPTIONS[0]) # default value
        
        self.data = tk.StringVar(self.sub_frame)
        self.data.set(self.DATA_TYPE_OPTIONS[0]) # default value
        
        self.inputs = [
            tk.Entry(self.sub_frame),
            tk.Entry(self.sub_frame),
            tk.Entry(self.sub_frame),
            tk.Entry(self.sub_frame)
        ]
        
        for i in range(len(self.labels)):
            self.labels[i].grid(row=i, column=0)
        for i in range(len(self.labels)):
            self.inputs[i].grid(row=i, column=1, sticky='ew')

        # Padding
        for child in self.sub_frame.winfo_children():
            child.grid_configure(padx=5, pady=2)
    
    def do_something(self):
        self.close_win()

class ReferenceList(HeaderFrame):
    
    def __init__(self, parent, root, text):
        ''' Constructor '''
        HeaderFrame.__init__(self, parent, text)
        self.parent = parent
        self.root = root
        self.init_gui()

    def init_gui(self):
        self.x = 3
        # Create Widgets
        self.top = ttk.Frame(self.sub_frame)
        self.bot = ttk.Frame(self.sub_frame)
        
        self.top.pack()
        self.bot.pack()
        
        self.labels = [
            tk.Label(self.top, text="Reference List: "),
        ]
        
        self.inputs = [
            tk.Entry(self.top)
        ]
        
        self.labels[0].grid(row=0, column=0, sticky='w')      
        self.inputs[0].grid(row=0, column=1, sticky='we')

        tk.Label(self.bot, text="Value: ").grid(row=0, column=0)        
        tk.Label(self.bot, text="Text Description").grid(row=0, column=1)   
        
        tk.Entry(self.bot).grid(row=1, column=1)        
        tk.Entry(self.bot).grid(row=1, column=0)
        
        tk.Button(self.bot, text='add', command=self.add).grid(row=10, column=1, sticky='e')
    
    
    def add(self):
        tk.Entry(self.bot).grid(row=self.x, column=0) 
        tk.Entry(self.bot).grid(row=self.x, column=1) 
        self.x+=1
        
    def do_something(self):
        self.close_win()
        
class PacketInfo(HeaderFrame):
    def __init__(self, parent, root, text):
        ''' Constructor '''
        HeaderFrame.__init__(self, parent, text)
        self.parent = parent
        self.root = root
        self.init_gui()

    def init_gui(self):

        self.x = 3
        # Create Widgets
        self.top = ttk.Frame(self.sub_frame)
        self.bot = ttk.Frame(self.sub_frame)
        
        self.top.pack()
        self.bot.pack()

        tk.Label(self.bot, text="Value: ").grid(row=0, column=0)        
        tk.Label(self.bot, text="Text Description").grid(row=0, column=1)   
        
        tk.Entry(self.bot).grid(row=1, column=1)        
        tk.Entry(self.bot).grid(row=1, column=0)
        
        tk.Button(self.bot, text='add', command=self.add).grid(row=10, column=1, sticky='e')
        
    
    def add(self):
        tk.Entry(self.bot).grid(row=self.x, column=0) 
        tk.Entry(self.bot).grid(row=self.x, column=1) 
        self.x+=1
        
    def do_something(self):
        self.close_win()

