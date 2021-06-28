import sys
import os
import argparse
import pathlib
import optparse
import traceback
import importlib

from nimba.commands.createapp import CreateApp
from nimba.core.server import Application
from wsgiref.validate import validator

class CommandUtility:
	"""
		logic command utility nimba framework
	"""
	def __init__(self, path_app, argv=None):
		self.argv = argv or sys.argv[:]
		self.prog_name = os.path.basename(self.argv[0])
		self.path_app = path_app
		try:
			self.subcommand = self.argv[1]
		except IndexError:
			self.subcommand = 'help'

	def execute(self, app):
		"""
			exectue command
		"""
		parser = optparse.OptionParser(
        	usage='%prog [OPTIONS] MODULE:EXPRESSION')
		parser.add_option(
	        '-p', '--port', default='8000',
	        help='Port to serve on (default 8080)')
		parser.add_option(
	        '-H', '--host', default='127.0.0.1',
	        help='Host to serve on (default localhost; 0.0.0.0 to make public)')
		parser.add_option(
	        '--noreload', default=False, action='store_true',
	        help='No reload server')
		parser.add_option(
	        '-V', '--version', default=False, action='store_true',
	        help='Nimba Framework version installed')
		#fonctionality
		parser.add_option(
	        '--app', help='create application with the structure.'
	    )
		options, args = parser.parse_args()
		#error command
		if (not options.version or not args) and self.subcommand == 'help':
			parser.print_help()
			sys.exit(2)
		#runserver
		if self.subcommand == 'serve':
			if options.noreload:
				Application(
					self.path_app, validator(app)
				).run('--noreload', options)
			else:
				Application(
					self.path_app, validator(app)
				).run('--reload', options)
		elif self.subcommand == 'create':
			app = CreateApp(options.app, self.prog_name)
			try:
				app.handle()
			except Exception as e:
				print(e)
		elif (
			self.subcommand == 'version' or self.subcommand == '--version' or options.version
		):
			from nimba import __version__
			print(f"Nimba Framework {__version__}")
			print("Nimba Solution Compagny all rights reserved.")

def mont_nimba(argv, path_app):
	#create app
	from nimba.core.welcom import home_default
	view_module = importlib.import_module('app.views')
	for attr in dir(view_module):
		if hasattr(attr, '__call__'):
			locals()[attr] = getattr(view_module, attr)
	utility = CommandUtility(path_app, argv)
	utility.execute(home_default)
