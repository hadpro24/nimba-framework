#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import sys

def main():
	try:
		from nimba.commands import run_command
	except ImportError as e:
		raise ImportError(
			"Couldn't import nimba server. Active your environnement"
			"or install nimba framework (ex: pip install nimba-framework)"
		)
	run_command(sys.argv, pathlib.Path(__file__).parent.absolute())

if __name__ == '__main__':
    main()
