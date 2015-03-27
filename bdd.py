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

    def run(self):
        input = raw_input("SGBD>>")
        if input == 'exit':
            print("Good Bye")
            return False
        elif input == "help":
            self.showHelp()
            return True

        else:
            self.execute(input.split())
        return True

    def execute(self,command):
        if 'showTables' in command:
            tableList = self.get_tables()
            for table in tableList:
                print table
        elif 'showDep' in command:
            depList = self.funcDep()
            if len(depList) <= 0:
                print("No dependencies")
            else:
                for dep in depList:
                    print dep
        elif 'addDep' in command:
            if(len(command)) <= 1:
                print("Parameter is missing")
            else :
                print("Dependence is like X -> A")
                x = raw_input("Enter X : ")
                a = raw_input("Enter A : ")
                self.add_dep((command[1],x,a,))
        elif 'showAtt' in command:
            if(len(command)) <= 1:
                print("Parameter is missing")
            else :
                attList = self.get_attributes(command[1])
                for att in attList:
                    print att
        elif 'showLogDep' in command:
            depList = self.get_logical_consequence()
            if len(depList) <= 0:
                print("No dependencies")
            else:
                for dep in depList:
                    print dep
        elif 'findSuperKey' in command:
            if(len(command)) <= 1:
                print("Parameter is missing")
            else :
                superKeyList = self.find_super_key(command[1])
                for superKey in superKeyList:
                    print(superKey)

        elif 'findKey' in command:
            if(len(command)) <= 1:
                print("Parameter is missing")
            else :
                keyList = self.find_key(command[1])
                for key in keyList:
                    print(key)
        elif 'isBcnf' in command:
            if(len(command)) <= 1:
                print("Parameter is missing")
            else :
                print(self.is_BCNF(command[1]))
        elif 'is3nf' in command:
            if(len(command)) <= 1:
                print("Parameter is missing")
            else :
                print(self.is_3NF(command[1]))
        else:
            print("Command not found")
            print("Type \'Help\' to know how use SGBD")

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

    def is_useless(self,triplet):
        for df in self.funcDep():
            if triplet[0] == df[0] and triplet[2] == df[2] and equals(split_str(df[1]),split_str(triplet[1])):
                print "this functional dependence (" + df[1] + " -> " + df[2] + ") is already in the table"
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

    def showHelp(self):
        print(10*"#"+"List of commands"+10*"#"+"\n")
        print(3*"- "+"showTables : show the name of all the tables in the database")
        print(3*"- "+"showDep : show all the functional dependencies")
        print(3*"- "+"addDep nameTable : add a functional dependence to nameTable")
        print(3*"- "+"showAtt nameTable : show the name of all the attributes of nameTable")
        print(3*"- "+"showLogDep : show all the logical dependencies")
        print(3*"- "+"findSuperKey nameTable : find all the super keys of nameTable")
        print(3*"- "+"findKey nameTable : find the key of nameTable")
        print(3*"- "+"isBcnf nameTable : say if nameTable is in BCNF")
        print(3*"- "+"is3nf nameTable : say if nameTable is in 3NF\n")


