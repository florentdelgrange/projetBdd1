from bdd import *

#Determine si des attributs ne sont jamais a droite d'une fleche
def not_involved(table, functional_dependencies, attributes):
    isolated_attributes = []
    sigma = functional_dependencies
    for df in sigma :
        if df[0] == table and df[2] not in isolated_attributes :
            isolated_attributes.append(df[2])
    isolated_attributes = complementary(isolated_attributes, attributes)
    return isolated_attributes

#retourne l'ensemble d'attributs A implique par l'ensemble d'attribut X tq
#sigma satisfait X->A
def find_consequence(attributes,functional_dependencies):
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

#trouve toutes les super cles de la table entree en parametre
def find_super_key(table, attributes, functional_dependencies):
    super_key = []
    combinations = partiesliste(attributes)
    sigma = []
    for triplet in functional_dependencies:
        if triplet[0] == table:
            sigma.append(triplet)
    for comb in combinations:
        if equals(attributes,find_consequence(comb,sigma)+comb):
            super_key.append(comb)
    return filter(super_key)

#trouve toutes les cles de la table entree en parametre
def find_key(table, attributes, functional_dependencies):
    keys = []
    super_keys_list = find_super_key(table, attributes, functional_dependencies)
    for super_key in super_keys_list:
        boolean = True
        for test_key in super_keys_list:
            if super_key != test_key and included_in(test_key, super_key):
                boolean = False
                break
        if(boolean):
            keys.append(super_key)
    return keys

def is_BCNF(table, attributes, functional_dependencies):
    sigma = []
    for triplet in functional_dependencies:
        if triplet[0] == table:
            sigma.append(triplet)
    for df in sigma:
        if not equals(attributes, find_consequence(split_str(df[1]),sigma)+split_str(df[1])):
            print attributes, " != ", find_consequence(split_str(df[1]),sigma)+split_str(df[1])
            return False
    return True


def is_3NF(table, attributes, functional_dependencies):
    sigma = []
    for triplet in functional_dependencies:
        if triplet[0] == table:
            sigma.append(triplet)
    key_list = find_key(table, attributes,functional_dependencies)
    in_key = set([])
    for key in key_list:
        in_key = set(key) | in_key
    if in_key == set(attributes):
        return True
    else:
        for df in sigma:
            if df[2] not in in_key:
                if not equals(attributes, find_consequence(split_str(df[1]),sigma)+split_str(df[1])):
                    return False
        return True

#retourne l'ensemble minimal X -> A
def minimal_dependence(triplet, functional_dependencies):
    #remarque : function_dependencies correpond a l'esemble des DF d'une table en particulier
    X = split_str(triplet[1])
    parties = partiesliste(X)
    X_mini = X
    for sub_X in parties:
        if triplet[2] in find_consequence(sub_X,functional_dependencies):
            if len(sub_X) < len(X_mini):
                X_mini = sub_X
    return (triplet[0], unsplit_str(X_mini), triplet[2])

#http://python.jpvweb.com/mesrecettespython/doku.php?id=parties_ensemble
def partiesliste(seq):
    p = []
    i, imax = 0, 2**len(seq)-1
    while i <= imax:
        s = []
        j, jmax = 0, len(seq)-1
        while j <= jmax:
            if (i>>j)&1 == 1:
                s.append(seq[j])
            j += 1
        p.append(s)
        i += 1
    return filter(p)

#supprime les doublons
def filter(list):
    sub_list = []
    for i in list:
        boolean = True
        for j in sub_list :
            if equals(i,j):
                boolean = False
                break
        if boolean :
            sub_list.append(i)
    return sub_list

def equals(list1,list2):
    return set(list1) == set(list2)

def union(list1,list2):
    return list(set(list1) | set(list2))

def complementary(list1, list2):
    complementary_list = []
    for i in list2:
        if i not in list1:
            complementary_list.append(i)
    return complementary_list

def included_in(list1,list2):
    if len(list1) <= len(list2):
        for i in list1:
            if i not in list2:
                return False
        return True
    else:
        return False

def get_minimal_funcDep(functional_dependencies):
    new_functional_dependencies =[]
    for df in functional_dependencies:
        minimal = minimal_dependence(df,functional_dependencies)
        new_functional_dependencies.append(minimal)
    return new_functional_dependencies

#renvoie la liste correspondant a une chaine de caractere (les espaces sont ignores)
def split_str(str):
    return str.split(' ')

def unsplit_str(list):
    str = ''
    for i in list:
        str += i
        str += ' '
    return str[:len(str)-1]


def merge(list,newList):
    placed = True
    for dep in list:
        if len(newList) <= 0:
            newList.append([dep])
        else:
            for l in newList:
                for dep2 in l:
                    if(not(included_in(split_str(dep[1]+dep[2]),split_str(dep2[1]+dep2[2])) and included_in(split_str(dep2[1]+dep2[2]),split_str(dep[1]+dep[2])))):
                        placed = False
                        break
                if(placed):
                    l.append(dep)
            if(not placed):
                newList.append([dep])
    return newList

def merge2(functional_dependencies):
    new_list = []
    for df in functional_dependencies:
        if len(new_list) == 0:
            new_list.append([df])
        else:
            for list in new_list:
                if included_in(split_str(df[1]+' '+df[2]), split_str(list[0][1] + ' ' + list[0][2])) or included_in(split_str(list[0][1] + ' ' + list[0][2]), split_str(df[1]+' '+df[2])):
                    list.append(df)
                else:
                    new_list.append([df])
    return new_list
