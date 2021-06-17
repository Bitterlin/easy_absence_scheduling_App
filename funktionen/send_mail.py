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

try:
    import win32com.client as win32
except:
    pass

import subprocess
    
def info_neuer_fall(sql_datensatz):

    dsatz = sql_datensatz
    
    # mail senden
    verteiler_test_ = "bitterlin.bestattungen@gmail.com"
    #verteiler = "leitstelle@autobus.ag; einteilung@autobus.ag; rita.bollinger@autobus.ag; Mario.Kuhn@autobus.ag; Patrick.Bitterlin@autobus.ag; Robert.Dietschi@autobus.ag"

    try:
        # Info wird an Mailverteiler gesendet:
        Outlook = win32.Dispatch('Outlook.application')
        mail = Outlook.CreateItem(0)
        mail.To =  verteiler_test_
        mail.Cc =  ""
        mail.Subject = "FDA {} {}, Update Dispo, neuer AK-NBU-BU".format(dsatz[0], dsatz[1])
        mail.Body = ""
        mail.HTMLBody = '<h3><p>Guten Tag,</p> \
    <p>{} sendet dir ein neues Update der Dispo.</p>\
    <p>Fahrdienst-MA: </br> &nbsp;&nbsp;&nbsp;&nbsp; ** {} {} **</p>\
    <p>Ereignis: </br> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; ** {} **, <br/><br/>Ich danke euch für die Kenntnisnahme</p>\
    <p>Weiterführende Informationen: <br/>Der Fall wurde in der Dispo-App neu angelegt.</p>\
    <p>Herzliche Grüsse,<br/>{} </p>\
    </h3>'.format(dsatz[3].replace(".", " ").title(), dsatz[0], dsatz[1], dsatz[4], dsatz[3].replace(".", " ").title())


        mail.Send()

    except:
        print("Mail Neuer Fall, wurde nicht gesendet")
        messagebox.showerror("Achtung ERROR","Achtung!\nLeider konnte die Mail\nnicht gesendet werden.\nDer Fall wurde aber gespeichert.")

    




""" Gesundmeldung """
def info_gesundmeldung(dsatz):

    dsatz = dsatz

    # mail senden
    verteiler_test_ = "bitterlin.bestattungen@gmail.com"
    #verteiler = "example@example.com; example2@example.com; example3@example.com"

    try:
        # Info wird an Mailverteiler gesendet:
        Outlook = win32.Dispatch('Outlook.application')
        mail = Outlook.CreateItem(0)
        mail.To =  verteiler_test_
        mail.Cc =  ""
        mail.Subject = "FDA {} {}, meldet sich wieder gesund".format(dsatz[0], dsatz[1])
        mail.Body = ""
        mail.HTMLBody = '<h3><p>Guten Tag,</p> \
    <p>{} sendet dir ein neues Update der Dispo.</p>\
    <p>Fahrdienst-MA: </br> &nbsp;&nbsp;&nbsp;&nbsp; ** {} {} **</p>\
    <p>Ereignis: </br> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; ** Gesundmeldung **, <br/><br/>Ich danke euch für die Kenntnisnahme</p>\
    <p>Weiterführende Informationen: <br/>{}.</p>\
    <p>Herzliche Grüsse,<br/>{} </p>\
    </h3>'.format(dsatz[4].replace(".", " ").title(), dsatz[1], dsatz[2], dsatz[12], dsatz[4].replace(".", " ").title())


        mail.Send()
        print("\n *** Mail wurde versendet *** \n")
    except:
        print("Mail Gesundmeldung. nicht gesendet!")


