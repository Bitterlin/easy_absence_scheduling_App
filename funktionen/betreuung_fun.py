import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter.font import Font
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import sys
import time
import datetime
from datetime import date
from datetime import datetime
import locale #locale.setlocale(locale.LC_ALL, 'de_CH.utf8')  
import getpass # um getuser = str(getpass.getuser())
from functools import partial # ==> einen Wert an eine Funktion senden zb. bei einer forschleife 
from pathlib import Path # um Path z.B. von Linux / automatisch zu Win \ convertieren

def betreuung_execute(dsatz):
    dsatz = list(dsatz)
    farbe = "#391C3F"
    weiss = "white"

    root_betreuung = tk.Tk()

    root_betreuung.title("Vertraulicher Bereich")
    root_betreuung.deiconify()  # info .deconifiy zum maximieren und .iconify zum minimieren.
    w, h = root_betreuung.winfo_screenwidth(), root_betreuung.winfo_screenheight()
    root_betreuung.geometry("%dx%d+0+0" % (w, h))
    root_betreuung.configure(bg=farbe)
    root_betreuung.focus_set()
    size_xxx = "Verdana 20 bold"    
    # ---e---


    text = f"Betreuung durch Gruppenleiter\n\nMA: {dsatz[1]} {dsatz[2]}"
    l_title = tk.Label(root_betreuung, text=text, bg=farbe, fg=weiss, font=size_xxx, anchor="w", justify="left")
    l_title.grid(row=0,column=0,padx=40,pady=40, columnspan=3, sticky="w")

# § § § § § § § § § § § § § § § § § § § § § § § § § § § § § § § § § § § § § §

    """ labelframe L """
    ### wenn die maus das frame verlässt, 
    # werden zuerst alle elemente in der db auf 0 gesetzt, danach werden alle daten  welche 
    # angewählt sind mit 1 gespeichert

    def themen_speichern(event):
        id_ = dsatz[0]
        
        # connect to db
        verbindung_secure = sqlite3.connect("datenbank/secure.db")
        zeiger_secure = verbindung_secure.cursor()
        # --e--

        # zuerst alle optinen auf 0 setzen
        li_all = ["Verhalten", "Integration", "Aufenthalt", "Wille", "Glaubhaftigkeit", "Regelmässigkeit", "Fahrtüchtigkeit", "Sperrfrist", "Ferienkürzung", "Case_management", "Vertrauensarzt", "Coach", "Iv", "Reha", "Frühpensionierung"]
        zähler = 0
        for i in li_all:
            zeiger_secure.execute(f"UPDATE betreuung SET {i}=? WHERE id_=?", ("0", id_))
            verbindung_secure.commit()
            li_alle_themen.itemconfig(zähler, bg=farbe, fg=weiss)
            zähler += 1
        zähler = 0

        # speichert alle themen die aktuell angewählt wurden
        values = [li_alle_themen.get(idx) for idx in li_alle_themen.curselection()]
        print("values: ", values)
        
        for i in values: # i gibt die strings optionen zurück
            zeiger_secure.execute(f"UPDATE betreuung SET {i}=? WHERE id_=?", ("1", id_))
            verbindung_secure.commit()
        verbindung_secure.close()
        
        # for ix in li_alle_themen.curselection(): # ix resp .curselection() gibt alle indexes welche angewählt sind zurück
        #     li_alle_themen.itemconfig(ix, bg="blue")
        # print("Curselection: ", str(li_alle_themen.curselection()))            
        # ---e---

    text = "Mögliche Themen:" 
    l_frame1 = tk.LabelFrame(root_betreuung, text=text, bg=farbe, fg="gold")
    l_frame1.grid(row=1, column=0, padx=40,pady=40, rowspan=3, sticky="n")
    l_frame1.bind("<Leave>", themen_speichern)
    
    # optionen / multioption
    li_option = ["Verhalten", "Integration", "Aufenthalt", "Wille", "Glaubhaftigkeit", "Regelmässigkeit", "Fahrtüchtigkeit", "Sperrfrist", "Ferienkürzung", "Case_management", "Vertrauensarzt", "Coach", "Iv", "Reha", "Frühpensionierung"]
    li_alle_themen = tk.Listbox(l_frame1, selectmode = "multiple", justify="center", height=15)
    li_alle_themen.pack(expand=tk.YES, fill="both")
    for i in range(len(li_option)):
        li_alle_themen.insert(tk.END, li_option[i])
        li_alle_themen.itemconfig(i, bg=farbe, fg=weiss)
    

    """ daten in der db, welche optionen sind gespeichert als gesetzt """
    id_ = dsatz[0]
    
    # connect to db
    verbindung_secure = sqlite3.connect("datenbank/secure.db")
    zeiger_secure = verbindung_secure.cursor()

    zeiger_secure.execute("SELECT Verhalten, Integration, Aufenthalt, Wille, Glaubhaftigkeit, Regelmässigkeit, Fahrtüchtigkeit, Sperrfrist, Ferienkürzung, Case_management, Vertrauensarzt, Coach, Iv, Reha, Frühpensionierung FROM betreuung WHERE id_=?",(id_,))
    ergebnis = zeiger_secure.fetchall()
    print(ergebnis)

    verbindung_secure.commit()
    verbindung_secure.close()

    zähler = 0
    #ergebnis = list(ergebnis
    for i in ergebnis:
        for ii in i:                
            if str(ii) == "1":
                li_alle_themen.select_set(zähler)
            zähler += 1    

