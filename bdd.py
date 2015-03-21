import sqlite3

class Bdd(object):
    def __init__(self, bdd_name):
        self.conn = sqlite3.connect(bdd_name+'.db')
        self.funcDep = []

    def addDep(self, triplet):
        self.funcDep.append(triplet)

    def detection(self,triplet):
        cur = self.conn.cursor()
        #Test n1 : est-ce que la table (triplet[0]) existe ?
        boolean = False
        for raw in cur.execute("select name from sqlite_master where type = 'table'"):
            if(raw[0]==triplet[0]):
                boolean=True
                break
        if boolean==False :
            return boolean

        #Test n2 : est-ce que les attributs sont bien tous dans cette table ?
        list = split_str(triplet[1])
        list.append(triplet[2])
        for raw in cur.execute("PRAGMA table_info("+triplet[0]+")"):
            if raw[1] not in list :
                return False;
        





def split_str(str):
    list=[]
    word = ''
    for i in range(len(str)):
        if i==len(str)-1 or str[i] == ' ':
            if i==len(str)-1:
                word+=str[i]
            list.append(word)
            word=''
        else:
            word+=str[i]
    return list

