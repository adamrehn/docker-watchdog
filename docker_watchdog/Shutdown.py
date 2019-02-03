import os, platform, subprocess

class Shutdown(object):
	'''
	Provides cross-platform functionality to perform a shutdown of the host system
	'''
	
	@staticmethod
	def shutdown():
		'''
		Performs an immediate system shutdown
		'''
		
		# The platform-specific shutdown commands for our supported platforms
		commands = {
			'Darwin': ['/usr/bin/osascript', '-e', 'tell app "system events" to shut down'],
			'Linux': ['/sbin/shutdown', '-P', 'now'],
			'Windows': ['{}\\System32\\shutdown.exe'.format(os.environ.get('WINDIR', 'C:\\Windows')), '/s', '/t', '0']
		}
		
		# Run the shutdown command for the host platform
		command = commands[platform.system()]
		subprocess.run(command, check=True)
