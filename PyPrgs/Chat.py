import tkinter as tk 
import tkinter.ttk as ttk 
from ttkthemes import ThemedTk

class Button_frm(ttk.Frame): 

    def __init__(self, master = None): 
        ttk.Frame.__init__(self, master)

        refresh  = ttk.Button(self, text="Refresh" )
        refresh.grid(row=0, column=0)

        settings = ttk.Button(self, text="Settings") 
        settings.grid(row=0, column=1)
        
        beenden = ttk.Button(self, text="Quit" ) 
        beenden.grid(row=0, column=2)
         


class Chat(ThemedTk): 
    
    def __init__(self, theme = 'default'): 
        ThemedTk.__init__(self)
        
        #title of window            
        self.wm_title("Hochschul Chat")
        
        #mindest Größe
        self.minsize(800,300)
        
        #style 
        self.set_theme(theme)
        #print(self.get_themes()) # zeigt verfügbare themes 
        
        #Hintergrund 
        self.configure(background = "ghost white")
        self.update()

        #Buttonreihe oben   
        Buttons = Button_frm(self)
        Buttons.grid(row=0, column =0)
     
    

if __name__ == "__main__":
    chat = Chat(theme ="breeze")  #https://ttkthemes.readthedocs.io/en/latest/themes.html
    chat.mainloop()
    