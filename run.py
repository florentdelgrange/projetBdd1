__author__ = 'Martin'

import sys
from bdd import *

def run(application):
    input = raw_input("SGBD>>")
    if input == 'exit':
        print("Good Bye")
        return False
    elif input == "help":
        showHelp()
        return True

    else:
        execute(application,input.split())
    return True

def showHelp():
        print(10*"#"+"List of commands"+10*"#"+"\n")
        print(3*" - "+"showTables : show the name of all the tables in the database")
        print(3*" - "+"showDep (nameTable)*: show all the functional dependencies (for nameTable)*")
        print(3*" - "+"addDep nameTable : add a functional dependence to nameTable")
        print(3*" - "+"delDep nameTable : delete a functional dependence to nameTable")
        print(3*" - "+"showAtt nameTable : show the name of all the attributes of nameTable")
        print(3*" - "+"showLogCons nameTable : show all the logical dependencies")
        print(3*" - "+"findSuperKey nameTable : find all the super keys of nameTable")
        print(3*" - "+"findKey nameTable : find the key of nameTable")
        print(3*" - "+"isBcnf nameTable : say if nameTable is in BCNF")
        print(3*" - "+"respect nameTable : say if all the functional dependence are respected")
        print(3*" - "+"is3nf nameTable : say if nameTable is in 3NF\n")


def execute(application,command):
    if 'showTables' in command:
        tableList = application.get_tables()
        for table in tableList:
            print (table)
    elif 'showDep' in command:
        depList = application.funcDep()
        if len(depList) <= 0:
            print("No dependencies")
        else:
            for dep in depList:
                if len(command) > 1:
                    if command[1] == dep[0]:
                        print (dep[0]+" "+dep[1]+" -> "+dep[2])
                else:
                    print (dep[0]+" | "+dep[1]+" -> "+dep[2])

    elif 'addDep' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            print("Dependence is like X -> A")
            x = raw_input("Enter X : ")
            a = raw_input("Enter A : ")
            application.add_dep((command[1],x,a,))
    elif 'showAtt' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            attList = application.get_attributes(command[1])
            for att in attList:
                print (att),
            print("\n")
    elif 'showLogCons' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else:
            number = 1
            while number > 0:
                depList = application.get_logical_consequence(command[1])
                if len(depList) <= 0:
                    print("No logical consequence ")
                    break
                else:
                    i=1
                    for dep in depList:
                        print (str(i)+" : "+dep[0]+" "+dep[1]+" -> "+dep[2])
                        i+=1
                    i=1
                    number = raw_input("If you want delete a dependence enter the correct number else enter 0")
                    if number == "0":
                        break
                    else:
                        for dep in depList:
                            if str(i) == number:
                                application.delete_dep(dep)
                                print("Consequence delete")
                            i+=1

    elif 'findSuperKey' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            superKeyList = application.find_super_key(command[1])
            for superKey in superKeyList:
                for att in superKey:
                    print(att),
                print("\n")
    elif 'findKey' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            keyList = application.find_key(command[1])
            for key in keyList:
                for att in key:
                    print(att),
                print("\n")
    elif 'isBcnf' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            print(application.is_BCNF(command[1]))
    elif 'is3nf' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            if(not application.is_3NF(command[1])):
                respect = application.respect(command[1])
                if len(respect) == 0:
                    print(application.is_3NF(command[1]))
                    input = raw_input("Do you want to make decomposition in 3NF (y/n) ")
                    if "y" in input or "Y" in input:
                        application.decompose(command[1])
                        print("Decomposition finished")

                else:
                    print("The functional dependencies are not respected")
            else:
                print(application.is_3NF(command[1]))

    elif 'respect' in command:
        if(len(command)) <= 1:
            print("Parameter is missing")
        else :
            respect = application.respect(command[1])
            if len(respect) == 0:
                print("All the dependencies are respected")
            else:
                print("Som dependence are not respected")
                i=1
                for triplet in respect:
                    print (str(i)+" : "+triplet[0]+" "+triplet[1]+" -> "+triplet[2])
                    i+=1
                number = raw_input("Do you want delete a functional dependence ? (Enter the a number or 0 to continue")
                while int(number) != 0:
                    application.delete_dep(respect[int(number)-1])

    else:
        print("Command not found")
        print("Type \'Help\' to know how use SGBD")



input = raw_input("Enter the name of the database that you want use : ")
application = Bdd(input)
while run(application):
    continue


