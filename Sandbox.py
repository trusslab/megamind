import os
import time
class Sandbox_pool:
	def __init__(self , num):
		self.num_of_sandboxs = num
		self.sandboxs = []
		for i in range(0,self.num_of_sandboxs):
			s = Sandbox()
			self.sandboxs.append(s)
	def initialize(self):
		os.system('rm -rf /tmp/mysession')
		for i in range(0,self.num_of_sandboxs):
			self.sandboxs[i].initialize(i)
		return
	def destroy_all(self):
		for sb in self.sandboxs:
			sb.destroy()
	def get_idle_sandbox(self):
		for sb in self.sandboxs:
			if(sb.in_use == False):
				return sb
		
class Sandbox:
	def __init__(self):
		self.id = 0
		self.pid = 0
		#self.script_pid =0
		self.dir = ''
		self.basedir = '/tmp/mysession/'
		self.runtime = 'RunTime.py'
		self.initialized = False
		self.in_use = False
		return
	def initialize(self , myid):
		self.id = myid
		print('Initializing sand box with id = ' + str(myid) )
		self.dir = self.basedir + str(myid)
		os.system( 'mkdir -p ' + self.dir )
		os.system('cp ./run_time.py ' + self.dir)
		os.system('cp ./Commu.py ' + self.dir)
		os.system('cp ./ready.txt ' + self.dir)
		os.system('cp ./Session.py ' + self.dir)
		path = self.dir + '/in_use.txt' 
		mode = 0o600
		os.mkfifo( path , mode)
		path = self.dir + '/data.txt' 
		mode = 0o600
		os.mkfifo( path , mode)
	
		curr_dir_name = os.path.dirname(os.path.abspath(__file__))
		newpid = os.fork()
		if newpid == 0:
			#os.system('firejail --profile=profiles/'+ str(self.id) +'.profile python3.7 ~/run_time.py')
			#os._exit(os.EX_OK)
			cmdbin = '/usr/local/bin/firejail'
			arg1 = '--profile'
			arg1_1 = '='
			arg1_2 = curr_dir_name + '/profiles/' + str(self.id) + '.profile'
			arg2 = '/usr/bin/python3.7'
			arg3 = 'run_time.py'
			args = [cmdbin , arg1 + arg1_1 +arg1_2, arg2, arg3]
			print('\n\n\n\n',args,'\n\n\n\n')
			os.execv(cmdbin,args)
			return
		self.pid = newpid
		self.initialized = True
		self.in_use = False
		#self.update_inuse()
		#self.update_new_data(False)
		return
	def execute(self,script):
		os.system('cp ' + script + ' ' + self.dir + '/action.py')
		self.in_use = True
		self.update_inuse()
		return
#	def transfer_data(self , data):	
#		print( 'transfering data')
#		f = open( self.dir + '/data.txt', 'w+')
#		f.write( data)
#		f.close()
#		self.update_new_data(True)
#		return
	def transfer_data(self , data):	
		print( 'transfering data')
		self.send_over_named_pipe(data,'data.txt')
		return
		
#	def wait_for_response(self):
#		print( ' in wait for response:')	
#		f = open( self.dir + '/ready.txt', 'r')
#		lines = f.readlines()
#		line = lines[0]
#		while line == 'False':
#			f.seek(0,0)
#			lines = f.readlines()
#			if( len(lines) == 1):
#				line = lines[0]
#		f.close()
#		f = open( self.dir + '/ready.txt', 'w+')
#		print('()(() setting ready to False()()')
#		f.write('False')
#		f.close()
#		return
#		
#	def get_response(self):
#		print( ' in get response:')	
#		f = open( self.dir + '/response.txt', 'r')
#		lines = f.readlines()
#		line = lines[0]
#		f.close()
#		return line
	def get_response_blocking(self):
		a = self.recive_from_named_pipe('response.txt')
		return a;	
#	def update_new_data(self , new_data):
#		print( 'in update newdata= ' + str(new_data))
#		f = open( self.dir + '/new_data.txt', 'w+')
#		f.write( str(new_data))
#		f.close()
#		return
	def update_inuse(self):
		print( 'in update inuse  self.in_use = ' + str(self.in_use))
		#f = open( self.dir + '/in_use.txt', 'w+')
		#f.write( str(self.in_use))
		#f.close()
		self.send_over_named_pipe('True','in_use.txt')
		return
		
	def destroy(self):
		path = self.dir + '/in_use.txt' 
		os.unlink(path)
		path = self.dir + '/data.txt' 
		os.unlink(path)
		print(    "bash kill_tree.sh " + str(self.pid))
		os.system("bash kill_tree.sh " + str(self.pid))
		os.system("rm -r " + self.dir)
		self.initialized = False
		self.in_use = False
		return
	def destroy_and_replace(self):
		self.destroy()
		self.initialize(self.id)
	def send_over_named_pipe(self,data,name):
		path = self.dir + '/' + name 
		f = open(path , 'w')
		f.write(data)
		f.close()
		return
	def recive_from_named_pipe(self, name):
		path = self.dir + '/' + name
		f = open( path, 'r')
		a = f.read()
		f.close()
		return a
		

