__author__ = 'Flo'

import sqlite3 as lite

con = lite.connect('exams_bdd.db')
with con:

    cur = con.cursor()
    cur.execute("CREATE TABLE exam2012(A TEXT, B TEXT, C TEXT, D TEXT, E TEXT, F TEXT, G TEXT, H TEXT)")
    cur.execute("CREATE TABLE exam2013(A INT, B INT, C INT, D INT, E INT, F INT)")
    cur.execute("INSERT INTO exam2012 VALUES ('PERRIER', 'FRAISE', 'POUR', 'LES BALAISES', 'PERRIER', 'GRENADINE', 'POUR', 'LES GAMINES')")
    cur.execute("INSERT INTO exam2012 VALUES (1,2,3,4,5,6,7,8)")
    for raw in cur.execute("SELECT * FROM exam2012"):
        print raw
    for raw in cur.execute("SELECT * FROM exam2013"):
        print raw
    con.commit()
    cur.close()
con.close()