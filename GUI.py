import Tkinter as tk

# Lots of tutorials have from tkinter import *, but that is pretty much always a bad idea
import ttk
import os
from Menu import Menubar
from Menu import WorkspaceLauncher
from BuildingArea import BuildingArea



            
class GUI(tk.Frame):
    """Main GUI class"""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.option_add('*font', ('verdana', 12, 'bold'))
        self.openwindow()

    def openwindow(self):
        self.new_win = tk.Toplevel(self.root) # Set parent
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



if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    GUI(root)
root.mainloop()