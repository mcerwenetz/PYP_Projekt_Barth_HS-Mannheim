import tkinter as tk 
import tkinter.ttk as ttk 
from ttkthemes import ThemedTk

import urllib.request 
import urllib.parse


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

        self.create_widgets()

    def create_widgets(self): 
        #Buttonreihe oben   
        refresh_btn  = ttk.Button(self, text="Refresh", command =self.refresh)
        refresh_btn.grid(row=0, column=0)

        settings_btn = ttk.Button(self, text="Settings") 
        settings_btn.grid(row=0, column=1)
        
        def quit_cmd(): 
            self.destroy()
        quit_btn = ttk.Button(self, text="Quit", command=quit_cmd ) 
        quit_btn.grid(row=0, column=2)

    def refresh(self): 
        msgs = chat_get()
        msgs = list(msgs.splitlines())
        msgs.reverse()
        #todo hier text box nachrichten löschen 
        for m in msgs: 
            #todo hier wieder nachrichten einfügen 
            print(m)



#GET/POST Stuff 

CHAT_URL = "https://pma.inftech.hs-mannheim.de/wsgi/chat"

def chat_get():
    resp = urllib.request.urlopen(CHAT_URL)
    if not resp.status==200: 
        return None
    return resp.read().decode("UTF-8")

def chat_post(msg, usr = "Anon"):
    msg = "["+usr+"] " + msg 
    data = msg.encode("UTF-8")
    
    req = urllib.request.Request(CHAT_URL, data = data)
    req.add_header("Content-Type", "text/plain")
    
    resp = urllib.request.urlopen(req)
    if not 200 <= resp.status <= 299:  
        return None
    return resp.read().decode("UTF-8")



if __name__ == "__main__":
    chat = Chat(theme ="breeze")  #https://ttkthemes.readthedocs.io/en/latest/themes.html
    chat.mainloop()