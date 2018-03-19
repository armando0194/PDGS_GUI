import Tkinter as tk
from Tkinter import * 

# Lots of tutorials have from tkinter import *, but that is pretty much always a bad idea
import ttk
import abc
import os
from PIL import ImageTk, Image
import Tkconstants, tkFileDialog

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
            
class GUI(tk.Frame):
    """Main GUI class"""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.option_add('*font', ('verdana', 12, 'bold'))
        self.openwindow()

    def openwindow(self):
        self.new_win = Toplevel(self.root) # Set parent
        WorkspaceLauncher(self.new_win, self)

    def init_gui(self, workspace_path):
        self.root.deiconify()
        print(workspace_path)
        self.root.title('Test GUI')
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(str(self.screen_width)+"x"+str(self.screen_height))#"1200x800")
        
        self.project_explorer = ProjectExplorer(self.root, '/home/armando/Documents/Software/PDGS_GUI/testprojects')
        self.menubar = Menubar(self.root, workspace_path, self.project_explorer)
        self.building_area = BuildingArea(self.root)
        
        self.Frame1 = tk.Frame(self.root, bg="grey")
        self.Frame2 = tk.Frame(self.root, bg="blue")
        self.Frame3 = tk.Frame(self.root, bg="green")
        self.Frame4 = tk.Frame(self.root, bg="brown")
        self.Frame5 = tk.Frame(self.root, bg="pink")
        self.Frame6 = tk.Frame(self.root, bg="white")
    
        self.menubar.grid(row=0, column=0, rowspan=1, columnspan=10, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.project_explorer.grid(row=1, column=0, rowspan=15, columnspan=2, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.building_area.grid(row=1, column=2, rowspan=15, columnspan=8, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.Frame5.grid(row=16, column=0, rowspan=4, columnspan=10, sticky=(tk.N, tk.S, tk.W, tk.E))

        for r in range(20):
            self.root.rowconfigure(r, weight=1)
        for c in range(10):
            self.root.columnconfigure(c, weight=1)

#==============================================================================
#         self.root.option_add('*tearOff', 'FALSE') # Disables ability to tear menu bar into own window
#         
#         self.label_title = ttk.Label(self, text="Protocol Dissector Generator System")
#         self.label_title.grid(row=0, column=0)
#         
#         # Menu Bar
#         self.menubar = Menubar(self.root)
#         self.menubar.grid(row=1, column=0, sticky='ew')
#         
#         # Project Explorer

#         self.project_explorer.grid(row=2, column=0, sticky='ew')
#         
#         #drag and drop 
#         self.drag_drop = Example(self.root)
#        # self.drag_drop.grid(row=2, column=0, sticky='ew')
#         
#         self.tabs = Tabs(self.root)
#         self.tabs.grid(row=3, column=0, sticky='ew')
#         
#==============================================================================

class Menubar(tk.Frame):
    """Builds a menu bar for the top of the main window"""
    def __init__(self, parent, path, project_explorer):
        ''' Constructor'''
        tk.Frame.__init__(self, parent)
        self.path = path
        self.project_explorer = project_explorer
        self.root = parent
        self.init_menubar()
    
    def new_project(self):
        self.new_proj_win = Toplevel(self.root) # Set parent
        NewProject(self.new_proj_win, self)
    
    def generate_dissector(self):
        self.gen_diss_win = Toplevel(self.root) # Set parent
        DissectorGenerator(self.gen_diss_win, self)
        
    def proj_import(self):
        self.proj_import_win = Toplevel(self.root) # Set parent
        ProjectImport(self.proj_import_win, self)
    
    def proj_export(self):
        self.proj_export_win = Toplevel(self.root) # Set parent
        ProjectExport(self.proj_export_win, self)
        
    def org_views(self):
        self.org_views_win = Toplevel(self.root) # Set parent
        OrganizeViews(self.org_views_win, self)
    
    def open_pcap(self):
        self.open_pcap_win = Toplevel(self.root) # Set parent
        OpenPCAP(self.open_pcap_win, self)
        
    def rebuild_tree(self, path):
        self.project_explorer.rebuild_tree(path)

    def init_menubar(self):
        self.label_title = Label(self, text="Protocol Dissector Generator System", font=("Helvetica", 18, 'bold'))
        self.label_title.grid(row=0, column=0, columnspan=10)
        
        # Create Widgets
        self.btns = [Button(self, text='Create Project', command=self.new_project),
                     Button(self, text='Save Project'),
                     Button(self, text='Close Project'),
                     Button(self, text='Switch Workspace'),
                     Button(self, text='Import Project', command=self.proj_import),
                     Button(self, text='Export Project', command=self.proj_export),
                     Button(self, text='Generate Dissector Script', command=self.generate_dissector),
                     Button(self, text='Organize Views', command=self.org_views),
                     Button(self, text='Open PCAP', command=self.open_pcap)]                   
       
        for i in range(len(self.btns)):
            self.btns[i].grid(row=1, column=i, padx=10, pady=10)
            self.btns[i].config(width=15)

            
class PopUp(object, tk.Frame):
    """Abstract base class for a popup window"""
    __metaclass__ = abc.ABCMeta
    def __init__(self, parent, root):
        ''' Constructor '''
        tk.Frame.__init__(self, parent)
        self.parent = parent
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
        
class WorkspaceLauncher(PopUp):
    """ New popup window """

    def init_gui(self):
        self.folder_path = ''
        self.parent.title("Workspace Launcher")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(3, weight=1)

        # Create Widgets
        self.label_title = ttk.Label(self.parent, text="Select a directory as workspace: PDGS uses the workspace\ndirectory to store projects.")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")

        self.path_entry = EntryWithPlaceholder(self.contentframe, 'Workspace Directory Path')
        self.browse_btn = Button(self.contentframe, text="Browse", command=self.browse)
        
        self.btn_do = Button(self.parent, text='Launch', command=self.do_something)
        self.btn_cancel = Button(self.parent, text='Cancel', command=self.close_win)

        # Layout
        self.label_title.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.contentframe.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.path_entry.grid(row=0, column=0, sticky='ew')
        self.contentframe.columnconfigure(0, weight=1)
        self.browse_btn.grid(row=0, column=1, sticky='e')

        self.btn_do.grid(row=2, column=0, sticky='e')
        self.btn_cancel.grid(row=2, column=1, sticky='e')

        # Padding
        for child in self.parent.winfo_children():
            child.grid_configure(padx=10, pady=5)
        for child in self.contentframe.winfo_children():
            child.grid_configure(padx=5, pady=2)
    
    def browse(self):
        self.folder_path = tkFileDialog.askdirectory()
        self.path_entry.put_text(self.folder_path)

    def do_something(self):
        self.folder_path = self.path_entry.get()
        if self.folder_path:
            self.root.init_gui(self.folder_path )
            # Do things with text
            self.close_win()
        else:
            print("Error: But for real though, field must not be empty.")

class NewProject(PopUp):
    """ New popup window """

    def init_gui(self):
        self.folder_path = ''
        self.parent.title("New Project")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(3, weight=1)

        # Create Widgets
        self.label_title = Label(self.parent, text="Create a new project")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")
        
        self.proj_name = Label(self.contentframe, text="Project Name: ")
        self.proj_name_entry = EntryWithPlaceholder(self.contentframe, 'Project Name')
        self.proj_desc = Label(self.contentframe, text="Project Description:")
        self.proj_desc_entry = Text(self.contentframe, height=5)
        
        self.btn_do = Button(self.parent, text='Create', command=self.do_something)
        self.btn_cancel = Button(self.parent, text='Cancel', command=self.close_win)

        # Layout
        self.label_title.grid(row=0, column=0, columnspan=2, sticky='')
        self.contentframe.grid(row=1, column=0, columnspan=2, sticky='')

        self.proj_name.grid(row=0, column=0, sticky='ew')
        self.proj_name_entry.grid(row=0, column=1, sticky='ew')
        
        self.proj_desc.grid(row=1, column=0, sticky='ew')
        self.proj_desc_entry.grid(row=1, column=1, sticky='ew')


        self.btn_do.grid(row=2, column=0, sticky='e')
        self.btn_cancel.grid(row=2, column=1, sticky='e')
        
        self.contentframe.columnconfigure(0, weight=1)

        # Padding
        for child in self.parent.winfo_children():
            child.grid_configure(padx=10, pady=5)
        for child in self.contentframe.winfo_children():
            child.grid_configure(padx=5, pady=2)
    
    def do_something(self):

        if self.proj_name_entry.get():
            file_path = self.root.path + "/" + self.proj_name_entry.get()
            self.ensure_dir(file_path)
            self.root.rebuild_tree(self.root.path)
            # Do things with text
            self.close_win()
        else:
            print("Error: But for real though, field must not be empty.")
    
    def ensure_dir(self, file_path):
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)

class DissectorGenerator(PopUp):
    """ New popup window """
    FORMAT_OPTIONS = ["LUA"]
    
    def init_gui(self):
        self.parent.title("Dissector Script")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(3, weight=1)

        # Create Widgets
        self.label_title = Label(self.parent, text="Generate a custom dissector script from a selected project")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")
        
        self.proj_name = Label(self.contentframe, text="Project: ")
        self.format = Label(self.contentframe, text="Dissector Format: ")
        self.save_path = Label(self.contentframe, text="Save Location: ")
        
        self.variable = StringVar(self.contentframe)
        self.variable.set(self.FORMAT_OPTIONS[0]) # default value
        self.format_dropdown = OptionMenu(self.contentframe, self.variable, *self.FORMAT_OPTIONS)
       
        self.proj_path_entry = EntryWithPlaceholder(self.contentframe, 'Project Name')
        self.proj_browse_btn = Button(self.contentframe, text="Browse", command=self.browse_proj)
        
        self.save_path_entry = EntryWithPlaceholder(self.contentframe, 'Local File System Path')
        self.save_browse_btn = Button(self.contentframe, text="Browse", command=self.browse_save)
           
        self.btn_do = Button(self.parent, text='Generate', command=self.do_something)
        self.btn_cancel = Button(self.parent, text='Cancel', command=self.close_win)

        # Layout
        self.label_title.grid(row=0, column=0, columnspan=2, sticky='')
        self.contentframe.grid(row=1, column=0, columnspan=2, sticky='')

        self.proj_name.grid(row=0, column=0, sticky='ew')
        self.proj_path_entry.grid(row=0, column=1, sticky='ew')
        self.proj_browse_btn.grid(row=0, column=2, sticky='ew')     
        
        self.format.grid(row=1, column=0, sticky='ew')
        self.format_dropdown.grid(row=1, column=1, sticky='ew')
        
        
        self.save_path.grid(row=2, column=0, sticky='ew')
        self.save_path_entry.grid(row=2, column=1, sticky='ew')
        self.save_browse_btn.grid(row=2, column=2, sticky='ew')        

        self.btn_do.grid(row=2, column=0, sticky='e')
        self.btn_cancel.grid(row=2, column=1, sticky='e')
        
        #

        # Padding
        for child in self.parent.winfo_children():
            child.grid_configure(padx=10, pady=5)
        for child in self.contentframe.winfo_children():
            child.grid_configure(padx=5, pady=2)
    
    def do_something(self):
        self.close_win()
        
    def browse_proj(self):
        self.proj_path = tkFileDialog.askdirectory()
        self.proj_path_entry.put_text(self.proj_path)
    
    def browse_save(self):
        self.save_path = tkFileDialog.askdirectory()
        self.save_path_entry.put_text(self.save_path)
        
class ProjectImport(PopUp):
    """ New popup window """

    def init_gui(self):
        self.folder_path = ''
        self.parent.title("Project Import")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(3, weight=1)

        # Create Widgets
        self.label_title = ttk.Label(self.parent, text="Import a project into the current workspace")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")

        self.proj = ttk.Label(self.contentframe, text="Project")
        self.path_entry = EntryWithPlaceholder(self.contentframe, 'Project Name')
        self.browse_btn = Button(self.contentframe, text="Browse", command=self.browse)
        
        self.btn_do = Button(self.parent, text='Import', command=self.do_something)
        self.btn_cancel = Button(self.parent, text='Cancel', command=self.close_win)

        # Layout
        self.label_title.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.contentframe.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.proj.grid(row=0, column=0, sticky='ew')
        self.path_entry.grid(row=0, column=1, sticky='ew')
        #self.contentframe.columnconfigure(0, weight=1)
        self.browse_btn.grid(row=0, column=2, sticky='e')

        self.btn_do.grid(row=2, column=0, sticky='e')
        self.btn_cancel.grid(row=2, column=1, sticky='e')

        # Padding
        for child in self.parent.winfo_children():
            child.grid_configure(padx=10, pady=5)
        for child in self.contentframe.winfo_children():
            child.grid_configure(padx=5, pady=2)
    
    def browse(self):
        self.folder_path = tkFileDialog.askdirectory()
        self.path_entry.put_text(self.folder_path)

    def do_something(self):
        self.folder_path = self.path_entry.get()
        if self.folder_path:
            self.close_win()
        else:
            print("Error: But for real though, field must not be empty.")
      
      
class ProjectExport(PopUp):
    """ New popup window """
    
    def init_gui(self):
        self.parent.title("Project Export")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(3, weight=1)

        # Create Widgets
        self.label_title = Label(self.parent, text="Export a project to the local system.")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")
        
        self.proj_name = Label(self.contentframe, text="Project: ")
        self.proj_path_entry = EntryWithPlaceholder(self.contentframe, 'Project Name')
        self.proj_browse_btn = Button(self.contentframe, text="Browse", command=self.browse_proj)
        
        self.format = Label(self.contentframe, text="To Export File: ")
        self.save_path_entry = EntryWithPlaceholder(self.contentframe, 'Local File System Path')
        self.save_browse_btn = Button(self.contentframe, text="Browse", command=self.browse_save)
           
        self.btn_do = Button(self.parent, text='Generate', command=self.do_something)
        self.btn_cancel = Button(self.parent, text='Cancel', command=self.close_win)

        # Layout
        self.label_title.grid(row=0, column=0, columnspan=2, sticky='')
        self.contentframe.grid(row=1, column=0, columnspan=2, sticky='')

        self.proj_name.grid(row=0, column=0, sticky='ew')
        self.proj_path_entry.grid(row=0, column=1, sticky='ew')
        self.proj_browse_btn.grid(row=0, column=2, sticky='ew')     
                
        self.format.grid(row=1, column=0, sticky='ew')
        self.save_path_entry.grid(row=1, column=1, sticky='ew')
        self.save_browse_btn.grid(row=1, column=2, sticky='ew')        

        self.btn_do.grid(row=2, column=0, sticky='e')
        self.btn_cancel.grid(row=2, column=1, sticky='e')

        # Padding
        for child in self.parent.winfo_children():
            child.grid_configure(padx=10, pady=5)
        for child in self.contentframe.winfo_children():
            child.grid_configure(padx=5, pady=2)
    
    def do_something(self):
        self.close_win()
        
    def browse_proj(self):
        self.proj_path = tkFileDialog.askdirectory()
        self.proj_path_entry.put_text(self.proj_path)
    
    def browse_save(self):
        self.save_path = tkFileDialog.askdirectory()
        self.save_path_entry.put_text(self.save_path)
        
class OrganizeViews(PopUp):
    """ New popup window """
    proj_flag = None
    diss_flag = None
    palette_flag = None
    packet_flag = None
    disse_flag = None
    raw_flag = None
    console_flag = None
        
    def init_gui(self):
        if OrganizeViews.proj_flag == None:
            OrganizeViews.proj_flag = IntVar(value=1)
            OrganizeViews.diss_flag = IntVar(value=1)
            OrganizeViews.palette_flag = IntVar(value=1)
            OrganizeViews.packet_flag = IntVar(value=1)
            OrganizeViews.disse_flag = IntVar(value=1)
            OrganizeViews.raw_flag = IntVar(value=1)
            OrganizeViews.console_flag = IntVar(value=1)
        
        self.parent.title("Organize Views")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(3, weight=1)

        # Create Widgets
        self.label_title = Label(self.parent, text="Customize the views.")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")
        
        self.show = Label(self.contentframe, text="Show")
        self.hide = Label(self.contentframe, text="Hide")
        self.proj= Label(self.contentframe, text="Project Navigation")
        self.diss = Label(self.contentframe, text="Dissector Building Area") 
        self.palette = Label(self.contentframe, text="Palette")
        self.packet = Label(self.contentframe, text="Packet Stream Area")
        self.disse = Label(self.contentframe, text="Dissected Stream Area")
        self.raw = Label(self.contentframe, text="Raw Data Area")
        self.console = Label(self.contentframe, text="Console Area")
        
        self.hide_proj = Radiobutton(self.contentframe, variable=OrganizeViews.proj_flag, value=0)
        self.show_proj = Radiobutton(self.contentframe, variable=OrganizeViews.proj_flag, value=1)
        self.hide_diss = Radiobutton(self.contentframe, variable=OrganizeViews.diss_flag, value=0)
        self.show_diss = Radiobutton(self.contentframe, variable=OrganizeViews.diss_flag, value=1)
        self.hide_palette = Radiobutton(self.contentframe, variable=OrganizeViews.palette_flag, value=0)
        self.show_palette = Radiobutton(self.contentframe, variable=OrganizeViews.palette_flag, value=1)
        self.hide_packet = Radiobutton(self.contentframe, variable=OrganizeViews.packet_flag, value=0)
        self.show_packet = Radiobutton(self.contentframe, variable=OrganizeViews.packet_flag, value=1)
        self.hide_disse = Radiobutton(self.contentframe, variable=OrganizeViews.disse_flag, value=0)
        self.show_disse = Radiobutton(self.contentframe, variable=OrganizeViews.disse_flag, value=1)
        self.hide_raw = Radiobutton(self.contentframe, variable=OrganizeViews.raw_flag, value=0)
        self.show_raw = Radiobutton(self.contentframe, variable=OrganizeViews.raw_flag, value=1)
        self.hide_console = Radiobutton(self.contentframe, variable=OrganizeViews.console_flag, value=0)
        self.show_console = Radiobutton(self.contentframe, variable=OrganizeViews.console_flag, value=1)
            
        self.btn_do = Button(self.parent, text='Generate', command=self.do_something)
        self.btn_cancel = Button(self.parent, text='Cancel', command=self.close_win)

        # Layout
        self.label_title.grid(row=0, column=0, columnspan=2, sticky='')
        self.contentframe.grid(row=1, column=0, columnspan=2, sticky='')
        
        self.show.grid(row=0, column=2, sticky='')
        self.hide.grid(row=0, column=1, sticky='')
        self.proj.grid(row=1, column=0, sticky='')
        self.diss.grid(row=2, column=0, sticky='')
        self.palette.grid(row=3, column=0, sticky='')
        self.packet.grid(row=4, column=0, sticky='')
        self.disse.grid(row=5, column=0, sticky='')
        self.raw.grid(row=6, column=0, sticky='')
        self.console.grid(row=7, column=0, sticky='')
        
        self.hide_proj.grid(row=1, column=1, sticky='')
        self.show_proj.grid(row=1, column=2, sticky='')
        self.hide_diss.grid(row=2, column=1, sticky='')
        self.show_diss.grid(row=2, column=2, sticky='')
        self.hide_palette.grid(row=3, column=1, sticky='')
        self.show_palette.grid(row=3, column=2, sticky='')
        self.hide_packet.grid(row=4, column=1, sticky='')
        self.show_packet.grid(row=4, column=2, sticky='')
        self.hide_disse.grid(row=5, column=1, sticky='')
        self.show_disse.grid(row=5, column=2, sticky='')
        self.hide_raw.grid(row=6, column=1, sticky='')
        self.show_raw.grid(row=6, column=2, sticky='')
        self.hide_console.grid(row=7, column=1, sticky='')
        self.show_console.grid(row=7, column=2, sticky='')

       
        self.btn_do.grid(row=2, column=0, sticky='e')
        self.btn_cancel.grid(row=2, column=1, sticky='e')

        # Padding
        for child in self.parent.winfo_children():
            child.grid_configure(padx=10, pady=5)
        for child in self.contentframe.winfo_children():
            child.grid_configure(padx=5, pady=2)
    
    def do_something(self):
        print(str(self.proj_flag.get()))
        print(str(self.diss_flag.get()))
        print(str(self.palette_flag.get()))
        print(str(self.packet_flag.get()))
        print(str(self.disse_flag.get()))
        print(str(self.raw_flag.get()))
        print(str(self.console_flag.get()))
        self.close_win()

class OpenPCAP(PopUp):
    """ New popup window """

    def init_gui(self):
        self.folder_path = ''
        self.parent.title("PCAP")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(3, weight=1)

        # Create Widgets
        self.label_title = ttk.Label(self.parent, text="Open a PCAP file")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")

        self.proj = ttk.Label(self.contentframe, text="Project")
        self.path_entry = EntryWithPlaceholder(self.contentframe, 'PCAP Name')
        self.browse_btn = Button(self.contentframe, text="Browse", command=self.browse)
        
        self.btn_do = Button(self.parent, text='Open', command=self.do_something)
        self.btn_cancel = Button(self.parent, text='Cancel', command=self.close_win)

        # Layout
        self.label_title.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.contentframe.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.proj.grid(row=0, column=0, sticky='ew')
        self.path_entry.grid(row=0, column=1, sticky='ew')
        #self.contentframe.columnconfigure(0, weight=1)
        self.browse_btn.grid(row=0, column=2, sticky='e')

        self.btn_do.grid(row=2, column=0, sticky='e')
        self.btn_cancel.grid(row=2, column=1, sticky='e')

        # Padding
        for child in self.parent.winfo_children():
            child.grid_configure(padx=10, pady=5)
        for child in self.contentframe.winfo_children():
            child.grid_configure(padx=5, pady=2)
    
    def browse(self):
        self.folder_path = tkFileDialog.askopenfilename()
        self.path_entry.put_text(self.folder_path)

    def do_something(self):
        self.folder_path = self.path_entry.get()
        if self.folder_path:
            self.close_win()
        else:
            print("Error: But for real though, field must not be empty.")
            
class EntryWithPlaceholder(object, Entry):
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




class ProjectExplorer(tk.Frame):
    def __init__(self, parent, path):
        tk.Frame.__init__(self, parent)
        self.root = parent
        self.tree = ttk.Treeview(self)
        ttk.Style().configure('Treeview', rowheight=40)
        ttk.Style().configure(".", font=('Helvetica', 12), foreground="")
        
        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text=path, anchor='w')

        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text='Workspace', open=True)
        self.process_directory(root_node, abspath)

        self.tree.pack(fill='both', expand=True)
        
