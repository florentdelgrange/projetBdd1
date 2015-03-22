import sqlite3

class Bdd(object):
    def __init__(self, bdd_name):
        self.conn = sqlite3.connect(bdd_name+'.db')
        self.funcDep = []

    def funcDep(self):
        return self.funcDep

    def addDep(self, triplet):
        if(self.detection(triplet)):
            self.funcDep.append(triplet)

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
                    return False
        return True

    def get_logical_consequence(self):
        triplets = []
        sigma = self.funcDep()
        for i in range(len(sigma)):
            functional_dependence = sigma[i][1]
            implication = [sigma[i][2]]
            last_call = ''
            owned = split_str(sigma[i][1])+[sigma[i][2]]
            to_recheck = sigma
            added = True
            found = False
            while added:
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

