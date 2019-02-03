import os, shutil

class Utility(object):
	'''
	Provides utility functionality
	'''
	
	@staticmethod
	def unlink(path):
		'''
		Removes the specified file or directory if it exists
		'''
		if os.path.exists(path):
			if os.path.isdir(path):
				shutil.rmtree(path)
			else:
				os.unlink(path)
	
	@staticmethod
	def writeFile(filename, data):
		'''
		Writes data to a file
		'''
		with open(filename, 'wb') as f:
			if isinstance(data, str):
				f.write(data.encode('utf-8'))
			else:
				f.write(data)
