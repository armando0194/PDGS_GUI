import Tkinter as tk
from Tkinter import * 

# Lots of tutorials have from tkinter import *, but that is pretty much always a bad idea
import ttk
import abc
import os
from PIL import ImageTk, Image

class Menubar(tk.Frame):
    """Builds a menu bar for the top of the main window"""
    def __init__(self, parent, *args, **kwargs):
        ''' Constructor'''
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_menubar()


    def on_exit(self):
        '''Exits program'''
        quit()

    def display_help(self):
        '''Displays help document'''
        pass

    def display_about(self):
        '''Displays info about program'''
        pass

    def init_menubar(self):
     
        # Create Widgets
        self.btns = [ttk.Button(self, text='Create Project'),
                     ttk.Button(self, text='Save Project'),
                     ttk.Button(self, text='Close Project'),
                     ttk.Button(self, text='Switch Workspace'),
                     ttk.Button(self, text='Import Project'),
                     ttk.Button(self, text='Export Project'),
                     ttk.Button(self, text='Generate Dissector Script'),
                     ttk.Button(self, text='Organize Views'),
                     ttk.Button(self, text='Open PCAP')]
        for i in range(len(self.btns)):
            self.btns[i].grid(row=0, column=i, padx=10, pady=10)
#==============================================================================
#         
# class Window(tk.Frame):
#     """Abstract base class for a popup window"""
#     __metaclass__ = abc.ABCMeta
#     def __init__(self, parent):
#         ''' Constructor '''
#         tk.Frame.__init__(self, parent)
#         self.parent = parent
#         self.parent.resizable(width=False, height=False) # Disallows window resizing
#         self.validate_notempty = (self.register(self.notEmpty), '%P') # Creates Tcl wrapper for python function. %P = new contents of field after the edit.
#         self.init_gui()
# 
#     @abc.abstractmethod # Must be overwriten by subclasses
#     def init_gui(self):
#         '''Initiates GUI of any popup window'''
#         pass
# 
#     @abc.abstractmethod
#     def do_something(self):
#         '''Does something that all popup windows need to do'''
#         pass
# 
#     def notEmpty(self, P):
#         '''Validates Entry fields to ensure they aren't empty'''
#         if P.strip():
#             valid = True
#         else:
#             print("Error: Field must not be empty.") # Prints to console
#             valid = False
#         return valid
# 
#     def close_win(self):
#         '''Closes window'''
#         self.parent.destroy()
# 
# class SomethingWindow(Window):
#     """ New popup window """
# 
#     def init_gui(self):
#         self.parent.title("New Window")
#         self.parent.columnconfigure(0, weight=1)
#         self.parent.rowconfigure(3, weight=1)
# 
#         # Create Widgets
# 
#         self.label_title = ttk.Label(self.parent, text="This sure is a new window!")
#         self.contentframe = ttk.Frame(self.parent, relief="sunken")
# 
#         self.label_test = ttk.Label(self.contentframe, text='Enter some text:')
#         self.input_test = ttk.Entry(self.contentframe, width=30, validate='focusout', validatecommand=(self.validate_notempty))
# 
#         self.btn_do = ttk.Button(self.parent, text='Action', command=self.do_something)
#         self.btn_cancel = ttk.Button(self.parent, text='Cancel', command=self.close_win)
# 
#         # Layout
#         self.label_title.grid(row=0, column=0, columnspan=2, sticky='nsew')
#         self.contentframe.grid(row=1, column=0, columnspan=2, sticky='nsew')
# 
#         self.label_test.grid(row=0, column=0)
#         self.input_test.grid(row=0, column=1, sticky='w')
# 
#         self.btn_do.grid(row=2, column=0, sticky='e')
#         self.btn_cancel.grid(row=2, column=1, sticky='e')
# 
#         # Padding
#         for child in self.parent.winfo_children():
#             child.grid_configure(padx=10, pady=5)
#         for child in self.contentframe.winfo_children():
#             child.grid_configure(padx=5, pady=2)
# 
#     def do_something(self):
#         '''Does something'''
#         text = self.input_test.get().strip()
#         if text:
#             # Do things with text
#             self.close_win()
#         else:
#             print("Error: But for real though, field must not be empty.")
#==============================================================================

class ProjectExplorer(tk.Frame):
    def __init__(self, master, path):
        tk.Frame.__init__(self, master)
        self.tree = ttk.Treeview(self)
        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text=path, anchor='w')

        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text=abspath, open=True)
        self.process_directory(root_node, abspath)

        self.tree.grid(row=0, column=0 )
        
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')
        #self.grid()

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)       
    
class Tabs(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
    
        # gives weight to the cells in the grid
        rows = 0
        while rows < 4:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows += 1
         
        # Defines and places the notebook widget
        nb = ttk.Notebook(self)
        nb.grid(row=1, column=0, columnspan=4, rowspan=3, sticky='NESW')
         
        # Adds tab 1 of the notebook
        page1 = ttk.Frame(nb)
        nb.add(page1, text='Tab1')
         
        # Adds tab 2 of the notebook
        page2 = ttk.Frame(nb)
        nb.add(page2, text='Tab2')
 
class Example(tk.Frame):
    '''Illustrate how to drag items on a Tkinter canvas'''

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a canvas
        self.canvas = tk.Canvas(width=400, height=400)
        self.canvas.grid(row=2, column=0)

        # this data is used to keep track of an 
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create a couple of movable objects
        self._create_token((100, 100), "white")
        self._create_token((200, 100), "black")

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("token", "<B1-Motion>", self.on_token_motion)

    def _create_token(self, coord, color):
        '''Create a token at the given coordinate in the given color'''
        (x,y) = coord
        self.canvas.create_oval(x-25, y-25, x+25, y+25, 
                                outline=color, fill=color, tags="token")

    def on_token_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_token_motion(self, event):
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        
class GUI(tk.Frame):
    """Main GUI class"""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.option_add('*font', ('verdana', 15, 'bold'))
        self.init_gui()

    def openwindow(self):
        self.new_win = tkinter.Toplevel(self.root) # Set parent
        SomethingWindow(self.new_win)

    def init_gui(self):
        self.root.title('Test GUI')
        self.root.geometry("1200x800")


        self.root.option_add('*tearOff', 'FALSE') # Disables ability to tear menu bar into own window
        
        self.label_title = ttk.Label(self, text="Protocol Dissector Generator System")
        self.label_title.grid(row=0, column=0)
        
        # Menu Bar
        self.menubar = Menubar(self.root)
        self.menubar.grid(row=1, column=0, sticky='ew')
        
        # Project Explorer
        self.project_explorer = ProjectExplorer(self.root, '/home/armando/Desktop')
        self.project_explorer.grid(row=2, column=0, sticky='ew')
        
        #drag and drop 
        self.drag_drop = Example(self.root)
       # self.drag_drop.grid(row=2, column=0, sticky='ew')
        
        self.tabs = Tabs(self.root)
        self.tabs.grid(row=3, column=0, sticky='ew')
        


if __name__ == '__main__':
    root = tk.Tk()
    GUI(root)
root.mainloop()