import tkinter as tk 

import Frames


class Main_App(tk.Frame): 

    def __init__(self, master = None): 
        tk.Frame.__init__(self, master)

        #title of window            
        master.wm_title("Hochschul Chat")
        master.minsize(300,300)

        Buttons = Frames.Button_frm(self)
        Buttons.grid(row=0, column =0)

        self.pack(expand=True, fill= tk.BOTH)

    

if __name__ == "__main__":
    root = tk.Tk()
    main = Main_App(root) 
    root.mainloop()