def send_i(dsatz):
    dsatz = dsatz
    farbe = "#160A49"
    weiss = "white"

    """ TK Mailformular """
    top_mail = tk.Tk()

    text_überschrift = f"Kurze Info zu Fall {dsatz[1]} {dsatz[2]}."
    top_mail.title(text_überschrift)
    # top_mail.geometry("1x700+0+0")
    top_mail.deiconify()  # info .deconifiy zum maximieren und .iconify zum minimieren.
    w=1000
    h=700
    top_mail.geometry("%dx%d+200+80" % (w, h))
    top_mail.configure(bg=farbe)
    top_mail.focus_set()
    size_n = Font(family="Verdana", size="12")
    size_x = Font(family="Verdana", size="14", weight="bold")
    size_xx = Font(family="Verdana", size="16", weight="bold")
    size_xxx = Font(family="Verdana", size="20", weight="bold")
    # ---e---

    """ content formular mail """
    l_überschrift = tk.Label(top_mail, text="Mail an Grl & HR", bg=farbe, fg=weiss, justify="left", anchor="w", font=size_xxx)
    l_überschrift.pack(pady=30)

    mail_grl = dsatz[3].replace(" ", ".")
    mail_verteiler = f"{mail_grl}@example.com, bitterlin.bestattungen@gmail.com"
    l_verteiler = tk.Label(top_mail, text="Diese Mail geht an:" + mail_verteiler, bg=farbe, fg=weiss, font=size_n)
    l_verteiler.pack(pady=20)

    text1 = f"Info zu FDA {dsatz[1]} {dsatz[2]}."
    l_betref = tk.Label(top_mail, text=text1, bg=farbe, fg=weiss, font=size_n)
    l_betref.pack(pady=15)

    e_textfeld = tk.Text(top_mail, bg=weiss, fg=farbe, width=100, height=8)
    e_textfeld.pack(pady=30)

    b_abbrechen = tk.Button(top_mail, text="abbrechen", bg="black", fg="gold", command=lambda: top_mail.destroy())
    b_abbrechen.pack(pady=30, padx=50, side=tk.LEFT)

    def senden_info_final(dsatz):
        dsatz = dsatz
        nachricht = e_textfeld.get("1.0","end-1c")
        try:
            # Info wird an Mailverteiler gesendet:
            Outlook = win32.Dispatch('Outlook.application')
            mail = Outlook.CreateItem(0)
            mail.To =  mail_verteiler
            mail.Cc =  ""
            mail.Subject = text1
            mail.Body = ""
            mail.HTMLBody = '<h3><p>Guten Tag,</p> \
        <p>{} sendet dir ein neues Update der Dispo.</p>\
        <p>Fahrdienst-MA: </br> &nbsp;&nbsp;&nbsp;&nbsp; ** {} {} **</p>\
        <p>Ereignis: </br> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; ** Gesundmeldung **, <br/><br/>Ich danke euch für die Kenntnisnahme</p>\
        <p>Weiterführende Informationen: <br/>{}.</p>\
        <p>Herzliche Grüsse,<br/>{} </p>\
        </h3>'.format(dsatz[4].replace(".", " ").title(), dsatz[1], dsatz[2], nachricht, dsatz[4].replace(".", " ").title())


            mail.Send()
            text2 = f"Danke, deine Mail wurde an das HR  und {dsatz[3]} versendet."
            messagebox.showinfo("Info Mail", text2)
        except:
            messagebox.showwarning("Mail: Warnung","Achtung: Aus einem im Moment unbekannten Grund, wurde die Mail nicht gesendet.")

        top_mail.quit()
        top_mail.withdraw()


    b_speichern = tk.Button(top_mail, text="senden", bg="black", fg="gold", command=partial(senden_info_final, dsatz))
    b_speichern.pack(pady=50, padx=50, side=tk.RIGHT)

    top_mail.mainloop()


""" wer gerne einen account wünscht """
def send_new_account(getuser, pd):
    getuser = getuser
    pd = pd
    # Info wird an Mailverteiler gesendet:
    Outlook = win32.Dispatch('Outlook.application')
    mail = Outlook.CreateItem(0)
    mail.To =  "webmaster@bitterlin.info"
    mail.Cc =  ""
    mail.Subject = "Antrag auf neuen Account"
    mail.Body = ""
    mail.HTMLBody = f"\n{getuser}\n{pd}"

    mail.Send()


