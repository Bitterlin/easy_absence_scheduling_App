#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
############################################
# Dispotool für das Abwesenheitsmanagement #
 
  Version 0.1.0 | Stand 2021.06.09        

# Kontakt: webmaster@bitterlin.info        #
#                                          #
############################################
"""

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
# Index: Wort anklicken und auf ctr+F    §§
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# aktuell 111
# hauptfenster
# status
# neuerFallanlegen
# fallbearbeitung
# Gesundmeldung
# myFirstScroolingWinidow
# delete_case
# GostCase
# betreuung
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§


""" algemeine python module """
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
  

""" eigene module """
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
import funktionen.create_db_a_table
from funktionen.store_datas_in_db_new_case import *
from funktionen.edit_mitarbeiter import *
from funktionen.select_data_in_db import *
from funktionen.gesund_meldung import *
from funktionen.betreuung_fun import *

from datafiles.gruppenleiter import *
from datafiles.abwesenheitsgruende import *
from funktionen.send_mail import * 
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§


""" default variablen """
locale.setlocale(locale.LC_ALL, 'de_CH.utf8')  # in verbindung mit import locale siehe oben 
global heute
heute = date.today()
global heute_time
heute_time = datetime.now()
global farbe 
farbe = "#160A49"
time_ = heute_time.strftime("%H:%M")
getuser = str(getpass.getuser())
# Font-variablen
schriftfarbe = "black"
hintergrund = "yellow"
bullet = "\u2022"
# ---e---


""" TK root """
root = tk.Tk()

root.title("Abwesenheiten Main")
# root.geometry("1x700+0+0")
root.deiconify()  # info .deconifiy zum maximieren und .iconify zum minimieren.
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.configure(bg='yellow')
root.focus_set()
#root.state('zoomed')
#root.iconbitmap(r"res\ico.ico")
size_n = Font(family="Verdana", size="12")
size_x = Font(family="Verdana", size="14", weight="bold")
size_xx = Font(family="Verdana", size="16", weight="bold")
size_xxx = Font(family="Verdana", size="20", weight="bold")
# ---e---


""" für windows user wird das win system 32 importiert """
try:
  import win32com.client as win32
except:
  messagebox.showinfo("Problem erkannt", "Die Mailfunktion ist inaktiv!")
# ---e---


""" Alle Bilder und Icons fotos """
logo_path = Path("icons/logo.png")
global logo               
logo = tk.PhotoImage(file=logo_path) # Logo halt 
schloss_path = Path("icons/password.png")
global schloss
schloss = tk.PhotoImage(file=schloss_path) # Foto mit Schloss und passwordpunkte
new_png_path = Path("icons/new.png")
global new_png
new_png = tk.PhotoImage(file=new_png_path) # Foto mit Mensch plus
abbruch_png_path = Path("icons/abbruch.png")
global abbruch_png
abbruch_png = tk.PhotoImage(file=abbruch_png_path) # Foto mit Kreuz
speichern_png_path = Path("icons/ok.png")
global speichern_png
speichern_png = tk.PhotoImage(file=speichern_png_path) # Foto mit ok-Haken 
important_png_path = Path("icons/important.png")
global important_png
important_png = tk.PhotoImage(file=important_png_path) # Foto Mit Ausrufezeichen
arztkoffer_png_path = Path("icons/arzt.png")
global arztkoffer_png
arztkoffer_png = tk.PhotoImage(file=arztkoffer_png_path) # Foto mit Arztkoffer
lupe_png_path = Path("icons/lupe.png")
global lupe_png
lupe_png = tk.PhotoImage(file=lupe_png_path)
edit_png_path = Path("icons/edit.png")
global edit_png
edit_png = tk.PhotoImage(file=edit_png_path)
send_png_path = Path("icons/send.png")
global send_png
send_png = tk.PhotoImage(file=send_png_path)
gost_png_path = Path("icons/gost.png")
global gost_png
gost_png = tk.PhotoImage(file=gost_png_path)
delete_png_path = Path("icons/delete.png")
global delete_png
delete_png = tk.PhotoImage(file=delete_png_path)
# ---e---


""" Logo einfügen und Bild Schloss""" 
logo_label = tk.Label(root, image=logo, bg="yellow")
logo_label.image = logo
logo_label.grid(row=0, column=0, padx=10, pady=50)
l_schloss = tk.Label(root, image=schloss, bg=hintergrund)
l_schloss.image = schloss
l_schloss.grid(row=1, column=20, columnspan=2, padx=50, pady=50)
# ---e---


""" funktion für das login """
def Try_user_login(event=None):
  # usereingaben entegennehmen
  inp_user_id =  e_user.get()
  inp_code = e_code.get()

  # 222
  try: 
    # Verbindung zum Table User in der db mitarbeiter aufbauen
    verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
    zeiger = verbindung.cursor()
    ergebnis = "ich bin eine string variable" 

    # Richtige Zugangsaden evaluieren
    sql1 = "SELECT check_ok FROM user WHERE user_id="
    # Prüfstring wird zusammengesetzt
    sql_anweisung = sql1 + "'" + str(inp_user_id) + "'"
    zeiger.execute(sql_anweisung) 
    for dsatz in zeiger:
      ergebnis = dsatz[0]
    verbindung.close()

  except ValueError: #222
    messagebox.showwarning("SQL ERROR", "Ein SQL Fehler!\nMelde dich bitte beim Developer Patrick Bitterlin")
  #---e---


    """ abfrage zugangsdaten OK ?  """  
  #Auswertung Kontrolle user versus db
  if ergebnis == str(inp_user_id + inp_code):
    verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
    zeiger = verbindung.cursor()
    berechtigung = 0
    try:
      # Richtige Zugangsaden evaluieren
      sql2 = "SELECT berechtigung FROM user WHERE user_id="
      sql_anweisung2 = sql2 + "'" + str(inp_user_id) + "'"
      zeiger.execute(sql_anweisung2) 
      for dsatz in zeiger:
        berechtigung = str(dsatz[0])
    except ValueError:
      messagebox.showwarning("SQL ERROR","Ein SQL Fehler ist aufgetreten, melde dich bitte bei Patrick Bitterlin")
    #---e---
    
    global globale_berechtigung  
    globale_berechtigung = berechtigung
    global global_user
    global_user = inp_user_id
    verbindung.close()
    #---e---

    """ Hauptfenster """
    def hauptfenster(sql_auswahl = True):
        
      ww = tk.Toplevel(root, bg="yellow")
      ww.title("eingelogt als " + getuser)
      ww.deiconify()  # info .deconifiy zum maximieren und .iconify zum minimieren.
      w, h = ww.winfo_screenwidth(), ww.winfo_screenheight()
      ww.geometry("%dx%d+0+0" % (w, h))
      ww.focus_set()
      root.withdraw() #Macht root (Site login) unsichtbar 

      """ Scrollbar instruction on this link: https://www.youtube.com/watch?v=0WafQCaok6g """
      #myFirstScroolingWinidow
      #create a main frame
      main_frame = tk.Frame(ww)
      main_frame.pack(fill=tk.BOTH, expand=1)

      #create a canvas
      my_canvas = tk.Canvas(main_frame, bg="yellow")
      my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

      #add a scrollbar to the canvas
      my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
      my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

      #convigure the canvas
      my_canvas.configure( yscrollcommand = my_scrollbar.set)
      my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
      # mit Mausrad scroolen
      def _on_mouse_wheel(event):  
        my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
        #---e---
      
      #create another frame inside the canvas 
      second_frame = tk.Frame(my_canvas, bg="yellow")

      #add that new frame to a window in the canvas
      my_canvas.create_window((0,0), window=second_frame, anchor="nw")
      # --- e Scrollbar ---


      """ Formular top für neuen Fall """
      # neuerFallanlegen
      def new_case():
        new = tk.Toplevel(second_frame, bg="yellow")

        new.title("Formular - neuer Fall -")
        # root.geometry("1x700+0+0")
        new.deiconify()  # info .deconifiy zum maximieren und .iconify zum minimieren.
        w, h = new.winfo_screenwidth(), new.winfo_screenheight()
        new.geometry("%dx%d+0+0" % (w, h))
        new.configure(bg='yellow')
        new.focus_set()

        logo_label = tk.Label(new, image=logo, bg=hintergrund)
        logo_label.image = logo
        logo_label.grid(row=0, column=0, padx=54, pady=50)
        l_ueberschrift = tk.Label(new, text="Neuer Fall", bg=hintergrund, fg=schriftfarbe, font=size_xxx)
        l_ueberschrift.grid(row=0, column=1, columnspan=10, padx=75, pady=5, sticky="w")
        #variablen für alle entries und labels
        l_width = "15"
        e_width = "20"
        px = 2 
        py = 5
        weiss = "white"
        # Calender fromat und alg. var
        cal_col = "#8F8746" 
        cal_width = "24" 
        cal_form = "dd.MM.yyyy"

        """ Entries für Fall neu """
        l_vorname = tk.Label(new, text="Vorname: ", bg=hintergrund, fg=schriftfarbe, width=l_width, anchor="w")
        l_vorname.grid(row=1, column=0, padx=px, pady=py)
        e_vorname = tk.Entry(new, width=e_width, font=size_n, bg=weiss, fg=schriftfarbe)
        e_vorname.grid(row=1, column=1, padx=px, pady=py)
        
        l_nachname = tk.Label(new, text="Nachname:", bg=hintergrund, fg=schriftfarbe, width=l_width, anchor="w")
        l_nachname.grid(row=2, column=0, padx=px, pady=py)
        e_nachname = tk.Entry(new, width=e_width, font=size_n, bg=weiss, fg=schriftfarbe)
        e_nachname.grid(row=2, column=1, padx=px, pady=py)
        l_gruppenleiter = tk.Label(new, text="Gruppenleiter:", bg=hintergrund, fg=schriftfarbe, width=l_width, anchor="w")
        l_gruppenleiter.grid(row=3, column=0, padx=px, pady=py)
        # Combobox Gruppenleiter erstellen
        v_gruppenleiter = tk.StringVar()
        e_gruppenleiter = ttk.Combobox(new, width="19", font=size_n, textvariable = v_gruppenleiter)
        # liste combobox drop down erstellen
        e_gruppenleiter['values'] = grl     
        e_gruppenleiter.grid(row=3, column=1, padx=px, pady=py)
        e_gruppenleiter.current()
        l_bearbeitet = tk.Label(new, text="Bearbeitet:", bg=hintergrund, fg=schriftfarbe, width=l_width, anchor="w")
        l_bearbeitet.grid(row=4, column=0, padx=px, pady=py)
        #e_bearbeitet = pseudo Entry
        bea = global_user.replace(".", " ").title()
        e_bearbeitet = tk.Label(new, text=bea, bg=weiss, fg=schriftfarbe, font=size_n, width=e_width, anchor="w")
        e_bearbeitet.grid(row=4, column=1, padx=px, pady=py)
        l_grund = tk.Label(new, text="Grund:", bg=hintergrund, fg=schriftfarbe, width=l_width, anchor="w")
        l_grund.grid(row=5, column=0, padx=px, pady=py)
        # Combobox Grund erstellen
        v_grund = tk.StringVar()
        e_grund = ttk.Combobox(new, width="19", font=size_n, textvariable=v_grund)
        # liste combobox drop down erstellen
        e_grund['values'] = grund_abwesenheit
        e_grund.grid(row=5, column=1, padx=px, pady=py)
        e_grund.current()
        l_abwesend_seit = tk.Label(new, text="1. Tag Abwesend:", bg=hintergrund, fg=schriftfarbe, width=l_width, anchor="w")
        l_abwesend_seit.grid(row=6, column=0, padx=px, pady=py)
        e_abwesend_seid = DateEntry(new, width=cal_width, background=cal_col, foreground=weiss, bd=2, date_pattern=cal_form)
        e_abwesend_seid.grid(row=6, column=1, padx=px, pady=py)
        l_gemeldet = tk.Label(new, text="Gemeldet:", bg=hintergrund, fg=schriftfarbe, width=l_width, anchor="w")
        l_gemeldet.grid(row=7, column=0, padx=px, pady=py)
        e_gemeldet = DateEntry(new, width=cal_width, background=cal_col, foreground=weiss, bd=2, date_pattern=cal_form)
        e_gemeldet.grid(row=7, column=1, padx=px, pady=py)
        e_gemeldet_time = time.strftime('%H:%M%p')
        e_gemeldet_time = tk.Entry(new, bg=weiss, fg=schriftfarbe, width=5)
        e_gemeldet_time.grid(row=7, column=2, padx=px, pady=py)
        e_gemeldet_time.insert(0, str(time_))
        l_time = tk.Label(new, text="H", bg=hintergrund, fg=schriftfarbe, width="2")
        l_time.grid(row=7, column=3, pady=py)
        l_meldepflicht = tk.Label(new, text="1. Meldepflicht:", bg=hintergrund, fg=schriftfarbe, width=l_width, anchor="w")
        l_meldepflicht.grid(row=8, column=0, padx=px, pady=py)
        e_meldepflicht = DateEntry(new, width=cal_width, background=cal_col, foreground=weiss, bd=2, date_pattern=cal_form)
        e_meldepflicht.grid(row=8, column=1, padx=px, pady=py)
        e_meldepflicht_time =time.strftime('%H:%M%p')
        e_meldepflicht_time = tk.Entry(new, bg=weiss, fg=schriftfarbe, width=5)
        e_meldepflicht_time.grid(row=8, column=2, padx=px, pady=py)
        l_time = tk.Label(new, text="H", bg=hintergrund, fg=schriftfarbe, width="2")
        l_time.grid(row=8, column=3, pady=py)
        l_prognose = tk.Label(new, text="Schätzung w. gesund:", bg=hintergrund, fg=schriftfarbe, width=l_width, anchor="w")
        l_prognose.grid(row=9, column=0, padx=px, pady=py)
        e_prognose = DateEntry(new, width=cal_width, background=cal_col, foreground=weiss, bd=2, date_pattern=cal_form)
        e_prognose.grid(row=9, column=1, padx=px, pady=py)
        l_notiz = tk.Label(new, text="Notizen für Dispo:", bg=hintergrund, fg=schriftfarbe, width=e_width, anchor="w")
        l_notiz.grid(row=1, column=4, padx=20, pady=py)
        e_notiz = tk.Text(new, width=60, height=12, bg=weiss, fg=schriftfarbe, font=size_n)
        e_notiz.grid(row=2, rowspan=8 , column=4, padx=20, pady=py)
        #Steuerungsbuttons
        def abbrechen_new(event=None):
          new.destroy()
          new.update()        
        b_abbrechen = tk.Button(new, text="abbrechen", image=abbruch_png, 
                                      width=140, bg=cal_col, fg=weiss, font=size_n, 
                                        compound="left", command=abbrechen_new)
        b_abbrechen.grid(row=10, column=0, padx=px, pady=60)


        """ Falldaten NEU Speichern und senden """
        def speichern_new(event=None):
          # Wir beginnen mit der validierung der Daten
          def check_string_not_null(strings):
            string = strings
            if not string:
              # pflichtfeld leer
              messagebox.showinfo("Pflichtfeld", "Ein Feld auf der linken Seite ist leer.")
              return False
              # ---e---
            else:
              return True

          def check_time_okey(strings):
            def alert():
              # Toplevel-Popup mit Alert, kein Pflichtfeld leer 
              messagebox.showinfo("Pflichtfeld Zeit", "Eines der beiden Zeit-Fenster ist nicht richtig ausgefüllt\nBitte nur im formatt ??:?? ausfüllen.")
              return False
              # ---e---


            string = strings
            numb = string.replace(":", "")
            if not 5 == len(string):
              alert()
              return False
            if not 1 == string.count(":"):
              alert()
              return False
            if not numb.isdigit():
              alert()
              return False
            else:
              return True


          # mit einer forschleife werden automatisiert die Entriews auf not null validiert, gail :-)
          string = [str(e_vorname.get()), str(e_nachname.get()), str(e_gruppenleiter.get()), str(e_grund.get()), str(e_gemeldet_time.get()), str(e_meldepflicht_time.get())]
          for strings in string:
            if not check_string_not_null(strings):
              return
          # nun checken wir ob die zeit vom format stimmt 11:11
          string = [str(e_gemeldet_time.get()), str(e_meldepflicht_time.get())]
          for strings in string:
            if not check_time_okey(strings):
              return

          sql_datensatz = [str(e_vorname.get().title()),
                            str(e_nachname.get().title()),
                            str(e_gruppenleiter.get()),
                            str(global_user),
                            str(e_grund.get()),
                            str(e_abwesend_seid.get()),
                            str(e_gemeldet.get()),
                            str(e_gemeldet_time.get()),
                            str(e_meldepflicht.get()),
                            str(e_meldepflicht_time.get()),
                            str(e_prognose.get()),
                            str(e_notiz.get("1.0","end-1c")),
                            str("A")]
          print(sql_datensatz)                  
          sql_insert_now(sql_datensatz) # funktionen/store_datas_in_db_new_case.py
          try:
            info_neuer_fall(sql_datensatz) # funktionen/send_mail.py
            messagebox.showinfo("Mail Info","Danke\n\nDer Fall ist gespeichert.")
          except:
            messagebox.showwarning("Warnung","Achtung!\n der Fall wurde gespeichert,\ndie Mail wurde aber nicht gesendet,\n Check deine Internetverbindung.")
          
          new.withdraw()
          ww.withdraw()
          hauptfenster()
          

        b_speichern = tk.Button(new, text="speichern", image=speichern_png, 
                                    width=140, bg=cal_col, fg=weiss, font=size_n, 
                                    compound="left", command=speichern_new) #compound regelt wo das Bild sein wird L o R
        b_speichern.grid(row=10, column=4, padx=px, pady=60, sticky="e")

        

      # Content Hauptfenster
      logo_label = tk.Label(second_frame, image=logo, bg="yellow")
      logo_label.image = logo
      logo_label.grid(row=0, column=0, padx=20, pady=50)
      
      
      b_new = tk.Button(second_frame, image=new_png, bg="yellow", command=new_case )
      b_new.image = new_png
      b_new.grid(row=0, column=5, padx=1, pady=50)
      # ---e---

      # sql_homescreen
      """ sql Verbindungsaufbau und filtrierung für Homescreen """
      verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
      zeiger = verbindung.cursor()
      if sql_auswahl:
        try:
          # zeige mir nur die "A"ktiv Abwesenden an
          zeiger.execute("SELECT * FROM mitarbeiter WHERE status='A' ORDER BY id_ DESC;")
        except:
          messagebox.showerror("ERROR keine Verbindung zur Datenbank","Hoop\'s, etwas hat nicht gelkappt, keine Verbindung zur Datenbank. ")
      else:
        try:
          # zeige mir alles
          zeiger.execute("SELECT * FROM mitarbeiter ORDER BY id_ DESC;") 
        except:
          messagebox.showerror("ERROR keine Verbindung zur Datenbank","Hoop\'s, etwas hat nicht gelkappt, keine Verbindung zur Datenbank. ")  

      hoch = 3
      weiss = "white"

      # Ueberschriften für Table Mitarbeiter welche auf dem Homescreen angezeigt werden 333
      l_head_name = tk.Label(second_frame, text=" NAME", width=50, height=1, bg="black", fg=weiss, anchor="w")
      l_head_name.grid(row=1, column=1, padx=1, pady=hoch)
      l_head_meldepflicht = tk.Label(second_frame, text=" MELDEPFLICHT", width=25, height=1, bg="black", fg=weiss)
      l_head_meldepflicht.grid(row=1, column=2, padx=1, pady=hoch)
      l_head_status = tk.Label(second_frame, text=" STATUS ", height=1, bg="black", fg=weiss)
      l_head_status.grid(row=1, column=3, padx=1, pady=hoch)    
      l_head_grl = tk.Label(second_frame, text=" GRUPPENLEITER ",  width=20, height=1, bg="black", fg=weiss)
      l_head_grl.grid(row=1, column=4, padx=1, pady=hoch)
      l_head_bearbeiten = tk.Label(second_frame, text=" EDIT ", width=7, height=1, bg="black", fg=weiss)
      l_head_bearbeiten.grid(row=1, column=5, padx=1, pady=hoch) 
      l_head_mail = tk.Label(second_frame, text="MAIL", bg="black", fg=weiss, width=7, height=1)
      l_head_mail.grid(row=1, column=6, padx=1, pady=hoch)
      if int(berechtigung) >= 2:
        l_head_delete = tk.Label(second_frame, text="DELETE", width=7, height=1, bg="black", fg=weiss)
        l_head_delete.grid(row=1, column=7, padx=1, pady=hoch)
      
      def fallbearbeitung(rows):
            # Übernahme aller Daten der einzelnen Person              
            mitarbeiter_dsatz = rows
            

            """ Fenster Fall bearbeiten """
            fall_bearbeiten = tk.Toplevel(root, bg=farbe)
            fall_bearbeiten.title("Ansicht Mitarbeiter " + mitarbeiter_dsatz[1] + " " + mitarbeiter_dsatz[2])
            fall_bearbeiten.deiconify()  # info .deconifiy zum maximieren und .iconify zum minimieren.
            w, h = fall_bearbeiten.winfo_screenwidth(), fall_bearbeiten.winfo_screenheight()
            fall_bearbeiten.geometry("%dx%d+0+0" % (w, h))

            # Content Fall bearbeiten
            l_bild_dr = tk.Label(fall_bearbeiten, image=arztkoffer_png, bg=farbe, fg=weiss)
            l_bild_dr.image = arztkoffer_png
            l_bild_dr.grid(row=0, column=0, padx=40, pady=40)
            namen = f"{mitarbeiter_dsatz[1]} {mitarbeiter_dsatz[2]}    |    Fallnummer: {mitarbeiter_dsatz[0]}"
            l_namen = tk.Label(fall_bearbeiten, text=namen, bg=farbe, fg=weiss, font=size_xxx)
            l_namen.grid(row=0, column=10, columnspan=29, padx=20, pady=40)
            
            # betreuung
            def betreuung(mitarbeiter_dsatz): 
              dsatz = mitarbeiter_dsatz
              check_is_in_sql(dsatz) # funktionen.betreuung_fun.check_sql()
              betreuung_execute(dsatz) #funktionen.betreuung_fun.betreuung_execute()
              # 111
            b_betreuung_grl = tk.Button(fall_bearbeiten,text="Betreuung", 
                                            bg=farbe, fg=weiss, font=size_n, command=partial(betreuung, mitarbeiter_dsatz))
            b_betreuung_grl.grid(row=0, column=30, padx=20, pady=40, sticky="e")

            # rechnet aus wie viele Tage der MA fehlt
            tag = datetime.strptime(mitarbeiter_dsatz[6], "%d.%m.%Y")
            tagen = heute_time - tag
            text_abwesend = f"Abwesend seit: {mitarbeiter_dsatz[6]}  |  Tage: {tagen.days}"
            l_abwesend = tk.Label(fall_bearbeiten, text=text_abwesend, bg=farbe, fg=weiss, font=size_x, anchor="w")
            l_abwesend.grid(row=1, column=10, columnspan=20, padx=45, pady=hoch, sticky="w")

            
            def edit_grl (mitarbeiter_dsatz, grl):
              mitarbeiter_dsatz = mitarbeiter_dsatz
              grl = grl
              ed_grl(mitarbeiter_dsatz, grl) # oeffnet ein Tk input feld und gibt den neuen Wert in den dsatz zurück
              fall_bearbeiten.withdraw()
              ww.withdraw()
              hauptfenster()  

            b_gruppenleiter = tk.Button(fall_bearbeiten, image=edit_png, bg=farbe, fg=weiss, command=partial(edit_grl, mitarbeiter_dsatz, grl))
            b_gruppenleiter.grid(row=10, column=10, padx=5, pady=hoch, sticky="w")
            l_gruppenleiter = tk.Label(fall_bearbeiten, text="Gruppenleiter: " + mitarbeiter_dsatz[3], bg=farbe, fg=weiss, font=size_n, anchor="w")
            l_gruppenleiter.grid(row=10, column=20, padx=5, pady=hoch, sticky="w")


            def edit_grund(mitarbeiter_dsatz, grund_abwesenheit):
              mitarbeiter_dsatz = mitarbeiter_dsatz
              grund_ = grund_abwesenheit
              ed_grund(mitarbeiter_dsatz, grund_)
              fall_bearbeiten.withdraw()
              ww.withdraw()
              hauptfenster()  
              
              
            b_grund = tk.Button(fall_bearbeiten, image=edit_png, bg=farbe, fg=weiss, command=partial(edit_grund, mitarbeiter_dsatz, grund_abwesenheit))
            b_grund.grid(row=20, column=10, padx=5, pady=hoch, sticky="w")
            l_grund = tk.Label(fall_bearbeiten, text="Grund: " + mitarbeiter_dsatz[5], bg=farbe, fg=weiss, font=size_n, anchor="w")
            l_grund.grid(row=20, column=20, padx=5, pady=hoch, sticky="w")

            def edit_meldepflicht(mitarbeiter_dsatz):
              mitarbeiter_dsatz = mitarbeiter_dsatz
              ed_meld(mitarbeiter_dsatz)
              
              ww.withdraw()
              fall_bearbeiten.withdraw()
              hauptfenster()
            
            
            b_melde = tk.Button(fall_bearbeiten, image=edit_png, bg=farbe, fg=weiss, command=partial(edit_meldepflicht, mitarbeiter_dsatz))
            b_melde.grid(row=30, column=10, padx=5, pady=hoch, sticky="w")
            text_melden = f"Meldepflicht: {mitarbeiter_dsatz[9]} | {mitarbeiter_dsatz[10]}"
            l_melde = tk.Label(fall_bearbeiten, text=text_melden, bg=farbe, fg=weiss, font=size_x, anchor="w")
            l_melde.grid(row=30, column=20, padx=5, pady=hoch, sticky="w")
            text_gemeldet = f"(gemeldet bei {mitarbeiter_dsatz[4]}, am {mitarbeiter_dsatz[7]} - {mitarbeiter_dsatz[8]} Uhr)"
            l_gemeldet = tk.Label(fall_bearbeiten, text=text_gemeldet, bg=farbe, fg=weiss, font=size_n)
            l_gemeldet.grid(row=40, column=20, padx=5, pady=hoch)

            def edit_prognose(mitarbeiter_dsatz):
              mitarbeiter_dsatz = mitarbeiter_dsatz
              ed_prog(mitarbeiter_dsatz) # funktionen.edit_mitarbeiter.ed_prog
              fall_bearbeiten.withdraw()
              ww.withdraw()
              hauptfenster()
              
            b_prognose = tk.Button(fall_bearbeiten, image=edit_png, bg=farbe, fg=weiss, command=partial(edit_prognose, mitarbeiter_dsatz))
            b_prognose.grid(row=50, column=10, padx=5, pady=hoch, sticky="w")
            text_prognose = f"Schätzt sich selbst ca. am {mitarbeiter_dsatz[11]} wieder gesund."
            l_prognose = tk.Label(fall_bearbeiten, text=text_prognose, bg=farbe, fg=weiss, font=size_n, anchor="w")
            l_prognose.grid(row=50, column=20, padx=5, pady=hoch,  ipady=20, sticky="w")

            space = tk.Label(fall_bearbeiten, text="", bg=farbe, fg=weiss, width=10, font=size_n)
            space.grid(row=1, column=29)

            l_notiz_title = tk.Label(fall_bearbeiten, text="Notizen und Infos für die Leitstelle:", bg=farbe, fg=weiss, font=size_x, anchor="w")
            l_notiz_title.grid(row=1, column=30, padx=0, pady=hoch, sticky="w")

            l_notiz = tk.Text(fall_bearbeiten, bg=weiss, fg="blue", font=size_n, height=15, width=60)
            l_notiz.grid(row=10, rowspan=70, column=30, padx=5, pady=hoch, ipadx=10, sticky="w")
            l_notiz.insert(tk.END, mitarbeiter_dsatz[12], "blue")

            def edit_notiz(mitarbeiter_dsatz):
              mitarbeiter_dsatz = mitarbeiter_dsatz
              wert = l_notiz.get("1.0","end-1c")
              ed_notiz(mitarbeiter_dsatz, wert)
              time = datetime.now().strftime("%H:%M:%S")
              b_notiz["text"] = f"ok: {time}"

            b_notiz = tk.Button(fall_bearbeiten, text="Notiz speichern ", image=edit_png, 
                                                  width=150, compound="left", bg="blue", 
                                                  fg=weiss, font=size_n, command=partial(edit_notiz, mitarbeiter_dsatz))
            b_notiz.grid(row=80, column=30, padx=2, pady=hoch, sticky="e")

            l_verlauf_meldungen_u = tk.Label(fall_bearbeiten, text="Velauf, die 4 letzten Meldungen:\nGemeldet Datum/Zeit | Meldepflichten | bearbeitet", 
                                                              anchor="w", justify="left",
                                                              bg=farbe, fg=weiss)
            l_verlauf_meldungen_u.grid(row=81, column=1, padx=2, pady=4, columnspan=100, sticky="w")  

            """ for-schleife Verlauf Meldungen """
            alle_meldungen = select_meldungen_history_in_db(mitarbeiter_dsatz)
            row_index = 100
            durchgänge = 1
            for ds in  reversed(alle_meldungen):
              text_alle_m = f"{ds[0]} {ds[1]} | {ds[2]} {ds[3]} | {ds[4]}"
              label = tk.Label(fall_bearbeiten, text=text_alle_m, bg=farbe, fg=weiss, font=size_n, anchor="w", justify="left")
              label.grid(row=row_index, column=1, padx=2, pady=4, columnspan=20, sticky="w")
              row_index += 1
              if durchgänge == 4:
                break
              durchgänge += 1
            
            """ Gesundmeldung """
            def gesundmeldung(mitarbeiter_dsatz):
              dsatz = mitarbeiter_dsatz
              ges_mel(dsatz) # funktionen.gesundmeldung.py
            
              fall_bearbeiten.withdraw()
              ww.withdraw()
              hauptfenster()
             
            gesund_png_path = Path("icons/gesund.png")
            gesund_png = tk.PhotoImage(file=gesund_png_path)
            b_gesundmeldung = tk.Button(fall_bearbeiten, text="Gesundmeldung", image=gesund_png, width=180,
                                                        compound="left", font=size_n, bg="green", fg=weiss,
                                                        anchor="e", command = partial(gesundmeldung, mitarbeiter_dsatz))
            b_gesundmeldung.grid(row=100, rowspan=30, column=30, padx=5, pady=5, sticky="e")
            b_gesundmeldung.image = gesund_png
            

      """ Hauptfenster alle mitarbeiter """
      row_number = 2  
      inhalt = zeiger.fetchall()
      verbindung.commit()
      verbindung.close()     
     
     
      def gost(sql_auswahl):
        sql_auswahl = sql_auswahl
        if sql_auswahl:
          sql_auswahl = False
        else:
          sql_auswahl = True

        ww.withdraw()
        hauptfenster(sql_auswahl)     

      b_alle_fälle_inkl_der_gesunden = tk.Button(second_frame, image=gost_png, bg="yellow", fg="white", command=partial(gost, sql_auswahl))
      b_alle_fälle_inkl_der_gesunden.grid(row=0, column=6, padx=1, pady=50)

  
      """ Mit der Forschleife werden alle Abwesenden auf die TK gelabelt 333 """
      
      for rows in inhalt:
          lab_tex = " " + rows[1] + " " + rows[2] 
          l_name = tk.Label(second_frame, text=lab_tex, width=50, height=hoch, bg="gold", fg="black", anchor="w")
          l_name.grid(row=row_number, column=1, padx=1, pady=hoch)
          meldepflicht_text = rows[9] + " | " + rows[10] + " Uhr"
          label_mepf = tk.Label(second_frame, text=meldepflicht_text, width=25, height=hoch, bg="gold", fg="black")
          label_mepf.grid(row=row_number, column=2, padx=1, pady=hoch)
          status = "1"
          # status Funktion
          control0 = rows[9]
          control1 = datetime.now() 
          dateString = f"{rows[9]} {rows[10]}"
          dateFormatter = "%d.%m.%Y %H:%M"
          control2 = datetime.strptime(dateString, dateFormatter)
          if heute.strftime("%d.%m.%Y") == control0:
            status = "2"
          if control1 > control2:
            status = "3"
          bild_status = str(status + ".png")
          bild_path_compl = "icons/status/" + bild_status 
          bild = tk.PhotoImage(file=bild_path_compl)
          label_status = tk.Label(second_frame, image=bild, bg="gold", fg="black")
          label_status.image = bild
          label_status.grid(row=row_number, column=3, padx=1, pady=hoch)
          label_grl = tk.Label(second_frame, text=rows[3], width=20, height=hoch, bg="gold", fg="black", anchor="w")
          label_grl.grid(row=row_number, column=4, padx=1, pady=hoch)

          # button um in den einzelnen Fall rein gehen         
          b_lupe = tk.Button(second_frame, image=lupe_png, bg="gold", command=partial(fallbearbeitung, rows))
          b_lupe.image = lupe_png
          b_lupe.grid(row=row_number, column=5, padx=1, pady=hoch)

          def send_info(rows):
            dsatz = rows
            # öffnet Fenster um kurze info zu schreiben und sendet sie an den entsprechenden Grl ab
            send_i(dsatz)

            ww.withdraw()
            hauptfenster()
            #---e--- 

          b_send_mail = tk.Button(second_frame, image=send_png, bg="gold", fg="black", command=partial(send_info, rows))
          b_send_mail.grid(row=row_number, column=6, padx=1, pady=hoch)
          
          def del_case(rows):
            rows = rows
            sql_delete_id(rows) # funktionen.edit_mitarbeiter.del_case
            ww.withdraw()
            hauptfenster()

          # wenn die berechtigung mehr wie 2 ist, zeige auch die Del Buttons
          if int(berechtigung) >= 2:
            b_delete_case = tk.Button(second_frame, image=delete_png, bg="gold", fg="Black", command=partial(del_case, rows))
            b_delete_case.grid(row=row_number, column=7, padx=1, pady=hoch)

          # wenn die fälle status "G" haben, färbe sie grau!
          if rows[13] == "G":
            liste_labels = [l_name, label_mepf, label_grl]
            for labels in liste_labels:
              labels["bg"] ="#BABDB6"
             
          row_number += 1
      row_space = row_number + 2
      space = tk.Label(second_frame, text="", bg="yellow", fg="yellow")
      space.grid(row=row_space, column=0, pady=100)

    hauptfenster()


  else:
    """ Zugangsdaten NICHT ok """
    # Toplevel-Popup mit Alert, kein Zugang 
    alert = tk.Toplevel(root, bg="black")
    alert.title("Zugang verweigert!")
    w, h = 550, 200
    alert.geometry("%dx%d+550+350" % (w, h))
    alert.focus_set()

    # Funktion um das Alertpopup zu schliessen
    def kill_alert(event=None):
        alert.destroy()
        alert.update()

    l_bild_important = tk.Label(alert, image=important_png, bg="black")
    l_bild_important.image = important_png
    l_bild_important.grid(row=0, column=0, padx=5, pady=10)
    l_ueberschrift = tk.Label(alert, text="Passwort oder Benutzernamen falsch!!", bg="black", fg="white", font=("verdana", 14, "bold"))
    l_ueberschrift.grid(row=0, column=1, padx=5, pady=5)
    l_alert_nachricht = tk.Label(alert, 
        text="Leider hat etwas nicht geklappt,\nentweder ist das Passwort falsch oder dein Benutzername.\nVersuche es nochmal.",
        bg="black", fg="white", font=size_n)
    l_alert_nachricht.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    b_ok = tk.Button(alert, text="okey", fg="white", bg="black", command=kill_alert)
    b_ok.grid(row=2, column=1, padx=20, pady=5)
    b_ok.bind('<Return>', kill_alert)
    # ---e---

