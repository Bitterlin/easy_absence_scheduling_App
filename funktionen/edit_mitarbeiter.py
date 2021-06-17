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
import sqlite3
import getpass

#### Hilfe / Vorlagen | heute.strftime("%d.%m.%Y")

from funktionen.update_data_in_db import *


locale.setlocale(locale.LC_ALL, 'de_CH.utf8')  # in verbindung mit import locale siehe oben 
heute = date.today().strftime("%d.%m.%Y")
user = str(getpass.getuser())

""" GRUPPENLEITER """
def ed_grl(mitarbeiter_dsatz, grl):    
    dsatz = list(mitarbeiter_dsatz)
    grl = grl
    
    edit_field = tk.Tk()
    edit_field.title("Gruppenleiterwechsel")
    w, h = 550, 300
    edit_field.geometry("%dx%d+550+350" % (w, h))
    edit_field.configure(bg='blue')
    edit_field.focus_set()

    text_ = f"Wechsle den Gruppenleiter für {dsatz[1]} {dsatz[2]}"
    label = tk.Label(edit_field, text=text_, bg="blue", fg="white", font=("Verdana", 12, "bold"))
    label.pack(pady=20)

    # Combobox Gruppenleiter erstellen
    v_gruppenleiter = tk.StringVar()
    e_gruppenleiter = ttk.Combobox(edit_field, width="19", foreground="black", background="blue", height=3, textvariable = v_gruppenleiter)
    # liste combobox drop down erstellen
    e_gruppenleiter['values'] = grl
    e_gruppenleiter.pack(padx=5, pady=20)
    e_gruppenleiter.current()

    def xxx():
        
        dsatz[3] = e_gruppenleiter.get()
        
        sql_update_grl(dsatz)

        edit_field.quit()
        edit_field.withdraw()

    button = tk.Button(edit_field, text="speichern", bg="black", fg="white", command=xxx)
    button.pack(padx=5, pady=20)

    edit_field.mainloop()


""" Edit Grund """
def ed_grund(mitarbeiter_dsatz, grund):
    dsatz = list(mitarbeiter_dsatz)
    grund = grund
    edit_field = tk.Tk()
    edit_field.title("Wechsel des Grundes")
    w, h = 550, 300
    edit_field.geometry("%dx%d+550+350" % (w, h))
    edit_field.configure(bg='blue')
    edit_field.focus_set()
    text_ = f"Welcher  Grund wird für {dsatz[1]} {dsatz[2]} zugewiesen?"
    label = tk.Label(edit_field, text=text_, bg="blue", fg="white", font=("Verdana", 12, "bold"))
    label.pack(pady=20)
    # Combobox Gruppenleiter erstellen
    v_grund = tk.StringVar()
    e_grund = ttk.Combobox(edit_field, width="19", foreground="black", background="blue", height=3, textvariable = v_grund)
    # liste combobox drop down erstellen
    e_grund['values'] = grund
    e_grund.pack(padx=5, pady=20)
    e_grund.current()

    def xxx1():
        dsatz[3] = e_grund.get()
        sql_update_grund(dsatz)
        edit_field.quit()
        edit_field.withdraw()
    button = tk.Button(edit_field, text="speichern", bg="black", fg="white", command=xxx1)
    button.pack(padx=5, pady=20)

    edit_field.mainloop()

""" Edit Prognose """
def ed_prog(mitarbeiter_dsatz):
    dsatz = list(mitarbeiter_dsatz)

    edit_field = tk.Tk()
    edit_field.title("Wechsel des Grundes")
    w, h = 550, 300
    edit_field.geometry("%dx%d+550+350" % (w, h))
    edit_field.configure(bg='blue')
    edit_field.focus_set()
    
    text_ = f"Deine Schätzung,\nwann kommt {dsatz[1]} {dsatz[2]} zurück?"
    label = tk.Label(edit_field, text=text_, bg="blue", fg="white", font=("Verdana", 12, "bold"))
    label.pack(pady=20)
    
    e_prog = DateEntry(edit_field, width=10, background="white", foreground="black", bd=2, date_pattern="dd.MM.YYYY")
    e_prog.pack(pady=20)

    def xxx1():
        dsatz[11] = e_prog.get()
        sql_update_prog(dsatz)
        edit_field.quit()
        edit_field.withdraw()
    button = tk.Button(edit_field, text="speichern", bg="black", fg="white", command=xxx1)
    button.pack(padx=5, pady=20)

    edit_field.mainloop()

