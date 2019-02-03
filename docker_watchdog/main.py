from humanfriendly import format_timespan as format_time
from .ConfigurationManager import ConfigurationManager
from .Installation import Installation
from .Watchdog import Watchdog
import argparse, sys

def main():
	
	# Parse the supplied command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--install', action='store_true', help='Install docker-watchdog as a service that runs at startup')
	args = parser.parse_args()
	
	# Determine if we are performing installation or running the watchdog
	if args.install == True:
		
		# Attempt to install the startup service
		try:
			Installation.install()
		except RuntimeError as e:
			print('\nError:\n{}'.format(e), file=sys.stderr)
			sys.exit(1)
		
	else:
		
		# Configure the watchdog using our config file or environment variables
		config = ConfigurationManager()
		watchdog = Watchdog(
			config.get('sleep'),
			config.get('timeout'),
			config.get('billing'),
			config.get('percentage')
		)
		
		# Log the configuration settings being used
		print('Starting Docker watchdog with the following settings:')
		print('Sleep interval:             ' + format_time(config.get('sleep')))
		print('Inactivity timeout:         ' + format_time(config.get('timeout')))
		print('Billing granularity:        ' + format_time(config.get('billing')))
		print('Cost-effective percentage:  {:.0f}%'.format(config.get('percentage') * 100.0))
		sys.stdout.flush()
		
		# Start the watchdog
		watchdog.start()
		
		# If we reach this point then a shutdown has been initiated
		print('Performing system shutdown...')
