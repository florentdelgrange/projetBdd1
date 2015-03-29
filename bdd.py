import sqlite3 as lite
import sys

from normalisation import *

class Bdd(object):

    def __init__(self, bdd_name):
        '''
        Initialise the object Bdd. The object connects to the bdd entered in parameter.
        Create the table "FuncDep" that contains the functional dependencies too.
        :param bdd_name: enter here the name of the bdd (without *.db)
        :return: None
        '''

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
        '''
        returns the tables list of this database
        :return: the list of tables name (str)
        '''
        table_list = []
        with self.conn:
            cur = self.conn.cursor()
            for table in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
                table_list.append(table[0])
        cur.close()
        return table_list

    def funcDep(self):
        '''
        return the list of the functional dependencies of all the tables
        :return: a list of triplet
        '''
        funcDep = []
        with self.conn:
            cur = self.conn.cursor()
            for l in cur.execute("SELECT * FROM FuncDep"):
                funcDep.append(l)
        cur.close()
        return funcDep

    def get_table_funcDep(self,table):
        '''
        return the list of the functional dependencies of the table entered in parameter
        :param table: the table name (str)
        :return: the triplet list of functional dependencies of the table
        '''
        funcDep = []
        with self.conn:
            cur = self.conn.cursor()
            for l in cur.execute("SELECT * FROM FuncDep"):
                if l[0] == table:
                    funcDep.append(l)
        cur.close()
        return funcDep

    def add_dep(self, triplet):
        '''
        Add a functional dependence (triplet) to the table FuncDep.
        If the triplet entered is not valid, it is not added to the FuncDep table
        :param triplet: the functional dependence to add to the FuncDep table
        :return: /
        '''
        if(self.detection(triplet)):
            with self.conn:
                cur = self.conn.cursor()
                cur.execute("INSERT INTO FuncDep VALUES (?, ?, ?)", triplet)
                cur.close()
            self.conn.commit()

    def delete_dep(self, triplet):
        '''
        Delete the functional dependence triplet of the table FuncDep table if it is possible (eg not possible if the triplet is not in the table).
        :param triplet: the triplet to remove from the table FuncDep
        :return: True if it is possible, False else.
        '''
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
        '''
        Return the triplets of functional dependencies that are not respected in the table entered in parameter
        :param table: the table to test the respect
        :return: the list of triplet that are not respected
        '''
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
        '''
        Say if the functional dependence triplet entered in parameter is useless to add to the FuncDep table.
        :param triplet: the triplet to test
        :return: True if the triplet is useless, False else.
        '''
        for df in self.funcDep():
            if triplet[0] == df[0] and triplet[2] == df[2] and equals(split_str(df[1]),split_str(triplet[1])):
                return True
        return False

    def get_logical_consequence(self, table):
        '''
        Return the list of triplet that is a logical consequence in FuncDep
        :param table: the table to test it
        :return: the list of logical consequence
        '''
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
        '''
        return the list of super_key of the table entered in parameter
        :param table: the table to test it
        :return: the list of list ofattributes that are the super_key
        '''
        return find_super_key(table, self.get_attributes(table), self.funcDep())

    def find_key(self,table):
        '''
        return the list of key of the list entered in parameter
        :param table: the table to test
        :return: the list of list of attributes that are the key
        '''
        return find_key(table, self.get_attributes(table), self.funcDep())

    def is_BCNF(self,table):
        return is_BCNF(table, self.get_attributes(table), self.funcDep())

    def is_3NF(self,table):
        return is_3NF(table, self.get_attributes(table), self.funcDep())

    def decompose(self,table):
        """
        Generate a 3NF decomposition in a new database
        :param table:
        :return:
        """
        if len(self.respect(table)) <= 0 :
            cons = self.get_logical_consequence(table)
            while len(cons) > 0:
                self.delete_dep(cons[0])
                cons = self.get_logical_consequence(table)
            minimal = get_minimal_funcDep(self.get_table_funcDep(table))
            minimal = merge(minimal,[])
            print(minimal)
            conn = lite.connect(minimal[0][0]+"decomposition.db")
            cur = self.conn.cursor()
            cur.execute("CREATE TABLE FuncDep(name TEXT, X TEXT, A TEXT )")
            i = 1
            for listDep in minimal:
                for dep in listDep:
                    triplet = (dep[0]+i,dep[1],dep[2])
                    cur.execute("INSERT INTO FuncDep VALUES (?, ?, ?)", triplet)
                i+=1
            conn.commit()
            cur.close()
            conn.close()
        else:
            print("The table don't respect de functional dependencies")






