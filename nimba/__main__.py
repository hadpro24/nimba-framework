import sys
import pathlib

if __name__ == '__main__':
	from nimba.commands import mont_nimba
	mont_nimba(sys.argv, pathlib.Path(__file__).parent.absolute())
