import Tkinter as tk

# Lots of tutorials have from tkinter import *, but that is pretty much always a bad idea
import ttk
import os
import tkFont
from Menu import Menubar
from Menu import WorkspaceLauncher
from BuildingArea import BuildingArea
from Menu import OrganizeViews
from CustomWidgets import HeaderFrame

            
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
        self.init_variables()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(str(self.screen_width)+"x"+str(self.screen_height))#"1200x800")
        
        self.project_explorer = ProjectExplorer(self.root, workspace_path, 'Project Explorer')
        self.menubar = Menubar(self.root, workspace_path, self.project_explorer, self.building_area)
        self.building_area = BuildingArea(self.root, 'Dissector Builder Area')
        self.tabs = Tabs(self.root)
        
        self.menubar.grid(row=0, column=0, rowspan=1, columnspan=10, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.project_explorer.grid(row=1, column=0, rowspan=15, columnspan=2, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.building_area.grid(row=1, column=2, rowspan=15, columnspan=8, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.tabs.grid(row=16, column=0, rowspan=4, columnspan=10, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        for r in range(20):
            self.root.rowconfigure(r, weight=1)
        for c in range(10):
            self.root.columnconfigure(c, weight=1)
        
    def init_variables(self):
        OrganizeViews.proj_flag = tk.IntVar(value=1)
        OrganizeViews.diss_flag = tk.IntVar(value=1)
        OrganizeViews.palette_flag = tk.IntVar(value=1)
        OrganizeViews.packet_flag = tk.IntVar(value=1)
        OrganizeViews.disse_flag = tk.IntVar(value=1)
        OrganizeViews.raw_flag = tk.IntVar(value=1)
        OrganizeViews.console_flag = tk.IntVar(value=1)


class ProjectExplorer(HeaderFrame):
    def __init__(self, parent, path, text):
        HeaderFrame.__init__(self, parent, text)
        self.root = parent
        self.tree = ttk.Treeview(self.sub_frame)
        
        ttk.Style().configure(".", font=('Helvetica', 12), foreground="")
        
        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text=path, anchor='w')

        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text='Workspace', open=True)
        self.process_directory(root_node, abspath)

        self.tree.pack(fill='both', expand=1)

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
    
    def close(self):
        OrganizeViews.proj_flag.set(0)
        self.grid_forget() 
    
    def show_exp(self):
        self.grid(row=1, column=0, rowspan=15, columnspan=2, sticky=(tk.N, tk.S, tk.W, tk.E))
        
    
class Tabs(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        blue = "#B4CEE3"
        myred = "#B4CEE3"

        style = ttk.Style()
        
        style.theme_create( "MyStyle", parent="alt", settings={
                "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
                "TNotebook.Tab": {
                    "configure": {"padding": [50, 30], "background": blue },
                    "map":       {"background": [("selected", myred)],
                                  "expand": [("selected", [1, 1, 1, 0])] } } } )
                                  
        f = tkFont.Font(family='helvetica', weight=tkFont.BOLD, size=12)
        style.theme_use("MyStyle")
        style.configure('Treeview', rowheight=40)
        style.configure('.', font=f)
        # gives weight to the cells in the grid
        rows = 0
        while rows < 4:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows += 1
         
        # Defines and places the notebook widget
        self.nb = ttk.Notebook(self)
        self.nb.grid(row=0, column=0, columnspan=4, rowspan=5, sticky='NESW')
        
        # Adds tab 1 of the notebook
        self.init_raw_data()
        self.init_packet_stream()
        self.init_dissected_area()
        self.init_console()
        
    def init_dissected_area(self):
        self.dissected = tk.Frame(self.nb)
        self.tree = ttk.Treeview(self.dissected)
        root_node = self.tree.insert('', 'end', text='User DataGram Protocol, Src Port: domain (53), Dst', open=True)
        domain = self.tree.insert('', 'end', text='Domain Name System (response)', open=True)
        self.tree.insert(domain, 'end', text='[Request in: 381]', open=True)
        self.tree.insert(domain, 'end', text='Transaction ID: 0x6f54', open=True)        
        self.tree.insert(domain, 'end', text='Flags: 0x874 (Standard query response, No error)', open=True)        
        self.tree.insert(domain, 'end', text='Question: 1', open=True)   
        self.tree.insert(domain, 'end', text='Answer RRs: 6', open=True)
        self.tree.insert(domain, 'end', text='Authority: 0', open=True)        
        self.tree.insert(domain, 'end', text='Additional RRs: 0', open=True)        
        queries = self.tree.insert(domain, 'end', text='Queries', open=True) 
        stuff = self.tree.insert(queries, 'end', text='www.cnn.com: type A', open=True)
        self.tree.insert(stuff, 'end', text='Name: ww.cnn.com', open=True)
        self.tree.insert(stuff, 'end', text='Type: A(Host)', open=True)
        self.tree.insert(stuff, 'end', text='Class: IN', open=True)
        
        self.tree.pack(fill='both', expand=1)
        self.nb.add(self.dissected, text='Dissected Packet Area') 
        
    def init_console(self):
        self.console = tk.Frame(self.nb)
        tk.Label(self.console, text='No Error Found').pack(side='left')
        
        self.nb.add(self.console, text='Console') 
        
    def init_raw_data(self):
        self.raw_tab = tk.Frame(self.nb)
        
        tk.Label(self.raw_tab, text="f6 a3 3d cb f7 64 9c b6  d0 d6 5f 77 08 00 45 00   ...=..d.. .._w..E").grid(row=0, column=0)
        tk.Label(self.raw_tab, text="f6 a3 3d cb f7 64 9c b6  d0 d6 5f 77 08 00 45 00   ...=..d.. .._w..E").grid(row=1, column=0)
        tk.Label(self.raw_tab, text="f6 a3 3d cb f7 64 9c b6  d0 d6 5f 77 08 00 45 00   ...=..d.. .._w..E").grid(row=2, column=0)
        tk.Label(self.raw_tab, text="f6 a3 3d cb f7 64 9c b6  d0 d6 5f 77 08 00 45 00   ...=..d.. .._w..E").grid(row=3, column=0)
        tk.Label(self.raw_tab, text="f6 a3 3d cb f7 64 9c b6  d0 d6 5f 77 08 00 45 00   ...=..d.. .._w..E").grid(row=4, column=0)
        tk.Label(self.raw_tab, text="f6 a3 3d cb f7 64 9c b6  d0 d6 5f 77 08 00 45 00   ...=..d.. .._w..E").grid(row=5, column=0)
        tk.Label(self.raw_tab, text="f6 a3 3d cb f7 64 9c b6  d0 d6 5f 77 08 00 45 00   ...=..d.. .._w..E").grid(row=6, column=0)
        tk.Label(self.raw_tab, text="f6 a3 3d cb f7 64 9c b6  d0 d6 5f 77 08 00 45 00   ...=..d.. .._w..E").grid(row=7, column=0)
                                          
        self.nb.add(self.raw_tab, text='Raw Data Area')         
        
    def init_packet_stream(self):
        self.packet_tab = tk.Frame(self.nb)
        self.nb.add(self.packet_tab, text='Packet Stream Area') 
        
        labels = [
                    tk.Label(self.packet_tab, text='No', anchor='w', padx=10),
                    tk.Label(self.packet_tab, text='Time', anchor='w', padx=10),
                    tk.Label(self.packet_tab, text='Source', anchor='w', padx=10),
                    tk.Label(self.packet_tab, text='Destination', anchor='w', padx=10),
                    tk.Label(self.packet_tab, text='Protocol', anchor='w', padx=10),
                    tk.Label(self.packet_tab, text='Info', anchor='w', padx=10),

                    tk.Label(self.packet_tab, text='366', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='11.767290', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='TSLv 1.2', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='631 -> 60224 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1386 WS=32 TSval=1000097195 TSecr=3959397636 SACK_PERM=1', anchor='w', padx=10, bg='lightgreen'),
                    
                    tk.Label(self.packet_tab, text='367', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='11.767290', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='TSLv 1.2', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='631 -> 60224 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1386 WS=32 TSval=1000097195 TSecr=3959397636 SACK_PERM=1', anchor='w', padx=10, bg='lightgreen'),
                    
                    tk.Label(self.packet_tab, text='368', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='11.767290', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='TSLv 1.2', anchor='w', padx=10, bg='lightgreen'),
                    tk.Label(self.packet_tab, text='631 -> 60224 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1386 WS=32 TSval=1000097195 TSecr=3959397636 SACK_PERM=1', anchor='w', padx=10, bg='lightgreen'),
                    
                    tk.Label(self.packet_tab, text='369', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='11.767290', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='TSLv 1.2', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='631 -> 60224 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1386 WS=32 TSval=1000097195 TSecr=3959397636 SACK_PERM=1', anchor='w', padx=10, bg='#ff8772'),
                    
                    tk.Label(self.packet_tab, text='370', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='11.767290', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='TSLv 1.2', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='631 -> 60224 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1386 WS=32 TSval=1000097195 TSecr=3959397636 SACK_PERM=1', anchor='w', padx=10, bg='#ff8772'),

                    tk.Label(self.packet_tab, text='371', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='11.767290', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='192.168.0.31', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='TSLv 1.2', anchor='w', padx=10, bg='#ff8772'),
                    tk.Label(self.packet_tab, text='631 -> 60224 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1386 WS=32 TSval=1000097195 TSecr=3959397636 SACK_PERM=1', anchor='w', padx=10, bg='#ff8772'),
        ]
                    
        for i in range(0, 6):
            labels[i].grid(row=0, column=i)
            labels[i+6].grid(row=1, column=i)
            labels[i+(6*2)].grid(row=2, column=i)
            labels[i+(6*3)].grid(row=3, column=i)
            labels[i+6*4].grid(row=4, column=i)
            labels[i+(6*5)].grid(row=5, column=i)
            labels[i+(6*6)].grid(row=6, column=i)
        
#==============================================================================
#         for r in range(6):
#             self.rowconfigure(r, weight=1)
#         for c in range(6):
#             self.columnconfigure(c, weight=1)
#==============================================================================
        

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    GUI(root)
root.mainloop()