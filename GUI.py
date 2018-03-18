import Tkinter as tk
from Tkinter import * 

# Lots of tutorials have from tkinter import *, but that is pretty much always a bad idea
import ttk
import abc
import os
from PIL import ImageTk, Image
import Tkconstants, tkFileDialog


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
        
        self.Frame1 = tk.Frame(self.root, bg="grey")
        self.Frame2 = tk.Frame(self.root, bg="blue")
        self.Frame3 = tk.Frame(self.root, bg="green")
        self.Frame4 = tk.Frame(self.root, bg="brown")
        self.Frame5 = tk.Frame(self.root, bg="pink")
        self.Frame6 = tk.Frame(self.root, bg="white")
    
        self.menubar.grid(row=0, column=0, rowspan=1, columnspan=10, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.project_explorer.grid(row=1, column=0, rowspan=15, columnspan=2, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.Frame2.grid(row=1, column=2, rowspan=15, columnspan=8, sticky=(tk.N, tk.S, tk.W, tk.E))
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
 
 
#==============================================================================
# 
# class ToggledFrame(tk.Frame):
# 
#     def __init__(self, parent, text="", *args, **options):
#         tk.Frame.__init__(self, parent, *args, **options)
# 
#         self.show = tk.IntVar()
#         self.show.set(0)
# 
#         self.title_frame = ttk.Frame(self)
#         self.title_frame.pack(fill="x", expand=1)
# 
#         ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)
# 
#         self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
#                                             variable=self.show, style='Toolbutton')
#         self.toggle_button.pack(side="left")
# 
#         self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
# 
#     def toggle(self):
#         if bool(self.show.get()):
#             self.sub_frame.pack(fill="x", expand=1)
#             self.toggle_button.configure(text='-')
#         else:
#             self.sub_frame.forget()
#             self.toggle_button.configure(text='+')
# 
# 
# if __name__ == "__main__":
#     root = tk.Tk()
# 
#     t = ToggledFrame(root, text='Rotate', relief="raised", borderwidth=1)
#     t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
# 
#     ttk.Label(t.sub_frame, text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
#     ttk.Entry(t.sub_frame).pack(side="left")
# 
#     t2 = ToggledFrame(root, text='Resize', relief="raised", borderwidth=1)
#     t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
# 
#     for i in range(10):
#         ttk.Label(t2.sub_frame, text='Test' + str(i)).pack()
# 
#     t3 = ToggledFrame(root, text='Fooo', relief="raised", borderwidth=1)
#     t3.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
# 
#     for i in range(10):
#         ttk.Label(t3.sub_frame, text='Bar' + str(i)).pack()
#==============================================================================


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
        


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    GUI(root)
root.mainloop()