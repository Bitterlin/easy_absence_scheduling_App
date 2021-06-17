import sqlite3

verbindung = sqlite3.connect("datenbank/abwesenheiten.db")
zeiger = verbindung.cursor()


### create maintable ###
sql_anweisung_create_table_mitarbeiter = """
CREATE TABLE IF NOT EXISTS mitarbeiter (
id_ INTEGER PRIMARY KEY AUTOINCREMENT,
vorname VARCHAR(20),
nachname VARCHAR(30),
gruppenleiter VARCHAR(4),
bearbeitet VARCHAR(4),
grund VARCHAR(20),
abwesend_seit DATE,
gemeldet DATE,
gemeldet_time TIME,
meldepflicht DATE,
meldepflicht_time TIME,
prognose DATE,
notiz TEXT,
status VARCHAR(1))"""

zeiger.execute(sql_anweisung_create_table_mitarbeiter)
# --- e ---


### create table Zugänge User###
sql_anweisung_create_table_user = """
CREATE TABLE IF NOT EXISTS user (
user_id VARCHAR(30) PRIMARY KEY,
code VARCHAR(50),
check_ok VARCHAR(80),
berechtigung INTEGER(5))"""

zeiger.execute(sql_anweisung_create_table_user)
# --- e ---


### create table archiv meldungen###
sql_anweisung_create_table_meldungen = """
CREATE TABLE IF NOT EXISTS meldungen (
id_ INTEGER(10),
meldung DATE,
meldung_time TIME,
meldepflicht DATE,
meldepflicht_time TIME,
bearbeitet VARCHAR(4))"""

zeiger.execute(sql_anweisung_create_table_meldungen)
# --- e ---

### create table Gesundmeldung ###
sql_anweisung_create_table_gesundmeldung = """
CREATE TABLE IF NOT EXISTS gesundmeldung (
id_ INTEGER(10),
meldung DATE,
meldung_time TIME,
Gesundgemeldet_auf DATE,
bearbeitet VARCHAR(4))"""

zeiger.execute(sql_anweisung_create_table_gesundmeldung)
verbindung.close()

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§

""" zweite Datenbank nurn für Führung """
verbindung_secure = sqlite3.connect("datenbank/secure.db")
zeiger_secure = verbindung_secure.cursor()

### create table betreuung ###
sql_anweisung_create_table_betreuung = """
CREATE TABLE IF NOT EXISTS betreuung (
id_ INTEGER(10),
Gespräche TEXT,
Verhalten INTEGER(1),
Integration INTEGER(1),
Aufenthalt INTEGER(1),
Wille INTEGER(1),
Glaubhaftigkeit INTEGER(1),
Regelmässigkeit INTEGER(1),
Fahrtüchtigkeit INTEGER(1),
Sperrfrist INTEGER(1),
Ferienkürzung INTEGER(1),
Case_management INTEGER(1),
Vertrauensarzt INTEGER(1),
Coach INTEGER(1),
Iv INTEGER(1),
Reha INTEGER(1),
Frühpensionierung INTEGER(1),
Sperrfrist_date DATE)"""

zeiger_secure.execute(sql_anweisung_create_table_betreuung)
verbindung_secure.close()

""" """
# 0 id_ 
# 1 gesprache 
# 2 verhalten 
# 3 integration 
# 4 aufenthalt 
# 5 wille 
# 6 glaubhaftigkeit 
# 7 regelmassigkeit 
# 8 fahrtuchtigkeit 
# 9 sperrfrist 
#10 ferienkurzung 
#11 case_management 
#12 vertrauensarzt 
#13 coach
#14 iv 
#15 reha 
#16 frupensionierung 
#17 sperrfrist_date 
""" """

# # Zweite Anweisung
# sql_anweisung = "INSERT INTO mitarbeiter VALUES('Patrick', 'Bitterlin')"
# zeiger.execute(sql_anweisung)
# # Tritte Anweisung
# sql_anweisung = "SELECT * FROM mitarbeiter"
# zeiger.execute(sql_anweisung)
# inhalt = zeiger.fetchall()
# print(inhalt)
# verbindung.commit()
# verbindung.close()