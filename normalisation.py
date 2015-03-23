from bdd import *

def not_involved(table, functional_dependencies, attributes):
    #Determine si des attributs ne sont jamais a droite d'une fleche
    isolated_attributes = []
    sigma = functional_dependencies
    for df in sigma :
        if df[0] == table and df[2] not in isolated_attributes :
            isolated_attributes.append(df[2])
    isolated_attributes = complementary(isolated_attributes, attributes)
    return isolated_attributes

def find_consequence(attributes,functional_dependencies):
    #retourne l'ensemble d'attributs A implique par l'ensemble d'attribut X tq
    #sigma satisfait X->A
    found = True
    owned = attributes[:]
    to_check = functional_dependencies[:]
    while found:
        check = []
        found = False
        for df in to_check :
            X = split_str(df[1])
            if included_in(X, owned):
                found = True
                if df[2] not in owned:
                    owned.append(df[2])
            else:
                check.append(df)
        to_check = check
    if len(owned)>len(attributes):
        return owned[len(attributes):]
    else:
        return []

def find_key(table, functional_dependencies, attributes):
    isolated_attributes = not_involved(table,functional_dependencies,attributes)
    rest = []
    for i in complementary(find_consequence(isolated_attributes, functional_dependencies), attributes):
        rest.append([i])
    if len(rest)-len(isolated_attributes) == 0:
        return [isolated_attributes]
    else:
        key = []
        prohibited_list = isolated_attributes[:]
        found = True
        iterations = 0
        while found or iterations < 2:
            iterations += 1
            #print "prohibited list : ",
            #print prohibited_list
            #print "rest : ",
            #print rest
            found = False
            for attribute_list in rest:
                boolean = True
                for i in attribute_list:
                    if i in prohibited_list:
                        #print i + " is in prohibited list, so rest = ",
                        boolean = False
                        rest.remove(attribute_list)
                        #print rest
                        break
                if boolean:
                    x = isolated_attributes[:]
                    for i in attribute_list:
                        x.append(i)
                    if included_in(attributes, find_consequence(x, functional_dependencies)+x):
                        found = True
                        iterations = 0
                        #print "key found :",
                        #print x,
                        #print " -> ",
                        #print find_consequence(x, functional_dependencies)
                        key.append(x)
                        prohibited_list = union(prohibited_list,x)
            if not found:
                rest = part(rest)
                #print "nothing found... new rest : ",
                #print rest
        return key

def comb(list, order):
    if len(list) < order :
        return []
    elif order == 1:
        new_list = []
        for elt in list:
            new_list.append([elt])
        return new_list
    else:
        new_list = []
        for i in range(1,order):
            for j in range(len(list)):
                if j < len(list):
                    sub_list = list[:j]+list[j+1:]
                else:
                    sub_list = list[:j]
                for elt in comb(sub_list, i):
                    new_list.append([list[j]]+elt)
        return new_list

def part(list):
    over_list = comb(list, len(list))
    sub_list = []
    for i in over_list :
        boolean = True
        for j in sub_list :
            if equals(i,j):
                boolean = False
                break
        if boolean :
            sub_list.append(i)
    return comb(list,1) + sub_list

def equals(list1,list2):
    if len(list1) == len(list2):
        counter = 0
        for i in list1:
            for j in list2:
                if i == j:
                    counter += 1
        if counter == len(list1):
            return True
    return False

def union(list1,list2):
    list = list1[:]
    for i in list2:
        if i not in list:
            list.append(i)
    return list

def complementary(list1, list2):
    complementary_list = []
    for i in list2:
        if i not in list1:
            complementary_list.append(i)
    return complementary_list

print not_involved("t", [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")], ["A","B","C","D","E","F","G","H"])
print find_consequence(["B"], [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")])
print part(['A','B','C','D'])