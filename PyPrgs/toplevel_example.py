import tkinter as tk

root = tk.Tk() 

def start_toplevel():
    #you can make as many Toplevels as you like
    extra_window = tk.Toplevel(root)
    label2 = tk.Label(extra_window, text="""this is extra_window
    closing this will not affect root""")
    label2.pack()

#put a label in the root to identify the window.
label1 = tk.Label(root, text="""this is root
closing this window will shut down app""")
label1.pack()
btn = tk.Button(root, text="start toplevel", command=start_toplevel)
btn.pack()

root.mainloop()