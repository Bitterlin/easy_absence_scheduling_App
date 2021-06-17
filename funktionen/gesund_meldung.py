import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import sys
import time
import datetime
from datetime import date
from datetime import datetime
import locale  
import getpass
from functools import partial 
from pathlib import Path

from funktionen.send_mail import *

""" Der mitarbeiter wird für die LS gesund geschrieben """
def ges_mel(dsatz):
    dsatz = dsatz

    root_gesund = tk.Tk()

    text_überschrift = f"{dsatz[1]} {dsatz[2]} meldet sich gesund."
    root_gesund.title(text_überschrift)
    # root_gesund.geometry("1x700+0+0")
    root_gesund.deiconify()  # info .deconifiy zum maximieren und .iconify zum minimieren.
    w=1000
    h=700
    root_gesund.geometry("%dx%d+250+80" % (w, h))
    root_gesund.configure(bg='green')
    root_gesund.focus_set()
    size_n = Font(family="Verdana", size="12")
    size_x = Font(family="Verdana", size="14", weight="bold")
    size_xx = Font(family="Verdana", size="16", weight="bold")
    size_xxx = Font(family="Verdana", size="20", weight="bold")
    # ---e---

    """ für Mailfunktion import von win Sys """
    try:
        import win32com.client as win32
    except:
        messagebox.showwarning("Problem erkannt", "Die Mailfunktion ist inaktiv! Sorry")

    """ Alle Bilder und Icons fotos """
    
    
    text_gesund = f"Der Fall {dsatz[1]} {dsatz[2]} wird als abgeschlossen behandelt,\n\
das heisst für die Leitstelle ist er nicht mehr sichtbar,\n\
aber für das HR und die Führung bleibt er als abgeschlossen bearbeitbar.\n\
Bitte schliesse den Fall erst als abgeschlossen ab, wenn der MA wirklich wieder gesund ist und arbeitet.\n\
Danke.\n\n\
Sollte der Mitarbeiter unvorhergesehen einen Rückfall erleiden muss ein neuer Fall angelegt werden.\n\n\n\n\
{dsatz[1]} {dsatz[2]} ist wieder gesund und kann archiviert werden ..."
    l_text = tk.Label(root_gesund, text=text_gesund, bg="green", fg="white", font=size_n, justify="left")
    l_text.grid(row=1, column=1, columnspan=3, padx=50, pady=30)

    
    l_zudatum = tk.Label(root_gesund, text="... Wann ist der MA gesund? ", bg="green", fg="white", font=size_n, justify="right", anchor="e")
    l_zudatum.grid(row=2, column=1, padx=50, pady=30, sticky="e")
    e_datum = DateEntry(root_gesund, width="10", background="green", foreground="white", bd=2, date_pattern="dd.mm.YYYY", anchor="w")
    e_datum.grid(row=2, column=2, padx=0, pady=30, stick="w")

    """ Definitiv Gesund """
    def gesund_execute(dsatz):
        dsatz = dsatz
        id_ = dsatz[0]
        status = "G"
        meldung = date.today().strftime("%d.%m.%Y")
        meldung_time = datetime.now().strftime("%H:%M")
        gesundgemeldet_auf = e_datum.get()
        bearbeitet = str(getpass.getuser())

        #connect to db
        verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
        zeiger = verbindung.cursor()

        # status wird in der mitarbeiter haupttable geupdatet
        zeiger.execute("UPDATE mitarbeiter SET status=? WHERE id_=?", (status, id_))
        verbindung.commit()
        
        # Die Gesundmeldung wird protokolliert
        zeiger.execute("INSERT INTO gesundmeldung (id_, meldung, meldung_time, gesundgemeldet_auf, bearbeitet) VALUES (?,?,?,?,?)", (id_, meldung, meldung_time, gesundgemeldet_auf, bearbeitet))
        verbindung.commit()
        verbindung.close()
        try:
            # funktionen.send_mail.py
            info_gesundmeldung(dsatz)
            messagebox.showinfo("Info Mail","Danke, der Fall wurde gespeichert, die Mail versendet.\nIch wünsche dir einen schönen Tag.")
        except:
            messagebox.showwarning("Info Mail", "Alle Daten sind gespeichert, aber wir konnten keine Mail senden, checke bitte deine Internetverbindung oder melde den Fall Patrick Bitterlin") 

        root_gesund.quit()
        root_gesund.withdraw()
        #111


    b_ok_gesund = tk.Button(root_gesund, text="okey, ich check in aus", bg="black", fg="gold", 
                                        font=size_x, anchor="w", command=partial(gesund_execute, dsatz))
    b_ok_gesund.grid(row=2, column=3, padx=50, pady=0, sticky="e")


    l_strich = tk.Label(root_gesund, text="______________________________________________________________________________________", 
                                            bg="green", fg="white", font=size_n)
    l_strich.grid(row=4, column=1, columnspan="3", padx=50, pady=4)

    text_gesund1 = "\n\n\n\n\nHmm ich warte lieber noch."
    l_text1 = tk.Label(root_gesund, text=text_gesund1, bg="green", fg="white", font=size_n, justify="left")
    l_text1.grid(row=5, column=3, padx=50, pady=30, sticky="e")

    b_abbrechen = tk.Button(root_gesund, text="abbrechen", bg="black", fg="gold", font=size_x, 
                                        justify="left", command=lambda: root_gesund.destroy())
    b_abbrechen.grid(row=6, column=3, padx=50, pady=0, sticky="e")




    root_gesund.mainloop() 