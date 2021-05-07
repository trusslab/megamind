import json
import os
class Commu:
	def __init__(self):
		self.first = 1
		return
	def init_pipes(self):
		if(self.first == 1):	
			path = 'response.txt' 
			mode = 0o600
			os.mkfifo( path , mode)
			self.first = 0
#	def update_new_data(self, b):
#		f = open ('new_data.txt' , 'w+')
#		f.write(str(b))
#		f.close()
#		return
#	def update_ready(self,b):
#		f = open( 'ready.txt' , 'w+')
#		print('setting ready to ' + str(b))
#		f.write(str(b))
#		f.close()
#		return
#	def wait_for_new_data(self):
#		f = open ('new_data.txt' , 'r')
#		lines = f.readlines()
#		line = lines[0]
#		while line == 'False':
#			f.seek(0,0)
#			lines = f.readlines()
#			if (len(lines) == 1):
#				line = lines[0]
#			#sleep(1)
#			#print('.')
#			#print(line)
#		self.update_new_data(False)
#		f.close()
#		return
#	def read_data(self):
#		f = open( 'data.txt')
#		return json.load(f)
	def read_data_blocking(self):
		a = self.recive_from_named_pipe('data.txt')
		return json.loads(a)

#	def write_response(self,item):
#		f = open( 'response.txt' ,'w+')
#		f.write(item)
#		f.close()
#		return

	def write_response(self,item):
		self.send_over_named_pipe(item,'response.txt')
		return
	def get_item_of_interest(self,session):
		req_res = session['req_resp']
		if (req_res == 'req'):
			req_dict = session['requests']
			num = req_dict['num_of_items']
			if (num >0):
				items = req_dict['items']
				last_item = items[num-1]
				return last_item
			return ""
		else:
			resp_dict = session['responses']
			num = resp_dict['num_of_items']
			if (num >0):
				items = resp_dict['items']
				last_item = items[num-1]
				return last_item
			return ""
	def is_request(self, session):
		req_res = session['req_resp']
		if (req_res == 'req'):
			return True
		else:
			return False
		
	def get_num_of_requests(self,session):
		req_res = session['req_resp']
		if (req_res == 'req'):
			req_dict = session['requests']
			num = req_dict['num_of_items']
			return num

	def get_num_of_responses(self,session):
		req_res = session['req_resp']
		if (req_res == 'resp'):
			resp_dict = session['responses']
			num = resp_dict['num_of_items']
			return num
	def send_over_named_pipe(self,data,name):
		path =  name 
		f = open(path , 'w')
		f.write(data)
		f.close()
		return
	def recive_from_named_pipe(self, name):
		path =  name
		f = open( path, 'r')
		a = f.read()
		f.close()
		return a
		

