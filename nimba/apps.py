import pathlib
import sys
from nimba.commands import CommandUtility

def mont_nimba():
	#create app
	argv = sys.argv
	path_app = pathlib.Path(__file__).parent.absolute()
	utility = CommandUtility(path_app, argv)
	utility()