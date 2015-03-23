import sqlite3

class Bdd(object):
    def __init__(self, bdd_name):
        self.conn = sqlite3.connect(bdd_name+'.db')
	cur = conn.cursor()
	with cur:
		triplet_list = []
		table_list = []
		for table in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
			table_list.append(table[0])
	if "FuncDep" not in table_list:
		cur.execute("CREATE TABLE FunctDep (table TEXT, X TEXT, A TEXT )")
		self.conn.commit()
		cur.close
		self.conn.close()
	
    def funcDep(self):
        self.conn = sqlite3.connect(bdd_name+'.db')
	cur = conn.cursor()
	with cur:
		cur.execute("SELECT * FROM FuncDep")
		for l in cur:
			self.funcDep.append(l)
	return self.funcDep

    def add_dep(self, triplet):
        if(self.detection(triplet)):
            self.funcDep.append(triplet)
        	self.conn = sqlite3.connect(bdd_name+'.db')
		cur = conn.cursor()
		cur.execute("INSERT INTO FuncDep(table,X,A) VALUES("+triplet[0]+","+triplet[1]+","+triplet[2]+")")
		self.conn.commit()

    def get_attributes(self,table):
        cur = self.conn.cursor()
        list=[]
        with cur:
            for raw in cur.execute("PRAGMA table_info("+table+")"):
                list.append(raw[1])
        self.conn.close()
        return list

    def detection(self, triplet):
        cur = self.conn.cursor()
        with cur:
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
                    self.conn.close()
                    return False
        self.conn.close()
        return True

    def get_logical_consequence(self):
        triplets = []
        sigma = self.funcDep()
        for i in range(len(sigma)):
            functional_dependence = sigma[i][1]
            #Pourquoi implication est une liste ? Cas ou la consequence logique implique 2 attributs ou plus ; c'est la raison de la presence de la variable "last_call"
            implication = [sigma[i][2]]
            last_call = ''
            owned = split_str(sigma[i][1])+[sigma[i][2]]
            to_recheck = sigma
            added = True
            found = False
            while added: #tant qu'une df a ete ajoutee a l'etape precendente
                added = False
                checklist = []
                for j in range(len(to_recheck)):
                    if to_recheck[j][0] == sigma[i][0]:
                        list = split_str(to_recheck[j][1])
                        if not included_in(list,owned):
                            checklist.append(to_recheck[j])
                        else:
                            if to_recheck[j][2] not in owned:
                                if to_recheck[j][1] == last_call:
                                    implication.append(to_recheck[j][2])
                                else:
                                    implication = [to_recheck[j][2]]
                                owned.append(to_recheck[j][2])
                                found = True
                                last_call = to_recheck[j][1]
                            for k in list:
                                if k not in owned:
                                    owned.append(k)
                            added = True
                            if j+1 < len(to_recheck):
                                checklist += to_recheck[j+1:]
                            to_recheck=checklist
                            break
            for attribute in implication :
                if found and not self.is_useless(sigma,(sigma[i][0], functional_dependence, attribute)):
                    triplets.append((sigma[i][0], functional_dependence, attribute))
        return triplets

    def is_useless(self,triplet):
        for df in self.funcDep():
            if triplet[0] == df[0] and triplet[2] == df[2] and included_in(split_str(df[1]),split_str(triplet[1])):
                return True
        return False

def included_in(list1,list2):
    for i in list1:
        if i not in list2:
            return False
    return True

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

