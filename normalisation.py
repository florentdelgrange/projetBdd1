from bdd import *

def not_involved(table, functional_dependencies, attributes):
    #Determine si des attributs ne sont jamais a droite d'une fleche
    attribute_list = attributes
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
    owned = attributes
    to_check = functional_dependencies
    while found:
        check = []
        found = False
        for df in to_check :
            list = split_str(df[1])
            if included_in(list, owned):
                found = True
                if df[2] not in owned:
                    owned.append(df[2])
            else :
                check.append(df)
        to_check = check
    if len(owned)>1:
        return owned[1:]


def complementary(list1, list2):
    complementary_list = []
    for i in list2:
        if i not in list1 :
            complementary_list.append(i)
    return complementary_list

print not_involved("t", [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")], ["A","B","C","D","E","F","G","H"])
print find_consequence(["B"], [("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")])