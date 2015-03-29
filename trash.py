from normalisation import *
from bdd import *

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

def get_logical_consequence(func_dep):
        triplets = []
        sigma = func_dep
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
                if found :#and not is_useless(sigma, (sigma[i][0], functional_dependence, attribute) ):
                    triplets.append((sigma[i][0], functional_dependence, attribute))
        return triplets

print get_logical_consequence([('myTable', 'C E', 'A'),('myTable', 'C', 'D'),('myTable', 'A', 'B'),('myTable', 'D', 'B'),('myTable', 'D', 'E'),('myTable', 'B', 'F'),('myTable', 'A D', 'C')])
