import tkinter as tk 
import tkinter.ttk as ttk 
import urllib.request 
import urllib.parse
from ttkthemes import ThemedTk
from threading import Thread 
from time import sleep 

CHAT_URL = "https://pma.inftech.hs-mannheim.de/wsgi/chat"

class MenubuttonFrame(ttk.Frame):
    """Dieses Frame ist oben im Chatfenster.

    Attributes
    -------------
    btn_refresh : ttk.Button
        Wenn man diesen Button drückt wird der Chat manuell
        aktualisiert.
    
    btn_settings : ttk.Button
        Wenn man diesen Button drückt werden die Einstellungen
        als Toplevel gestartet.
    
    btn_finish : ttk.Button
        Wenn man diesen Button drückt wird das Programm beendet.


    Methods
    --------
    
    quit_cmd(self)
        Schließt das Chatfenster

    refresh(self)
        Aktualisiert den Chatverlauf
    """
    def __init__(self, master = None, cb_Refresh=None, cb_Settings=None, cb_Quit=None): 
        ttk.Frame.__init__(self, master)

        self.btn_refresh  = ttk.Button(self, text="Refresh", command=cb_Refresh)
        self.btn_refresh.grid(row=0, column=0)

        self.btn_settings = ttk.Button(self, text="Settings", command=cb_Settings) 
        self.btn_settings.grid(row=0, column=1)
        
        self.btn_finish = ttk.Button(self, text="Quit", command=cb_Quit) 
        self.btn_finish.grid(row=0, column=2)


class InputBar(ttk.Frame):
    """
    Dieses Frame ist die Eingabezeile unten im Chat.

    Attributes
    ------------
    inputField : ttk.Entry
        Das Haupteingabefeld für den Chat

    btn_submit : ttk.Entry
        Wenn man diesen Button drückt wird der Inhalt des inputFields
        geposted
    """
    def __init__(self, master = None, cb_post=None): 
        ttk.Frame.__init__(self, master)

        def post(self): 
            cb_post()

        self.inputField  = ttk.Entry(self)
        self.inputField.grid(row=0, column=0, sticky=tk.E+tk.W )
        self.inputField.bind("<Return>", post)

        self.btn_submit = ttk.Button(self, text="Submit", command=cb_post) 
        self.btn_submit.grid(row=0, column=1, sticky=tk.E+tk.W)

        # textbar soll all den verfügbaren platz der row bekommen
        self.columnconfigure(0, weight=1)
    
    def get_msg(self): 
        msg = self.inputField.get()
        self.inputField.delete(0, tk.END)
        return msg

class SettingsWindow(ttk.Frame):
    def __init__(self, master = None): 
        ttk.Frame.__init__(self,master)
        self.lbl_nickname=ttk.Label(self,text="Nickname")
        self.lbl_nickname.grid(row=0, column=0)
        self.entry_nickname = ttk.Entry(self, width=10)
        self.entry_nickname.grid(row=0, column=1)
        
        self.lbl_auto_refresh=ttk.Label(self,text="auto refresh")
        self.lbl_auto_refresh.grid(row=1, column=0)
        self.chkbtn_autoupdate=ttk.Checkbutton(self)
        self.chkbtn_autoupdate.grid(row=1, column=1)

        self.btn_cancel=ttk.Button(self, text="Cancel")
        self.btn_cancel.grid(row=2, column=0)
        self.btn_ok=ttk.Button(self, text="Ok")
        self.btn_ok.grid(row=2,column=1)



