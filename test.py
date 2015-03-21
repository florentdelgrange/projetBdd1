#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from bdd import *

con = lite.connect('test.db')
with con:
    cur = con.cursor()
    line = []
    cur = con.cursor()

    for raw in cur.execute("select name from sqlite_master where type = 'table'"):
        line.append(raw)
        if raw[0]=='Cars':
            print 'vrai'
        print raw[0]
    print line
    for raw in cur.execute("PRAGMA table_info(Cars)"):
         print raw[1],
    print #retour a la ligne

print(split_str("michel ma belle sont des mots qui vont tres bien ensembles"))
print(checkIn(['a','b','c'], ['x','b','v','d','a','g','c','s']))