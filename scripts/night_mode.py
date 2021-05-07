import os
from Commu import Commu
import json

def pr(*args , **kwargs):
	print( '**** ' + " ".join(map(str,args)) + " ****" , **kwargs)

pr("night mode extention")
comm = Commu()
comm.init_pipes()
#comm.update_ready(False)
while True:
	#comm.wait_for_new_data()
	#session = comm.read_data()
	session = comm.read_data_blocking()
	#pr(session)
	#item = comm.get_item_of_interest(session)
	comm.write_response('stop')
	#comm.update_ready(True)

	
