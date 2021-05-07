import os
class MyPipe:
	def __init__(self , name):
		os.system('mkdir -p /tmp/MegaMind')
		self.path = '/tmp/MegaMind/' + name
	def make(self):	
		mode = 0o600
		os.mkfifo(self.path, mode)
	def write_to_pipe(self, data):	
		f = open(self.path , 'w')
		f.write(data)
		f.close()
		return
	
	def read_from_pipe(self):
		f = open( self.path, 'r')
		a = f.read()
		f.close()
		return a
	def wait_on_pipe(self):
		self.read_from_pipe()
		return
	def close(self):
		os.unlink(self.path)
		return		
	