# § § § § § § § § § § § § § § § § § § § § § § § § § § § § § 
    def gespräch_speichern():

         # connect to db
        verbindung_secure = sqlite3.connect("datenbank/secure.db")
        zeiger_secure = verbindung_secure.cursor()

        
        gespräch_text = e_text_gespräche.get("1.0","end-1c")
        zeiger_secure.execute(f"UPDATE betreuung SET Gespräche=? WHERE id_=?", (gespräch_text, id_))
        verbindung_secure.commit()
        verbindung_secure.close()
        

        time = datetime.now().strftime("%H:%M:%S")
        b_speichern["text"] = f"ok: {time}"


    l_überschrift_gespräche = tk.Label(root_betreuung, text="Gesprächsnotizen:", bg=farbe, fg=weiss, font=size_xxx)
    l_überschrift_gespräche.grid(row=1, column=1, padx=20, pady=5)

    S = tk.Scrollbar(root_betreuung)
    S.grid(row=2, column=1, sticky=tk.N+tk.S+tk.E)

    e_text_gespräche = tk.Text(root_betreuung, bg=weiss, fg="blue", width=120, height=30)
    e_text_gespräche.grid(row=2, column=1, padx=20, pady=5)


    # connect to db to get Gespräche
    verbindung_secure = sqlite3.connect("datenbank/secure.db")
    zeiger_secure = verbindung_secure.cursor()

    zeiger_secure.execute("SELECT Gespräche FROM betreuung WHERE id_=?", (id_,)) 
    text_gespräche = zeiger_secure.fetchall()
    verbindung_secure.commit()
    verbindung_secure.close()
    # --e--

    S.config(command=e_text_gespräche.yview)
    e_text_gespräche.config(yscrollcommand=S.set)
    e_text_gespräche.insert("end", text_gespräche[0][0])

    b_speichern = tk.Button(root_betreuung, text="speichern", bg=farbe, fg=weiss, command= gespräch_speichern)
    b_speichern.grid(row=3, column=1, padx=20, pady=2, sticky="e")

    
