import os

Now=[]
List=os.listdir('.')
for File in List:
    if File[0]=='_' or File[-1]!='y':
        pass
    else:
        Now.append(File[:-3])
        print File[:-3]
FileHandle=open('__init__.py','w')
FileHandle.write('# -*- coding: UTF-8 -*-\n\n')
for Name in Now:
    FileHandle.write('from '+Name+' import *\n')
FileHandle.close()
