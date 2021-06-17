import sqlite3



def select_meldungen_history_in_db(mitarbeiter_dsatz):
    dsatz = mitarbeiter_dsatz
    id_ = dsatz[0]
    
    # connect to db
    verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
    zeiger = verbindung.cursor()

    zeiger.execute("SELECT meldung, meldung_time, meldepflicht, meldepflicht_time, bearbeitet FROM meldungen WHERE id_=?",(id_,))
    ausgabe = zeiger.fetchall()
    
    verbindung.commit()
    verbindung.close()
    #print(ausgabe)
    return ausgabe

