import os
from Commu import Commu
import json

def pr(*args , **kwargs):
	print( '**** ' + " ".join(map(str,args)) + " ****" , **kwargs)
family_names = ['alex','steve','julia']
pr("redacting extention")
comm = Commu()
comm.init_pipes()
#comm.update_ready(False)
while True:
	#comm.wait_for_new_data()
	#session = comm.read_data()
	session = comm.read_data_blocking()
	#pr(session)
	item = comm.get_item_of_interest(session)
	print(item)
	item = item.replace('f\'uck','bleep')
	for name in family_names:
		item = item.replace(name,'R_FIRST_NAME')
	comm.write_response(item)
	#comm.update_ready(True)

	
