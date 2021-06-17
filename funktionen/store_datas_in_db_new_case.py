
import sqlite3

def sql_insert_now(sql_datensatz):
    dsatz = sql_datensatz
    vorname = dsatz[0]
    nachname = dsatz[1]
    gruppenleiter = dsatz[2]
    bearbeitet = dsatz[3]
    grund = dsatz[4]
    abwesend_seit = dsatz[5]
    gemeldet = dsatz[6]
    gemeldet_time =dsatz[7]
    meldepflicht = dsatz[8]
    meldepflicht_time = dsatz[9]
    prognose = dsatz[10]
    notiz = dsatz[11]
    if notiz == "":
        notiz = "Noch keine Notiz hinterlegt."
    status = dsatz[12]

    #connect to db
    verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
    zeiger = verbindung.cursor()

    zeiger.execute("INSERT INTO mitarbeiter (vorname, nachname, gruppenleiter, bearbeitet, grund, abwesend_seit, gemeldet, gemeldet_time, meldepflicht, meldepflicht_time, prognose, notiz, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (vorname, nachname, gruppenleiter, bearbeitet, grund, abwesend_seit, gemeldet, gemeldet_time, meldepflicht, meldepflicht_time, prognose, notiz, status))
    verbindung.commit()
    verbindung.close()