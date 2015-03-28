__author__ = 'Martin'

import sys
from bdd import *

def run(self,application):
    self.app = application
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


def execute(self,command):
    if 'showTables' in command:
        tableList = self.app.get_tables()
        for table in tableList:
            print table
    elif 'showDep' in command:
        depList = self.app.funcDep()
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
            self.app.add_dep((command[1],x,a,))
    elif 'showAtt' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            attList = self.app.get_attributes(command[1])
            for att in attList:
                print att
    elif 'showLogDep' in command:
        depList = self.app.get_logical_consequence()
        if len(depList) <= 0:
            print("No dependencies")
        else:
            for dep in depList:
                print dep
    elif 'findSuperKey' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            superKeyList = self.app.find_super_key(command[1])
            for superKey in superKeyList:
                print(superKey)

    elif 'findKey' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            keyList = self.app.find_key(command[1])
            for key in keyList:
                print(key)
    elif 'isBcnf' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            print(self.app.is_BCNF(command[1]))
    elif 'is3nf' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            print(self.app.is_3NF(command[1]))
    else:
        print("Command not found")
        print("Type \'Help\' to know how use SGBD")



input = raw_input("Enter the name of the database that you want use : ")
application = Bdd(input)
while run(application):
    continue