class Chat(ThemedTk):
    """
    Hauptklasse des Chats. Das Mainframe in dem alle Unterframes gebunden
    werden.
    
    Attributes
    -----------
    menubuttons : MenubuttonFrame
        Die Menubuttons oben im Chat (Refresh, Close, Settings)

    lbl_chatview : tk.Label
        Der Chatverlauf

    inputBar : InputBar
        Die Eingabezeile unten.

    Methods
    -----------
    create_widgets(self)
        Diese Methode erstellt alle Frames und Widgets
        im Chatfenster.

    chat_get(self)
        Holt den Chatverlauf vom Server

    chat_post(msg, usr = "Anon")
        Posted einen String, die Message, auf den Server mit
        unter dem username usr
        default ist Anon.
    """
    def __init__(self, theme = 'default'):
        """
        Initialisierung des Mainframes.
        Stylekonfiguration
        Initialisierung und bindung der Subframes.
        Parameters
        ----------
        theme : str, optional, default='default'
            Das ttk Theme.
        """
        ThemedTk.__init__(self)
        self.nickname= "Anon"
                
        #title of window            
        self.wm_title("Hochschul Chat")

        #style 
        self.set_theme(theme)
        #print(self.get_themes()) # zeigt verfügbare themes 

        self.settings_already_opend = False
        
        #Hintergrund 
        self.configure(background = "ghost white")
        self.update()

        self.create_widgets()

        #tk variable für die settings. wir brauchen zwei variabeln weil wenn
        # wir im thread auf die tk variable prüfen
        # kann es sein dass der thread startet oder stoppt bevor ok gedrückt
        # wurde und das wäre nicht userfreundlich und könnte problematisch werden
        self.auto_refresh_checked_settings = tk.BooleanVar()
        self.auto_refresh_checked_settings.set(False)
        # Die gesonderte Threadvariable. Der Thread checkt hier ob er wirklich noch
        # refreshen soll. wird nur verändert durch ein drücken auf ok in den settings
        self.keep_refreshing = False

        self.auto_update_thread = Thread(target=self.run_auto_update)

    def create_widgets(self):
        """
        Initialisierung und Bindung der Subframes.
        """
        #Buttonreihe oben   
        self.menubuttons = MenubuttonFrame(self,cb_Refresh= self.refresh,
        cb_Settings=self.toplevel_settings, cb_Quit=self.quit)
        self.menubuttons.grid(column=0, row=0, sticky=tk.W)

        #Großer Textview in der Mitte + scrollbar
        self.chatbox = tk.Text(self, height=10, width=50) 
        self.chatbox.grid(column=0,row=1, sticky="nswe")
        self.chatbox.configure(state='disabled')
        self.refresh()
        
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.grid(column=1,row=1, sticky= tk.N+tk.S)
        self.scrollbar["command"] = self.chatbox.yview
        self.chatbox["yscrollcommand"] = self.scrollbar.set

        # Submitbar unten
        self.inputBar = InputBar(self, cb_post=self.chat_post)
        self.inputBar.grid(column=0, row=2, columnspan=2,sticky=tk.E+tk.W+tk.S)

        # row1 (chatview) braucht n weight für resize in y richtung
        # dann nimmt das label den extra space ein
        self.rowconfigure(1, weight=1)
        #alle rows brauchen weight für resize in x richtung
        self.columnconfigure(0,weight=1)
    


    def refresh(self):
        """Aktualisierung des Chatverlaufs"""
        msgs = list(self.chat_get().splitlines())
        msgs = reversed(msgs)

        #textfeld soll read only sein
        self.chatbox.configure(state='normal')
        self.chatbox.delete(1.0, 'end')
       
        for m in msgs: 
            self.chatbox.insert('end', m +"\n" )
    
        self.chatbox.see('end')
        self.chatbox.configure(state='disabled') 

        
    def toplevel_settings(self):
        """SettingsToplevel dass dann SettingsWindow übergeben wird. Kann nur einmal
        geöffnet werden."""
        if not self.settings_already_opend:
            self.settings_already_opend = True
            self.toplevel = tk.Toplevel(self)
            self.toplevel.title("Settings")
            self.top = SettingsWindow(self.toplevel)
            self.top.btn_ok["command"] = self.save_and_exit
            self.top.btn_cancel["command"] = self.cancel_and_exit
            self.top.grid()
            self.top.chkbtn_autoupdate["variable"] = self.auto_refresh_checked_settings
            #Wenn das Window über Window Decoration geschlossen wird soll auch
            #das settings_open flag resettet werden.
            #sonst gehen ja keine Fenster mehr auf
            self.toplevel.protocol("WM_DELETE_WINDOW", self.cancel_and_exit)

        
    def save_and_exit(self):
        "methode die gerufen wird wenn ok in den Settings ok gedrückt wurde"
        self.settings_already_opend = False
        self.nickname = self.top.entry_nickname.get()
        auto_update = self.auto_refresh_checked_settings.get()
        if(auto_update and not self.auto_update_thread.is_alive()):
            self.start_auto_update()
        elif(not auto_update):
            self.stop_auto_update()
        self.toplevel.destroy()


    def cancel_and_exit(self):
        "methode die gerufen wird wenn ok in den Settings cancel gedrückt wurde"
        self.settings_already_opend = False
        self.toplevel.destroy()

    def quit(self):
        """Beenden des Mainframes."""
        self.destroy()
    

    def chat_get(self):
        """Chatverlauf von Server holen."""
        resp = urllib.request.urlopen(CHAT_URL)
        if not resp.status==200: 
            return None
        return resp.read().decode("UTF-8")

    def chat_post(self):
        """Neue Nachricht auf Server posten"""
        msg = "["+self.nickname+"] " + self.inputBar.get_msg() 
        data = msg.encode("UTF-8")
    
        req = urllib.request.Request(CHAT_URL, data = data)
        req.add_header("Content-Type", "text/plain")

        urllib.request.urlopen(req)
        self.refresh()

    def run_auto_update(self):
        """callable für den auto refresh thread"""
        while self.keep_refreshing == True: 
            self.refresh() 
            sleep(3)

    def start_auto_update(self):
        """startet den auto refresh thread"""
        self.keep_refreshing = True
        self.auto_update_thread.start() 

    def stop_auto_update(self): 
        """stoppt den auto refresh thread"""
        self.keep_refreshing = False


if __name__ == "__main__":
    chat = Chat(theme ="breeze")  #https://ttkthemes.readthedocs.io/en/latest/themes.html
    chat.mainloop()