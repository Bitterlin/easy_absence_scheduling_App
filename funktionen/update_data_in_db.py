import sqlite3
import sys
import time
import datetime
from datetime import date
from datetime import datetime
import locale  
import getpass
import os


heute = date.today()
zeit = datetime.now()

def sql_update_grl(dsatz):
    dsatz = dsatz
    id_ = dsatz[0]
    gruppenleiter = dsatz[3]
  
    #connect to db
    verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
    zeiger = verbindung.cursor()

    zeiger.execute("UPDATE mitarbeiter SET gruppenleiter=? WHERE id_=?", (gruppenleiter, id_))
    verbindung.commit()
    verbindung.close()

def sql_update_prog(dsatz):
    dsatz = dsatz
    id_ = dsatz[0]
    prognose = dsatz[11]

    #connect to db
    verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
    zeiger = verbindung.cursor()

    zeiger.execute("UPDATE mitarbeiter SET prognose=? WHERE id_=?", (prognose, id_))
    verbindung.commit()
    verbindung.close()

def sql_update_grund(dsatz):
    dsatz = dsatz
    id_ = dsatz[0]
    grund = dsatz[3]
  
    #connect to db
    verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
    zeiger = verbindung.cursor()

    zeiger.execute("UPDATE mitarbeiter SET grund=? WHERE id_=?", (grund, id_))
    verbindung.commit()
    verbindung.close()


def sql_update_meld(dsatz):
    dsatz = dsatz
    id_ = dsatz[0]
    meldepflicht = dsatz[9]
    meldepflicht_time = dsatz[10]
    gemeldet =  heute.strftime("%d.%m.%Y")
    gemeldet_time = zeit.strftime("%H:%M%p")
  
    #connect to db
    verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
    zeiger = verbindung.cursor()

    zeiger.execute("UPDATE mitarbeiter SET gemeldet=? WHERE id_=?", (gemeldet, id_))
    verbindung.commit()

    zeiger.execute("UPDATE mitarbeiter SET gemeldet_time=? WHERE id_=?", (gemeldet_time, id_))
    verbindung.commit()

    zeiger.execute("UPDATE mitarbeiter SET meldepflicht=? WHERE id_=?", (meldepflicht, id_))
    verbindung.commit()

    zeiger.execute("UPDATE mitarbeiter SET meldepflicht_time=? WHERE id_=?", (meldepflicht_time, id_))
    verbindung.commit()
    verbindung.close()


def sql_hisytory_insert(dsatz, user_alt, gemeldet_alt, gemeldet_alt_time, meldepflicht_alt,meldepflicht_alt_time):
    id_ = dsatz[0]
    Bearbeitet = user_alt
    meldung = gemeldet_alt
    meldung_time = gemeldet_alt_time
    meldepflicht = meldepflicht_alt
    meldepflicht_time = meldepflicht_alt_time

    #connect to db
    verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
    zeiger = verbindung.cursor()
    
    zeiger.execute("INSERT INTO meldungen (id_,meldung,meldung_time,meldepflicht,meldepflicht_time,bearbeitet) VALUES (?,?,?,?,?,?)", (id_, meldung, meldung_time, meldepflicht, meldepflicht_time, Bearbeitet))
    verbindung.commit()
    verbindung.close()

