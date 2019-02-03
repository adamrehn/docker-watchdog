import json, os, platform

class ConfigurationManager(object):
	'''
	Manages the configuration settings for the watchdog
	'''
	
	@staticmethod
	def getConfigDirectory():
		'''
		Determines the platform-specific location for the watchdog config directory
		'''
		if platform.system() == 'Windows':
			return os.path.join(os.environ['APPDATA'], 'docker-watchdog')
		elif os.getuid() != 0:
			return os.path.join(os.environ['HOME'], '.config', 'docker-watchdog')
		else:
			return '/etc/docker-watchdog'
	
	def __init__(self):
		'''
		Reads configuration settings from either the config file or environment variables.
		Sane defaults are provided for any missing values.
		'''
		
		# If the config file exists, parse it
		configData = {}
		configFile = self._configFilePath()
		if os.path.exists(configFile) == True:
			with open(configFile, 'r') as f:
				configData = json.loads(f.read())
		
		# Store each of our settings, using the following source precedence:
		#  1. Config file
		#  2. Environment variable
		#  3. Sane default value
		self._config = {
			'sleep': int(self._findSetting(configData, 'sleep', 'DOCKER_WATCHDOG_SLEEP_INTERVAL', '60')),
			'timeout': int(self._findSetting(configData, 'timeout', 'DOCKER_WATCHDOG_IDLE_TIMEOUT', '600')),
			'billing': int(self._findSetting(configData, 'billing', 'DOCKER_WATCHDOG_BILLING_GRANULARITY', '0')),
			'percentage': float(self._findSetting(configData, 'percentage', 'DOCKER_WATCHDOG_EFFECTIVE_PERCENTAGE', '0.9'))
		}
		
		# Clamp the cost-effective percentage value to the range [0.0, 1.0]
		self._config['percentage'] = max(min(self._config['percentage'], 1.0), 0.0)
	
	def get(self, setting):
		'''
		Retrieves the value of the specified setting
		'''
		return self._config.get(setting, 0)
	
	
	# "Private" methods
	
	def _findSetting(self, data, key, envVar, default):
		'''
		Finds the appropriate value for a setting based on our source precedence rules
		'''
		if key in data:
			return data[key]
		elif envVar in os.environ:
			return os.environ[envVar]
		else:
			return default
	
	def _configFilePath(self):
		'''
		Determines the platform-specific location for the watchdog config file
		'''
		return os.path.join(ConfigurationManager.getConfigDirectory(), 'config.json')
