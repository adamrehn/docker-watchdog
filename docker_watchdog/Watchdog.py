from .Shutdown import Shutdown
import docker, time, uptime

class Watchdog(object):
	'''
	Provides inactivity monitoring and automatic shutdown functionality
	'''
	
	def __init__(self, sleep, timeout, billing, percentage):
		'''
		Creates a new watchdog instance.
		
		`sleep` specifies the interval (in seconds) to sleep for between sampling runs.
		
		`timeout` specifies the period of inactivity (in seconds) required to consider the system idle.
		
		`billing` specifies the billing granularity (in seconds) if the host is a cloud VM, or zero otherwise.
		
		`percentage` specifies the minimum percentage (0.0 to 1.0) of the current billing unit that must have
		elapsed to consider a shutdown to be cost-effective.
		'''
		
		# Store our configuration settings
		self._sleep = sleep
		self._timeout = timeout
		self._billing = billing
		self._percentage = percentage
		
		# Keep track of our connection to the Docker daemon
		self._docker = None
		
		# Keep track of the number of seconds the system has been running for
		self._uptime = 0
		
		# Keep track of the number of seconds the system has been idle for
		self._idleCount = 0
	
	def start(self):
		'''
		Starts the watchdog. This method will not return until the watchdog terminates.
		'''
		while True:
			
			# If we have not yet connected to the Docker daemon, attempt to do so
			# (If the Docker daemon has not started yet, we simply continue waiting)
			if self._docker is None:
				try:
					self._docker = docker.client.from_env()
				except:
					pass
			
			# If we have a connection then perform a sampling run
			if self._docker is not None:
				
				# Sample the system uptime and determine how long we last slept for
				lastUptime = self._uptime
				self._uptime = uptime.uptime()
				lastSleep = self._uptime - lastUptime if lastUptime > 0 else 0
				
				# Determine if there is at least one running container and update our idle count
				active = len(self._docker.containers.list()) > 0
				self._idleCount = 0 if active == True else self._idleCount + lastSleep
				
				# If the host is a cloud VM, determine if shutting down would be cost-effective
				costEffective = self._billing == 0 or (self._uptime % self._billing) > (self._billing * self._percentage)
				
				# If we have exceeded the idle timeout threshold, and it is cost-effective to do so, then perform a shutdown
				if self._idleCount >= self._timeout and costEffective == True:
					Shutdown.shutdown()
					return
			
			# Sleep until the next sampling run
			time.sleep(self._sleep)
