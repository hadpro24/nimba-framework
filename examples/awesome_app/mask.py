#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import sys

from nimba.core.welcom import home_default as application

def main():
    try:
        from nimba.commands import mont_nimba
    except ImportError as e:
        raise ImportError(
            "Couldn't import nimba server. Active your environnement"
            "or install nimba framework (ex: pip install nimba-framework)"
        )
    mont_nimba(sys.argv, pathlib.Path(__file__).parent.absolute())

if __name__ == '__main__':
    main()
