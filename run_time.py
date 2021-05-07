import os
from time import sleep
from Commu import Commu

comm =  Commu()

print('MegaMind extention runtime')


a = comm.recive_from_named_pipe('in_use.txt')
print(a)


#os.system('/bin/python3.7 action.py')
pybin = '/bin/python3.7'
arg1 = 'action.py'
args = [pybin , arg1]
os.execv(pybin , args )
