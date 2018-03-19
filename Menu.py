import Tkinter as tk
import abc
import ttk
import tkFileDialog
import  os
from CustomWidgets import EntryWithPlaceholder 

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
        self.new_proj_win = tk.Toplevel(self.root) # Set parent
        NewProject(self.new_proj_win, self)
    
    def generate_dissector(self):
        self.gen_diss_win = tk.Toplevel(self.root) # Set parent
        DissectorGenerator(self.gen_diss_win, self)
        
    def proj_import(self):
        self.proj_import_win = tk.Toplevel(self.root) # Set parent
        ProjectImport(self.proj_import_win, self)
    
    def proj_export(self):
        self.proj_export_win = tk.Toplevel(self.root) # Set parent
        ProjectExport(self.proj_export_win, self)
        
    def org_views(self):
        self.org_views_win = tk.Toplevel(self.root) # Set parent
        OrganizeViews(self.org_views_win, self)
    
    def open_pcap(self):
        self.open_pcap_win = tk.Toplevel(self.root) # Set parent
        OpenPCAP(self.open_pcap_win, self)
        
    def rebuild_tree(self, path):
        self.project_explorer.rebuild_tree(path)

    def init_menubar(self):
        self.label_title = tk.Label(self, text="Protocol Dissector Generator System", font=("Helvetica", 18, 'bold'))
        self.label_title.grid(row=0, column=0, columnspan=10)
        
        # Create Widgets
        self.btns = [tk.Button(self, text='Create Project', command=self.new_project),
                     tk.Button(self, text='Save Project'),
                     tk.Button(self, text='Close Project'),
                     tk.Button(self, text='Switch Workspace'),
                     tk.Button(self, text='Import Project', command=self.proj_import),
                     tk.Button(self, text='Export Project', command=self.proj_export),
                     tk.Button(self, text='Generate Dissector Script', command=self.generate_dissector),
                     tk.Button(self, text='Organize Views', command=self.org_views),
                     tk.Button(self, text='Open PCAP', command=self.open_pcap)]                   
       
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
        self.browse_btn = tk.Button(self.contentframe, text="Browse", command=self.browse)
        
        self.btn_do = tk.Button(self.parent, text='Launch', command=self.do_something)
        self.btn_cancel = tk.Button(self.parent, text='Cancel', command=self.close_win)

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
        self.label_title = tk.Label(self.parent, text="Create a new project")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")
        
        self.proj_name = tk.Label(self.contentframe, text="Project Name: ")
        self.proj_name_entry = EntryWithPlaceholder(self.contentframe, 'Project Name')
        self.proj_desc = tk.Label(self.contentframe, text="Project Description:")
        self.proj_desc_entry = tk.Text(self.contentframe, height=5)
        
        self.btn_do = tk.Button(self.parent, text='Create', command=self.do_something)
        self.btn_cancel = tk.Button(self.parent, text='Cancel', command=self.close_win)

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
        self.label_title = tk.Label(self.parent, text="Generate a custom dissector script from a selected project")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")
        
        self.proj_name = tk.Label(self.contentframe, text="Project: ")
        self.format = tk.Label(self.contentframe, text="Dissector Format: ")
        self.save_path = tk.Label(self.contentframe, text="Save Location: ")
        
        self.variable = tk.StringVar(self.contentframe)
        self.variable.set(self.FORMAT_OPTIONS[0]) # default value
        self.format_dropdown = tk.OptionMenu(self.contentframe, self.variable, *self.FORMAT_OPTIONS)
       
        self.proj_path_entry = EntryWithPlaceholder(self.contentframe, 'Project Name')
        self.proj_browse_btn = tk.Button(self.contentframe, text="Browse", command=self.browse_proj)
        
        self.save_path_entry = EntryWithPlaceholder(self.contentframe, 'Local File System Path')
        self.save_browse_btn = tk.Button(self.contentframe, text="Browse", command=self.browse_save)
           
        self.btn_do = tk.Button(self.parent, text='Generate', command=self.do_something)
        self.btn_cancel = tk.Button(self.parent, text='Cancel', command=self.close_win)

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
        self.browse_btn = tk.Button(self.contentframe, text="Browse", command=self.browse)
        
        self.btn_do = tk.Button(self.parent, text='Import', command=self.do_something)
        self.btn_cancel = tk.Button(self.parent, text='Cancel', command=self.close_win)

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
        self.label_title = tk.Label(self.parent, text="Export a project to the local system.")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")
        
        self.proj_name = tk.Label(self.contentframe, text="Project: ")
        self.proj_path_entry = EntryWithPlaceholder(self.contentframe, 'Project Name')
        self.proj_browse_btn = tk.Button(self.contentframe, text="Browse", command=self.browse_proj)
        
        self.format = tk.Label(self.contentframe, text="To Export File: ")
        self.save_path_entry = EntryWithPlaceholder(self.contentframe, 'Local File System Path')
        self.save_browse_btn = tk.Button(self.contentframe, text="Browse", command=self.browse_save)
           
        self.btn_do = tk.Button(self.parent, text='Generate', command=self.do_something)
        self.btn_cancel = tk.Button(self.parent, text='Cancel', command=self.close_win)

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
            OrganizeViews.proj_flag = tk.IntVar(value=1)
            OrganizeViews.diss_flag = tk.IntVar(value=1)
            OrganizeViews.palette_flag = tk.IntVar(value=1)
            OrganizeViews.packet_flag = tk.IntVar(value=1)
            OrganizeViews.disse_flag = tk.IntVar(value=1)
            OrganizeViews.raw_flag = tk.IntVar(value=1)
            OrganizeViews.console_flag = tk.IntVar(value=1)
        
        self.parent.title("Organize Views")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(3, weight=1)

        # Create Widgets
        self.label_title = tk.Label(self.parent, text="Customize the views.")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")
        
        self.show = tk.Label(self.contentframe, text="Show")
        self.hide = tk.Label(self.contentframe, text="Hide")
        self.proj= tk.Label(self.contentframe, text="Project Navigation")
        self.diss = tk.Label(self.contentframe, text="Dissector Building Area") 
        self.palette = tk.Label(self.contentframe, text="Palette")
        self.packet = tk.Label(self.contentframe, text="Packet Stream Area")
        self.disse = tk.Label(self.contentframe, text="Dissected Stream Area")
        self.raw = tk.Label(self.contentframe, text="Raw Data Area")
        self.console = tk.Label(self.contentframe, text="Console Area")
        
        self.hide_proj = tk.Radiobutton(self.contentframe, variable=OrganizeViews.proj_flag, value=0)
        self.show_proj = tk.Radiobutton(self.contentframe, variable=OrganizeViews.proj_flag, value=1)
        self.hide_diss = tk.Radiobutton(self.contentframe, variable=OrganizeViews.diss_flag, value=0)
        self.show_diss = tk.Radiobutton(self.contentframe, variable=OrganizeViews.diss_flag, value=1)
        self.hide_palette = tk.Radiobutton(self.contentframe, variable=OrganizeViews.palette_flag, value=0)
        self.show_palette = tk.Radiobutton(self.contentframe, variable=OrganizeViews.palette_flag, value=1)
        self.hide_packet = tk.Radiobutton(self.contentframe, variable=OrganizeViews.packet_flag, value=0)
        self.show_packet = tk.Radiobutton(self.contentframe, variable=OrganizeViews.packet_flag, value=1)
        self.hide_disse = tk.Radiobutton(self.contentframe, variable=OrganizeViews.disse_flag, value=0)
        self.show_disse = tk.Radiobutton(self.contentframe, variable=OrganizeViews.disse_flag, value=1)
        self.hide_raw = tk.Radiobutton(self.contentframe, variable=OrganizeViews.raw_flag, value=0)
        self.show_raw = tk.Radiobutton(self.contentframe, variable=OrganizeViews.raw_flag, value=1)
        self.hide_console = tk.Radiobutton(self.contentframe, variable=OrganizeViews.console_flag, value=0)
        self.show_console = tk.Radiobutton(self.contentframe, variable=OrganizeViews.console_flag, value=1)
            
        self.btn_do = tk.Button(self.parent, text='Generate', command=self.do_something)
        self.btn_cancel = tk.Button(self.parent, text='Cancel', command=self.close_win)

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
        self.browse_btn = tk.Button(self.contentframe, text="Browse", command=self.browse)
        
        self.btn_do = tk.Button(self.parent, text='Open', command=self.do_something)
        self.btn_cancel = tk.Button(self.parent, text='Cancel', command=self.close_win)

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