#==============================================================================
#         self.tree.rowconfigure(1, weight=1)
#         self.tree.columnconfigure(1, weight=1)
#         
#         ysb.grid(row=0, column=1, sticky='ns')
#         xsb.grid(row=1, column=0, sticky='ew')
#==============================================================================
        #self.grid()

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)    
    
    def rebuild_tree(self, path):
        self.tree.delete(self.tree.get_children())
        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text='Workspace', open=True)
        self.process_directory(root_node, abspath)
    
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
 
 

class ToggledFrame(tk.Frame):

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
            self.sub_frame.pack(fill="both", expand=1)
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

class CustomButton(tk.Canvas):
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
#==============================================================================
#         self.bind("<ButtonPress-1>", self._on_press)
#         self.bind("<ButtonRelease-1>", self._on_release)
# 
#     def _on_press(self, event):
#         self.configure(relief="sunken")
# 
#     def _on_release(self, event):
#         self.configure(relief="raised")
#         if self.command is not None:
#             self.command()
#==============================================================================

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
            return
        if 'rect' in self.shape :
            label = tk.Label(canvas, text=self.name,
                                  borderwidth=2, relief="raised", padx=10, pady=10)    
        elif 'circular' in self.shape :
            label = CustomButton(canvas, 50, 50, 'grey')
            
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
   
        self.fields = ToggledFrame(self.pallete, text='Fields', relief="raised", borderwidth=1)
        self.fields.pack(fill="x", pady=2, padx=2, anchor="ne")
       
        self.constructs = ToggledFrame(self.pallete, text='Constructs', relief="raised", borderwidth=1)
        self.constructs.pack(fill="x", expand=1, pady=2, padx=2, anchor="ne")
        
        for r in range(4):
            self.rowconfigure(r, weight=1)
        for c in range(4):
            self.columnconfigure(c, weight=1)
        
        self.init_fields()

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
      
            
                          
        
        
#==============================================================================
#         self.pallete = tk.Frame(self)
#         
#         self.fields = ToggledFrame(self.pallete, text='Fields', relief="raised", borderwidth=1)
#         self.fields.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
#         
#         self.t2 = ToggledFrame(self.pallete, text='Constructs', relief="raised", borderwidth=1)
#         self.t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
#         
#         self.pallete.grid(row=1, column=1, sticky='ew')
#==============================================================================

# 
#     ttk.Label(t.sub_frame, text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
#     ttk.Entry(t.sub_frame).pack(side="left")
# 
#    
# 
#     for i in range(10):
#         ttk.Label(t2.sub_frame, text='Test' + str(i)).pack()
# 
#     t3 = ToggledFrame(root, text='Fooo', relief="raised", borderwidth=1)
#     t3.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
# 
#     for i in range(10):
#         ttk.Label(t3.sub_frame, text='Bar' + str(i)).pack()
        


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    GUI(root)
root.mainloop()