# § § § § § § § § § § § § § § § § § § § § § § § § § § § § § 

    # """ labelframe R """
    # # wenn die maus das frame verlässt, daten speichern
    # def lösungen_speichern(event):
    #     id_ = dsatz[0]

    #     # connect to db
    #     verbindung_secure = sqlite3.connect("datenbank/secure.db")
    #     zeiger_secure = verbindung_secure.cursor()
    #     # --e--

    #     # zuerst alle optinen auf 0 setzen
    #     li_all_2 = ["Sperrfrist", "Ferienkürzung", "Case_management", "Vertrauensarzt", "Coach", "Iv", "Reha", "Frühpensionierung"]
    #     zähler = 0
    #     for i in li_all_2:
    #         zeiger_secure.execute(f"UPDATE betreuung SET {i}=? WHERE id_=?", ("0", id_))
    #         verbindung_secure.commit()
    #         li_alle_lösungen.itemconfig(zähler, bg=farbe, fg=weiss)
    #         zähler += 1
    #     zähler = 0
    #     # speichert alle themen die angewählt wurden
    #     values_2 = [li_alle_lösungen.get(idx) for idx in li_alle_lösungen.curselection()]
    #     print("values: ", values_2)
        
    #     for i in values_2:
    #         zeiger_secure.execute(f"UPDATE betreuung SET {i}=? WHERE id_=?", ("1", id_))
    #         verbindung_secure.commit()
    #     verbindung_secure.close()
        
    #     for ix in li_alle_lösungen.curselection():
    #         li_alle_lösungen.itemconfig(ix, bg="blue")
    #     print("Curselection: ", str(li_alle_lösungen.curselection()))            
    #     # ---e---

    # text_2 = "Mögliche lösungen:" 
    # l_frame2 = tk.LabelFrame(root_betreuung, text=text_2, bg=farbe, fg="gold")
    # l_frame2.grid(row=1, column=2, padx=40, pady=40, rowspan=3, sticky="n")
    # l_frame2.bind("<Leave>", lösungen_speichern)
    
    # # lösungen / multioption
    # li_lösungen = ["Sperrfrist", "Ferienkürzung", "Case_management", "Vertrauensarzt", "Coach", "Iv", "Reha", "Frühpensionierung"]
    # li_alle_lösungen = tk.Listbox(l_frame2, selectmode = "multiple", justify="center", height=8)
    # li_alle_lösungen.pack(expand=tk.YES, fill="both")
    # for i in range(len(li_lösungen)):
    #     li_alle_lösungen.insert(tk.END, li_lösungen[i])
    #     li_alle_lösungen.itemconfig(i, bg=farbe, fg=weiss)
    

    # """ daten in der db, welche oprionen sind gespeichert als gesetzt """
    # id_ = dsatz[0]
    
    # # connect to db
    # verbindung_secure = sqlite3.connect("datenbank/secure.db")
    # zeiger_secure = verbindung_secure.cursor()

    # zeiger_secure.execute("SELECT Sperrfrist, Ferienkürzung, Case_management, Vertrauensarzt, Coach, Iv, Reha, Frühpensionierung FROM betreuung WHERE id_=?",(id_,))
    # ergebnis_2 = zeiger_secure.fetchall()
    # print(ergebnis_2)

    # verbindung_secure.commit()
    # verbindung_secure.close()

    # zähler = 0
    # #ergebnis_2 = list(ergebnis_2)
    # for i in ergebnis_2:
    #     for ii in i:                
    #         if str(ii) == "1":
    #             li_alle_lösungen.select_set(zähler)
    #         zähler += 1    



# § § § § § § § § § § § § § § § § § § § § § § § § § § § § §




    root_betreuung.mainloop()
    # ---e---

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§






def check_is_in_sql(dsatz):
    dsatz = dsatz
    id_ = dsatz[0]

    # connect to db
    verbindung_secure = sqlite3.connect("datenbank/secure.db")
    zeiger_secure = verbindung_secure.cursor()

    zeiger_secure.execute("SELECT count(id_) FROM betreuung WHERE id_=?",(id_,))
    resultat = zeiger_secure.fetchall()

    verbindung_secure.commit()
    
    """
    print(str(resultat))
    print(type(resultat))
    print(resultat[0])
        """
    if str(resultat) == "[(0,)]":
        id_ = dsatz[0]
        Gespräche = "Noch kein Eintrag"
        Verhalten = 0
        Integration = 0
        Aufenthalt = 0
        Wille = 0
        Glaubhaftigkeit = 0 
        Regelmässigkeit = 0
        Fahrtüchtigkeit = 0
        Sperrfrist = 0
        Ferienkürzung = 0
        Case_management = 0
        Vertrauensarzt = 0
        Coach = 0
        Iv = 0
        Reha = 0
        Frühpensionierung = 0 

        zeiger_secure.execute("""INSERT INTO betreuung (id_, 
                                                        Gespräche,
                                                        Verhalten,
                                                        Integration,
                                                        Aufenthalt,
                                                        Wille,
                                                        Glaubhaftigkeit,
                                                        Regelmässigkeit,
                                                        Fahrtüchtigkeit,
                                                        Sperrfrist,
                                                        Ferienkürzung,
                                                        Case_management,
                                                        Vertrauensarzt,
                                                        Coach,
                                                        Iv,
                                                        Reha,
                                                        Frühpensionierung) 
                                                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", 
                                                        (id_,
                                                        Gespräche, 
                                                        Verhalten,
                                                        Integration,
                                                        Aufenthalt,
                                                        Wille,
                                                        Glaubhaftigkeit,
                                                        Regelmässigkeit,
                                                        Fahrtüchtigkeit,
                                                        Sperrfrist,
                                                        Ferienkürzung,
                                                        Case_management,
                                                        Vertrauensarzt,
                                                        Coach,
                                                        Iv,
                                                        Reha,
                                                        Frühpensionierung))
        verbindung_secure.commit()
        # ---e---

    verbindung_secure.close()
    # ---e---    