""" loginfenster antrag auf account """
def antrag():
  top_account = tk.Toplevel()
  top_account.title("- Antrag auf eine neue Zugangsberechtigung -")
  top_account.deiconify()  # info .deconifiy zum maximieren und .iconify zum minimieren.
  w, h = top_account.winfo_screenwidth(), top_account.winfo_screenheight()
  top_account.geometry("%dx%d+0+0" % (w, h))
  top_account.configure(bg='yellow')
  top_account.focus_set()
  l_label1 = tk.Label(top_account, text="Ich wünsche einen Zugang zur Dispo-App",
                                    bg="yellow", fg="black", font=("verdana", 16, "bold"))
  l_label1.pack(pady=20)
  text2 = "Bitte beachte, dass deine Zugangsberechtigung erst geprüft werden muss,\n\
    in der Regel brauchen wir wärend der Bürozeit eine Reaktionszeit von einer Stunde,\n\
    bei Unklarheiten ob die Berechtigung legitim ist, kann der Prozess aber wesentlich länger dauern."
  l_label2 = tk.Label(top_account, text=text2, bg="yellow", fg="black", font=size_n)
  l_label2.pack(pady=20)
  
  text3 = f"Dein Username wird \"{getuser}\" sein.\n\nBitte gebe ein Wunschpassword ein (mind 8 Zeichen)"
  l_label3 = tk.Label(top_account, text=text3, bg="yellow", fg="black", font=size_n)
  l_label3.pack(pady=20)

  e_code_new = tk.Entry(top_account, width=20)
  e_code_new.pack(pady=33)

  # entgegennahme des eingegebenen Passworts
  pd = e_code_new.get()

  def antrag():
    try:
      send_new_account(getuser, pd)
      messagebox.showinfo("Mail info","Dein Antrag wurde gesendet,\nwir behandeln dein Antrag so schnell wie möglich")
    except:
      messagebox.showerror("Error Mail","Achtung, aus techn. Gründen, konnte dein Antrag nicht versendet werden, versuche es später nochmal.")
    
  b_senden_account = tk.Button(top_account, text="Senden", bg="black", fg="gold", font=size_x, 
                                                  command = antrag)
  b_senden_account.pack(pady=40)

