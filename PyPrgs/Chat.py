import tkinter as tk 
import tkinter.ttk as ttk 
import urllib.request 
import urllib.parse
from ttkthemes import ThemedTk
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
        # self.cb_Refresh = cb_Refresh
        # self.cb_Settings =cb_Settings
        # self.cb_Quit = cb_Quit

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
    def __init__(self, master = None): 
        ttk.Frame.__init__(self, master)

        self.inputField  = ttk.Entry(self)
        self.inputField.grid(row=0, column=0, sticky=tk.E+tk.W )

        self.btn_submit = ttk.Button(self, text="Submit") 
        self.btn_submit.grid(row=0, column=1, sticky=tk.E+tk.W)

        # textbar soll all den verfügbaren platz der row bekommen
        self.columnconfigure(0, weight=1)

class SettingsWindow(ttk.Frame):
    def __init__(self, master = None): 
        ttk.Frame.__init__(self,master)
        self.lbl_nickname=ttk.Label(self,text="Kuerzel")
        self.lbl_nickname.grid(row=0, column=0)
        self.entry_nickname = ttk.Entry(self, width=5)
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
        
        #title of window            
        self.wm_title("Hochschul Chat")

        #style 
        self.set_theme(theme)
        #print(self.get_themes()) # zeigt verfügbare themes 

        self.settings_open = False
        
        #Hintergrund 
        self.configure(background = "ghost white")
        self.update()

        self.create_widgets()

    def create_widgets(self):
        """
        Initialisierung und Bindung der Subframes.
        """
        #Buttonreihe oben   
        self.menubuttons = MenubuttonFrame(self,cb_Refresh= self.refresh,cb_Settings=self.toplevel_settings, cb_Quit=self.quit)
        self.menubuttons.grid(column=0, row=0, sticky=tk.W)

        #Großer Textview in der Mitte
        self.lbl_chatview = tk.Label(self, height=10, width=50)
        self.lbl_chatview.grid(column=0,row=1, sticky="nswe")

        # Submitbar unten
        self.inputBar = InputBar(self)
        self.inputBar.grid(column=0, row=2, sticky=tk.E+tk.W+tk.S)

        # row1 (chatview) braucht n weight für resize in y richtung
        # dann nimmt das label den extra space ein
        self.rowconfigure(1, weight=1)
        #alle rows brauchen weight für resize in x richtung
        self.columnconfigure(0,weight=1)
    


    def refresh(self):
        """Aktualisierung des Chatverlaufs"""
        msgs = self.chat_get()
        msgs = list(msgs.splitlines())
        msgs.reverse()
        #todo hier text box nachrichten löschen 
        for m in msgs: 
            #todo hier wieder nachrichten einfügen 
            self.lbl_chatview

    def toplevel_settings(self):
        if not self.settings_open:
            self.settings_open = True
            self.toplevel = tk.Toplevel(self)
            self.toplevel.overrideredirect(True)
            self.toplevel.title("Settings")
            self.top = SettingsWindow(self.toplevel)
            self.top.btn_ok["command"] = self.save_and_exit
            self.top.grid()
        
    def save_and_exit(self):
        self.settings_open = False
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

    def chat_post(self, msg, usr = "Anon"):
        """Neue Nachricht auf Server posten"""
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