""" Edit Meldepflicht """
def ed_meld(mitarbeiter_dsatz):
    dsatz = list(mitarbeiter_dsatz)
    edit_field = tk.Tk()
    edit_field.title("Neue Meldepflicht")
    w, h = 550, 300
    edit_field.geometry("%dx%d+550+350" % (w, h))
    edit_field.configure(bg='blue')
    edit_field.focus_set()

    # Wird der History/Verlauf übergeben  
    user_alt = dsatz[4]
    gemeldet_alt = dsatz[7]
    gemeldet_alt_time = dsatz[8]
    meldepflicht_alt = dsatz[9]
    meldepflicht_alt_time = dsatz[10]

    # die aktuellen variablen werden bezogen
    text_ = f"Neue Meldepflicht für {dsatz[1]} {dsatz[2]} zuweisen?"
    label = tk.Label(edit_field, text=text_, bg="blue", fg="white", font=("Verdana", 12, "bold"))
    label.pack(pady=5)
    label2 = tk.Label(edit_field, text="Datum:", bg="blue", fg="black")
    label2.pack(pady=5)
    e_meldepflicht = DateEntry(edit_field, width=10, background="white", foreground="black", bd=2, date_pattern="dd.MM.YYYY")
    e_meldepflicht.pack(padx=5, pady=5)
    label3 = tk.Label(edit_field, text="Zeit", bg="blue", fg="black")
    label3.pack(pady=5) 
    e_meldepflicht_time = time.strftime('%H:%M%p')
    e_meldepflicht_time = tk.Entry(edit_field, bg="white", fg="Black", width=5)
    e_meldepflicht_time.pack(padx=5, pady=5)
    e_meldepflicht_time.insert(0, dsatz[10])
    l_time = tk.Label(edit_field, text="Zeit bitte nur im Format 11:11 eingeben", bg="blue", fg="white", width="40")
    l_time.pack(pady=5)


    def xxx2():
        dsatz[9] = e_meldepflicht.get()
        dsatz[10] = e_meldepflicht_time.get()
        sql_hisytory_insert(dsatz, user_alt, gemeldet_alt, gemeldet_alt_time, meldepflicht_alt,meldepflicht_alt_time)
        sql_update_meld(dsatz)
        edit_field.quit()
        edit_field.withdraw()
    button = tk.Button(edit_field, text="speichern", bg="black", fg="white", command=xxx2)
    button.pack(padx=5, pady=20)

    edit_field.mainloop()

def ed_notiz(mitarbeiter_dsatz, wert):
    dsatz = mitarbeiter_dsatz
    notiz = wert
    id_ = dsatz[0]
    
  
    #connect to db
    verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
    zeiger = verbindung.cursor()

    zeiger.execute("UPDATE mitarbeiter SET notiz=? WHERE id_=?", (notiz, id_))
    verbindung.commit()
    verbindung.close()


def sql_delete_id(rows):
    dsatz = rows
    id_ = dsatz[0]

    text = f"{dsatz[1]} {dsatz[2]} wirklich unwiederuflich löschen?"
    result_y_n = messagebox.askyesno("WARNUNG",text)
    if result_y_n:
        #connect to db
        verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
        zeiger = verbindung.cursor()

        zeiger.execute("DELETE FROM mitarbeiter WHERE id_=" + str(id_))
        verbindung.commit()
        verbindung.close()

        text2 = f"{dsatz[1]} {dsatz[2]} erfolgreich gelöscht."
        
        messagebox.showinfo("LÖSCHUNG ERFOLGREICH",text2)
    else:
        return
        


    





    