""" loginfenster content """
b_antrag_auf_account = tk.Button(root, text="Antrag auf einen User-Account", 
                                      bg="yellow", fg="brown", relief="groov", font=size_n, command=antrag)
b_antrag_auf_account.grid(row=4, column=20, pady=150)
userInEntry = str(getuser)
l_hello = tk.Label(root, text="Bitte log dich ein:", bg=hintergrund, fg=schriftfarbe,font=size_xx)
l_hello.grid(row=1, column=10, padx=5, pady=50)
l_user = tk.Label(root, text="Benutzer:", bg=hintergrund, fg=schriftfarbe, font=size_x, width=8, anchor="w")
l_user.grid(row=2, column=10, padx=5, pady=5)
l_code = tk.Label(root, text="Passwort:", bg=hintergrund, fg=schriftfarbe, font=size_x, width=8, anchor="w")
l_code.grid(row=3, column=10, padx=5, pady=10)
e_user = tk.Entry(root, font=size_n, width=33)
e_user.grid(row=2, column=20, padx=1, pady=5)
e_user.insert(0, userInEntry)
e_code = tk.Entry(root, font=size_n, width=33, show=bullet)
e_code.grid(row=3, column=20, padx=1, pady=20)
e_code.bind('<Return>', Try_user_login)
# ---e---

""" END OF PARTY """
root.mainloop()  
