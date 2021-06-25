import gzip
import os
import sys
import warnings
from importlib import import_module
from time import sleep
import pathlib

from nimba.commands.base import Loader
from nimba.core.exceptions import AppNameIncorrect, CommandError


manager_file = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import sys

from app.views import * #import your view

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
"""
import_view = """from nimba.http import router, render

@router('/')
def home(request):
    return "Nimba Framework installed succesfuly!"
"""

class CreateApp:
    """
        Creating app command
    """
    def __init__(self, app_label, path_to_create):
        self.app_label = app_label
        self.path_to_create = path_to_create

    def handle(self):
        #check name application
        if not self.app_label or not self.app_label.isidentifier():
            raise AppNameIncorrect(
                "AppNameIncorrect: Your name '{name}' is not a valid app name. Please make sure the "
                "app name is a valid identifier.".format(
                    name=self.app_label,
                )
            )
        # Check it cannot be imported.
        path_application = os.path.join(
            pathlib.Path(self.path_to_create).parent.absolute(), 
            self.app_label
        )
        if os.path.exists(path_application):
            raise CommandError(
                "CommandError: '{name}' conflicts with the name of an existing Python "
                "module and cannot be used as app. Please try "
                "another name.".format(
                    name=self.app_label,
                )
            )
        with Loader("Create application...", "Done!"):
            import shutil
            #create application
            os.makedirs(path_application)
            os.makedirs(os.path.join(path_application, 'app'))
            os.makedirs(os.path.join(path_application, 'templates'))
            os.makedirs(os.path.join(path_application, 'staticfiles'))
            #init
            f = open(os.path.join(path_application, 'app', '__init__.py'), 'w+')
            f.close()
            f = open(os.path.join(path_application, 'app', 'models.py'), 'w+')
            f.close()
            f = open(os.path.join(path_application, 'app', 'views.py'), 'w+')
            f.write(import_view)
            f.close()
            #setting
            f = open(os.path.join(path_application, 'settings.py'), 'w+')
            f.close()
            #copy file
            with open(os.path.join(path_application, 'mask.py'), 'w+') as file:
                file.write(manager_file)
            #verify emplacement
            sleep(0.5)

