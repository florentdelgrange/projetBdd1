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

print not_involved("t", [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")], ["A","B","C","D","E","F","G","H"])
print find_consequence(["B"], [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")])
print find_super_key("t", ["A","B","C","D","E","F","G","H"], [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")])
print find_key("t", ["A","B","C","D","E","F","G","H"], [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")])
print find_key('t', ['A','B','C', 'D', 'E', 'F'], [('t', 'C D', 'B'), ('t','A','E'), ('t', 'E F', 'A'), ('t', 'C','D'), ('t', 'A B E', 'F'), ('t', 'A B E', 'C'), ('t', 'A B', 'C'), ('t', 'A E', 'F')])
print find_key('t',['A','B','C', 'D', 'E', 'F'], [('t',' A B C D E F', 'D'), ('t', 'A C', 'E'), ('t','A B D', 'C'), ('t', 'E B', 'F'), ('t', 'E F', 'A'), ('t', 'E F', 'B'), ('t', 'E F', 'C'), ('t', 'A F', 'B'), ('t', 'A F', 'C')])
print is_3NF('t',['A','B','C', 'D', 'E', 'F'], [('t',' A B C D E F', 'D'), ('t', 'A C', 'E'), ('t','A B D', 'C'), ('t', 'E B', 'F'), ('t', 'E F', 'A'), ('t', 'E F', 'B'), ('t', 'E F', 'C'), ('t', 'A F', 'B'), ('t', 'A F', 'C')])
print is_3NF("t", ["A","B","C","D","E","F","G","H"], [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")])
print is_3NF('t', ['A','B','C', 'D', 'E', 'F'], [('t', 'C D', 'B'), ('t','A','E'), ('t', 'E F', 'A'), ('t', 'C','D'), ('t', 'A B E', 'F'), ('t', 'A B E', 'C'), ('t', 'A B', 'C'), ('t', 'A E', 'F')])


