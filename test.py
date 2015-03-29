#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from normalisation import *

con = lite.connect('test.db')
with con:
    cur = con.cursor()
    line = []
    cur = con.cursor()

    for raw in cur.execute("select name from sqlite_master where type = 'table'"):
        line.append(raw)
        if raw[0]=='Cars':
            print ('vrai')
        print (raw[0])
    print (line)
    list=[]
    for raw in cur.execute("PRAGMA table_info(Cars)"):
         list.append(raw[1])
    print (list)
    print #retour a la ligne

def is_useless(functional_dependencies,triplet):
        for df in functional_dependencies:
            if triplet[0] == df[0] and triplet[2] == df[2] and included_in(split_str(df[1]),split_str(triplet[1])):
                return True
        return False

def get_logical_consequence(functional_dependencies):
        logical_cons = []
        for df in functional_dependencies:
            part = partiesliste(split_str(df[1]))
            print df,
            print ' => parties : ',
            print part
            sigma = functional_dependencies[:]
            sigma.remove(df)
            for sub_X in part:
                print sub_X,
                print ' -> ',
                implicated = find_consequence(sub_X, sigma)
                print implicated
                if df[2] in implicated:
                    print sub_X,
                    print ' -> ',
                    print df[2],
                    print 'so',
                    print df,
                    print 'is a logical consequence'
                    logical_cons.append(df)
                    break
        print
        return logical_cons

print(split_str("michel ma belle sont des mots qui vont tres bien ensembles"))
print(included_in(['a','b','c'], ['x','b','v','d','a','g','c','s']))
print ("\n \n")
print ('\n \n')
print (get_logical_consequence([('t', 'C D', 'B'), ('t','A','E'), ('t', 'E F', 'A'), ('t', 'C','D'), ('t', 'A B E', 'F'), ('t', 'A B E', 'C'), ('t', 'A B', 'C'), ('t', 'A E', 'F')]))
print (get_logical_consequence([('t', 'A', 'C'), ('t', 'A', 'B'), ('t', 'B A', 'C')]))
print (get_logical_consequence([("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")]))
#normalisation
print (not_involved("t", [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")], ["A","B","C","D","E","F","G","H"]))
print (find_consequence(["B"], [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")]))
print(find_super_key("t", ["A","B","C","D","E","F","G","H"], [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")]))
print (find_key("t", ["A","B","C","D","E","F","G","H"], [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")]))
print (find_key('t', ['A','B','C', 'D', 'E', 'F'], [('t', 'C D', 'B'), ('t','A','E'), ('t', 'E F', 'A'), ('t', 'C','D'), ('t', 'A B E', 'F'), ('t', 'A B E', 'C'), ('t', 'A B', 'C'), ('t', 'A E', 'F')]))
print (find_key('t',['A','B','C', 'D', 'E', 'F'], [('t',' A B C D E F', 'D'), ('t', 'A C', 'E'), ('t','A B D', 'C'), ('t', 'E B', 'F'), ('t', 'E F', 'A'), ('t', 'E F', 'B'), ('t', 'E F', 'C'), ('t', 'A F', 'B'), ('t', 'A F', 'C')]))
print get_logical_consequence([('table', 'A', 'B'), ('table', 'B', 'C'), ('table', 'A', 'C')])
print
print (find_key('t', ['A','B','C', 'D', 'E', 'F'], [('t', 'C D', 'B'), ('t','A','E'), ('t', 'E F', 'A'), ('t', 'C','D'), ('t', 'A B E', 'F'), ('t', 'A B E', 'C'), ('t', 'A B', 'C'), ('t', 'A E', 'F')]))
print union(['Arabseque','Bretagne','Chien', 'Detritus', 'Enfant', 'Film'], ['michel', 'Chien', 'Chat'])
print included_in(['Chien', 'Michel', 'Chat'], ['Horloge', 'Michel', 'Chien', 'Grue', 'Chat'])
print equals(['Lord', 'Voldemort'], ['Voldemort', 'Lord'])
print (get_logical_consequence([('t',' A B C D E F', 'D'), ('t', 'A C', 'E'), ('t','A B D', 'C'), ('t', 'E B', 'F'), ('t', 'E F', 'A'), ('t', 'E F', 'B'), ('t', 'E F', 'C'), ('t', 'A F', 'B'), ('t', 'A F', 'C')]))
print (find_key('t',['Arabesque','Bretagne','Chien', 'Detritus', 'Enfant', 'Film'], [('t','Arabesque Bretagne Chien Detritus Enfant Film', 'Detritus'), ('t', 'Arabesque Chien', 'Enfant'), ('t','Arabesque Bretagne Detritus', 'Chien'), ('t', 'Enfant Bretagne', 'Film'), ('t', 'Enfant Film', 'Arabesque'), ('t', 'Enfant Film', 'Bretagne'), ('t', 'Enfant Film', 'Chien'), ('t', 'Arabesque Film', 'Bretagne'), ('t', 'Arabesque Film', 'Chien')]))
print get_logical_consequence([('myTable', 'C E', 'A'),('myTable', 'C', 'D'),('myTable', 'A', 'B'),('myTable', 'D', 'B'),('myTable', 'D', 'E'),('myTable', 'B', 'F'),('myTable', 'A D', 'C'),('myTable', 'A D', 'F')])
print get_minimal_funcDep([('myTable', 'A B', 'C'),('myTable', 'A B C', 'D')])
print (is_3NF('t',['A','B','C', 'D', 'E', 'F'], [('t',' A B C D E F', 'D'), ('t', 'A C', 'E'), ('t','A B D', 'C'), ('t', 'E B', 'F'), ('t', 'E F', 'A'), ('t', 'E F', 'B'), ('t', 'E F', 'C'), ('t', 'A F', 'B'), ('t', 'A F', 'C')]))
print (is_3NF("t", ["A","B","C","D","E","F","G","H"], [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")]))
print (is_3NF('t', ['A','B','C', 'D', 'E', 'F'], [('t', 'C D', 'B'), ('t','A','E'), ('t', 'E F', 'A'), ('t', 'C','D'), ('t', 'A B E', 'F'), ('t', 'A B E', 'C'), ('t', 'A B', 'C'), ('t', 'A E', 'F')]))

