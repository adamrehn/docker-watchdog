from os.path import abspath, dirname, join
from setuptools import setup

# Read the README markdown data from README.md
with open(abspath(join(dirname(__file__), 'README.md')), 'rb') as readmeFile:
	__readme__ = readmeFile.read().decode('utf-8')

setup(
	name='docker-watchdog',
	version='0.0.5',
	description='Service to perform automatic shutdown of idle container hosts',
	long_description=__readme__,
	long_description_content_type='text/markdown',
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Software Development :: Build Tools',
		'Environment :: Console'
	],
	keywords='docker continuous-integration',
	url='http://github.com/adamrehn/docker-watchdog',
	author='Adam Rehn',
	author_email='adam@adamrehn.com',
	license='MIT',
	packages=['docker_watchdog'],
	zip_safe=True,
	python_requires = '>=3.5',
	install_requires = [
		'docker>=3.0.0',
		'humanfriendly',
		'requests',
		'setuptools>=38.6.0',
		'twine>=1.11.0',
		'uptime',
		'wheel>=0.31.0'
	],
	entry_points = {
		'console_scripts': ['docker-watchdog=docker_watchdog:main']
	}
)
