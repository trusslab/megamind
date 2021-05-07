import json
import os
import time

time_list = []
class Timer(object):
	def __init__(self, name=None):
		self.name = name
		time_list = []

	def __enter__(self):
		self.tstart = time.time()

	def __exit__(self, type, value, traceback):
		if self.name:
			print('[%s]' % self.name,)
		print('Elapsed: %s' % (time.time() - self.tstart))
		time_list.append(time.time() - self.tstart)

class Trigger:
	def __init__(self , file_name="",script=""):
		self.file_name = file_name
		self.script = script

def debug_log(*args, **kwargs):
	pass
class Items:
	def __init__(self, mydict = None):
		if(mydict is None):
			self.num_of_items = 0
			self.items = []
			self.last_item = None 
			self.dictionary = {}
		else:
			self.num_of_items = mydict.get('num_of_items')
			self.items = mydict.get('items')
			self.last_item = self.items[slef.num_of_items -1]
	def insert_new(self,new_str):
		self.items.append(new_str)
		self.last_item = new_str
		self.num_of_items += 1
	def get_dictionary(self):
		self.dictionary['num_of_items'] = self.num_of_items
		self.dictionary['items'] = self.items
		return self.dictionary
				
	
class Session:
	def __init__(self):
		self.requests = Items()
		self.responses = Items()
		self.speaker_id = "ND"
		self.skill_id = "ND"
		self.dictionary = {}
	def get_dictionary(self):
		self.dictionary['requests'] = self.requests.get_dictionary()
		self.dictionary['responses'] = self.responses.get_dictionary()
		self.dictionary['speaker_id'] = self.speaker_id
		self.dictionary['skill_id'] = self.skill_id
		return self.dictionary
	
def evaluate_filter(filter_dict ,my_session ):
	debug_log('\n---------------')
	debug_log('evaluating filter\n')
	debug_log(filter_dict)
	debug_log('\n')
	#debug_log(my_session.get_dictionary())
	last_req = my_session.requests.last_item 
	last_resp = my_session.responses.last_item
	debug_log('last request: ', last_req)
	debug_log('last response:', last_resp)
	keyword_evaluation = False
	include_or_evaluationn = False
	exclude_and_evaluation = True
	if 'keywords' in filter_dict:
		keywords = filter_dict.get('keywords')
		debug_log( 'these are keywords:')
		debug_log(keywords)
		if 'include_or' in keywords:
			include_or_evaluation = False
			debug_log('there is include or')
			include_or_items = keywords.get('include_or')
			for item in include_or_items:
				debug_log(item)
				if ((item in last_req) or (item in last_resp)):
					include_or_evaluationn= True 
					break
				
		if 'exclude_and' in keywords:
			exclude_and_evaluation = True
			debug_log('there is exclude and')
			exclude_and_items = keywords.get('exclude_and')
			for item in exclude_and_items:
				debug_log(item)
				if ( (item in last_resp) or (item in last_req)):
					exclude_and_evaluation = False
					break
		keyword_evaluation = include_or_evaluationn and exclude_and_evaluation
	
	if (keyword_evaluation == False):
		return False	
	return True	
def evaluate_trigger(name, my_session):
	try:
		myfile = open(name,'r')

	except:
		debug_log('error oppenning' + name)

#	try:
	mydict = json.load(myfile)
	debug_log(mydict)
	filters = mydict.get('filters')
	debug_log('\n\n')
	debug_log(filters)
	for fil in filters:
		if( evaluate_filter(fil, my_session)):
			return True
	
def trigger_functions(my_session, triggers):
	#for name in file_names:
	for trig in triggers:
		if(evaluate_trigger(trig.file_name,my_session)):
			print('we should execute',trig.script)
			os.system('rm -rf /tmp/mysession')
			os.system('mkdir -p /tmp/mysession/scripts')
			os.system('cp ./' + trig.script + ' /tmp/mysession/scripts')
			os.system('firejail --profile=myprof.profile python3.7 ~/' + trig.script)
	#	except:
	#		debug_log('error in parsing')

def main():
	file1 = open( './JSONs/session.json' , 'r')
	#session_dict = json.load(file1)
	my_session = Session()
	my_session.requests.insert_new('Open Uber')
	my_session.responses.insert_new('Hello this is uber')
	my_session.requests.insert_new('Get me a cab to airport')
	my_session.responses.insert_new('For when')
	my_session.requests.insert_new('For now buy a taxi')
	my_session.speaker_id = 'Javad'
	my_session.skill_id = 'Uber'
	debug_log(my_session.get_dictionary())

	triggers = []
	triggers.append(Trigger('./JSONs/parental.json','scripts/parental.py'))
	for i in range(1,10):
		with Timer('time it'):
			trigger_functions(my_session , triggers)
	print('The average execution time is: ', sum(time_list)/len(time_list) )
			

if __name__ == '__main__':
	main()
