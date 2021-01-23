import tkinter as tk 
import tkinter.ttk as ttk 
from ttkthemes import ThemedTk

class MenubuttonFrame(ttk.Frame): 

    def __init__(self, master = None): 
        ttk.Frame.__init__(self, master)

        btn_refresh  = ttk.Button(self, text="Refresh" )
        btn_refresh.grid(row=0, column=0)

        btn_settings = ttk.Button(self, text="Settings") 
        btn_settings.grid(row=0, column=1)
        
        btn_finish = ttk.Button(self, text="Quit" ) 
        btn_finish.grid(row=0, column=2)

class InputBar(ttk.Frame): 

    def __init__(self, master = None): 
        ttk.Frame.__init__(self, master)

        inputField  = ttk.Entry(self)
        inputField.grid(row=0, column=0, sticky=tk.E+tk.W )

        btn_submit = ttk.Button(self, text="Submit") 
        btn_submit.grid(row=0, column=1, sticky=tk.E+tk.W)
        
        self.columnconfigure(0, weight=1)
        

class Chat(ThemedTk): 
    
    def __init__(self, theme = 'default'): 
        ThemedTk.__init__(self)
        
        #title of window            
        self.wm_title("Hochschul Chat")

        #style 
        self.set_theme(theme)
        #print(self.get_themes()) # zeigt verfügbare themes 
        
        #Hintergrund 
        self.configure(background = "ghost white")
        self.update()

        #Buttonreihe oben   
        menubuttons = MenubuttonFrame(self)
        menubuttons.grid(column=0, row=0, sticky=tk.W)

        #Großer Textview in der Mitte
        chatview = tk.Label(self, height=10, width=50)
        chatview.grid(column=0,row=1, sticky="nswe")

        # Submitbar unten
        chatview = InputBar(self)
        chatview.grid(column=0, row=2, sticky=tk.E+tk.W+tk.S)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0,weight=1)

        



if __name__ == "__main__":
    chat = Chat(theme ="breeze")  #https://ttkthemes.readthedocs.io/en/latest/themes.html
    chat.mainloop()
    