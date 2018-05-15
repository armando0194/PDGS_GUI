import Tkinter as tk

def draw(event):
    x, y = event.x, event.y
    if canvas.old_coords:
        x1, y1 = canvas.old_coords
        canvas.create_line(x, y, x1, y1)
    canvas.old_coords = x, y

def draw_line(event):
    print str(event.type)
    if str(event.type) in '4':
        canvas.old_coords = event.x, event.y

    elif str(event.type) in '5':
        x, y = event.x, event.y
        x1, y1 = canvas.old_coords
        canvas.create_line(x, y, x1, y1, arrow="first")

def reset_coords(event):
    canvas.old_coords = None

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
canvas.old_coords = None

root.bind('<ButtonPress-1>', draw_line)
root.bind('<ButtonRelease-1>', draw_line)

#root.bind('<B1-Motion>', draw)
#root.bind('<ButtonRelease-1>', reset_coords)

root.mainloop()