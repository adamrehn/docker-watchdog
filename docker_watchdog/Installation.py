from .ConfigurationManager import ConfigurationManager
import os, platform, requests, subprocess, sys
from .Utility import Utility

class Installation(object):
	'''
	Provides cross-platform functionality for installing the watchdog as a service that runs at startup
	'''
	
	@staticmethod
	def install():
		'''
		Installs the watchdog service
		'''
		
		# Generate the command to run the watchdog
		command = [sys.executable, '-m', 'docker_watchdog']
		
		# Perform installation using the most appropriate method for the host platform
		if platform.system() == 'Windows':
			
			# Under Windows, use WinSW to create the service
			try:
				
				# Compute the paths for storing our service wrapper files
				serviceDir = os.path.join(ConfigurationManager.getConfigDirectory(), 'service')
				serviceExe = os.path.join(serviceDir, 'DockerWatchdogService.exe')
				serviceXml = os.path.join(serviceDir, 'DockerWatchdogService.xml')
				
				# Ensure the service wrapper directory exists and is empty
				Utility.unlink(serviceDir)
				os.makedirs(serviceDir)
				
				# Download the WinSW executable
				response = requests.get('https://github.com/kohsuke/winsw/releases/download/winsw-v2.2.0/WinSW.NET4.exe')
				Utility.writeFile(serviceExe, response.content)
				
				# Generate our service wrapper configuration XML
				serviceName = 'docker-watchdog'
				Utility.writeFile(serviceXml, '<service><id>{}</id><name>{}</name><description>{}</description><executable>{}</executable><arguments>{}</arguments></service>'.format(
					serviceName,
					'Docker Idle Watchdog',
					'docker-watchdog startup service',
					command[0],
					' '.join(command[1:])
				))
				
				# Un-register the service if it already exists, otherwise registration will fail
				subprocess.run([serviceExe, 'uninstall'], check=False)
				
				# Register the service
				subprocess.run([serviceExe, 'install'], check=True)
				
			except Exception as err:
				
				# Propagate any exception details without the backtrace
				Installation._propagateError(err,
					'Could not install the service. ' +
					'Ensure you have sufficient privileges for creating Windows services.'
				)
			
		else:
			
			# Under macOS and Linux, use pleaserun to generate and install the startup script
			try:
				subprocess.run([
					'pleaserun', '--install', '--overwrite',
					'--name', 'docker-watchdog',
					'--description', 'docker-watchdog startup service'
				] + command, check=True)
			except Exception as err:
				
				# Propagate any exception details without the backtrace
				Installation._propagateError(err,
					'Could not install the service. ' +
					'Ensure pleaserun is installed and you have sufficient privileges for creating startup scripts.'
				)
	
	
	# "Private" methods
	
	@staticmethod
	def _propagateError(error, message):
		raise RuntimeError('{}\n\nError details:\n{}: {}'.format(message, type(error).__name__, str(error)))
