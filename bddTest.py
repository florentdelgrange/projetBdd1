__author__ = 'Delgrange Florent'

from bdd import *

data_base = Bdd('exams_bdd')
print (data_base.get_tables())
data_base.add_dep(("exam2012", "A B","C"))
data_base.add_dep(("exam2012","A B","D"))
data_base.add_dep(("exam2012", "G", "E"))
data_base.add_dep(("exam2012", "E F", "G"))
data_base.add_dep(("exam2012", "E F", "H"))
data_base.add_dep(("exam2012", "B C D", "A"))
data_base.add_dep(("exam2012", "B", "F"))
data_base.add_dep(("exam2012", "F", "A"))
data_base.add_dep(('exam2013', 'C D', 'B'))
data_base.add_dep(('exam2013','A','E'))
data_base.add_dep(('exam2013', 'E F', 'A'))
data_base.add_dep(('exam2013', 'C','D'))
data_base.add_dep(('exam2013', 'A B E', 'F'))
data_base.add_dep(('exam2013', 'A B E', 'C'))
data_base.add_dep(('exam2013', 'A B', 'C'))
data_base.add_dep(('exam2013', 'A E', 'F'))
print (data_base.get_attributes("exam2012"))
print (data_base.funcDep())
print (data_base.find_super_key('exam2012'))
print (data_base.find_key('exam2012'))
print (data_base.find_key('exam2013'))
print (data_base.is_3NF('exam2012'))
print (data_base.is_BCNF('exam2013'))
while data_base.run():
    continue

