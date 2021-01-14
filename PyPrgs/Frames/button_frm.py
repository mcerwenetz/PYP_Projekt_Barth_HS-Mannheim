import tkinter as tk 

class Button_frm(tk.Frame): 

    def __init__(self, master = None): 
        tk.Frame.__init__(self, master)

        refresh  = tk.Button(self, text="Refresh" ) 
        refresh.grid(row=0, column=0)

        settings = tk.Button(self, text="Settings" ) 
        settings.grid(row=0, column=1)
        
        beenden = tk.Button(self, text="Quit" ) 
        beenden.grid(row=0, column=2)
         