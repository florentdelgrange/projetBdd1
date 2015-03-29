import sqlite3 as lite
import sys

from normalisation import *

class Bdd(object):
    def __init__(self, bdd_name):
        print("Type \'help\' to know how use SGBD")
        print("Type \'exit\' to quit SGBD")
        self.conn = lite.connect(bdd_name+'.db')
        with self.conn:
            cur = self.conn.cursor()
            table_list = []
            for table in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
                table_list.append(table[0])
            if "FuncDep" not in table_list:
                cur.execute("CREATE TABLE FuncDep(name TEXT, X TEXT, A TEXT )")
                self.conn.commit()
            cur.close()



    def get_tables(self):
        table_list = []
        with self.conn:
            cur = self.conn.cursor()
            for table in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
                table_list.append(table[0])
        cur.close()
        return table_list

    def funcDep(self):
        funcDep = []
        with self.conn:
            cur = self.conn.cursor()
            for l in cur.execute("SELECT * FROM FuncDep"):
                funcDep.append(l)
        cur.close()
        return funcDep

    def get_table_funcDep(self,table):
        funcDep = []
        with self.conn:
            cur = self.conn.cursor()
            for l in cur.execute("SELECT * FROM FuncDep"):
                if l[0] == table:
                    funcDep.append(l)
        cur.close()
        return funcDep

    def add_dep(self, triplet):
        if(self.detection(triplet)):
            with self.conn:
                cur = self.conn.cursor()
                cur.execute("INSERT INTO FuncDep VALUES (?, ?, ?)", triplet)
                cur.close()
            self.conn.commit()

    def delete_dep(self, triplet):
        if triplet not in self.funcDep():
            return False
        else:
            with self.conn:
                cur = self.conn.cursor()
                cur.execute("DELETE FROM FuncDep WHERE name=? AND X=? AND A=?", triplet)
                cur.close()
            self.conn.commit()
            return True

    def get_attributes(self,table):
        list=[]
        with self.conn:
            cur = self.conn.cursor()
            for raw in cur.execute("PRAGMA table_info("+table+")"):
                list.append(raw[1])
            cur.close()
        return list

    def detection(self, triplet):
        #Test n1 : est-ce que la table (triplet[0]) existe ?
        if triplet[0] not in self.get_tables():
            print ("la table n'existe pas")
            return False
        #Test n2 : est ce que les attributs de la dependance fonctionnelle entree en parametre sont bien dans cette table ?
        parameters = split_str(triplet[1]) + [triplet[2]]
        if not included_in(parameters, self.get_attributes(triplet[0])):
            print ("les attributs n'existent pas")
            return False
        #Test n3 : est ce que cette df est utile ?
        return not self.is_useless(triplet)

    #retourne les dependences fonctionelles non respectees dans la table entree en parametre
    def respect(self, table):
        list = []
        sigma = self.get_table_funcDep(table)
        with self.conn:
            cur = self.conn.cursor()
            for df in sigma:
                boolean = True
                for raw1 in cur.execute('SELECT ' + df[1].replace(' ', ',') + ',' + df[2] + ' FROM ' + table):
                    if boolean:
                        for raw2 in cur.execute('SELECT ' + df[1].replace(' ', ',') + ',' + df[2] + ' FROM ' + table):
                            if raw1[:len(raw1)-1] == raw2[:len(raw2)-1] and raw1[len(raw1)-1] != raw2[len(raw2)-1]:
                                list.append(df)
                                boolean = False
                                break
                    else:
                        break
            cur.close()
        return list

    def is_useless(self,triplet):
        for df in self.funcDep():
            if triplet[0] == df[0] and triplet[2] == df[2] and equals(split_str(df[1]),split_str(triplet[1])):
                return True
        return False

    def get_logical_consequence(self, table):
        logical_cons = []
        funcDep = self.get_table_funcDep(table)
        for df in funcDep:
            part = partiesliste(split_str(df[1]))
            sigma = funcDep[:]
            sigma.remove(df)
            for sub_X in part:
                implicated = find_consequence(sub_X, sigma)
                if df[2] in implicated:
                    logical_cons.append(df)
                    break
        return logical_cons

    def find_super_key(self,table):
        return find_super_key(table, self.get_attributes(table), self.funcDep())

    def find_key(self,table):
        return find_key(table, self.get_attributes(table), self.funcDep())

    def is_BCNF(self,table):
        return is_BCNF(table, self.get_attributes(table), self.funcDep())

    def is_3NF(self,table):
        return is_3NF(table, self.get_attributes(table), self.funcDep())




