import gzip
import os
import sys
import warnings
from importlib import import_module
from time import sleep
import pathlib

from nimba.commands.base import Loader
from nimba.core.exceptions import AppNameIncorrect, CommandError
from nimba.core.welcom import DEFAULT_DIRECTORY_INDEX_TEMPLATE

manager_file = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import sys

def main():
    try:
        from nimba.commands import mont_nimba
    except ImportError as e:
        raise ImportError(
            "Couldn't import nimba server. Active your environnement"
            "or install nimba framework (ex: pip install nimba)"
        )
    mont_nimba(sys.argv, pathlib.Path(__file__).parent.absolute())

if __name__ == '__main__':
    main()
"""

import_view = f"""from nimba.http import router, render

@router('/')
def home(request):
    return render('awesome_app/home.html')
"""

import_test = """# write your test here """
import_models = """# write your models here """
import_settings = """# all settings application """

class CreateApp:
    """
        Creating app command
    """
    def __init__(self, app_label, path_to_create):
        self.app_label = f'{app_label}'
        self.path_to_create = path_to_create

    def handle(self):
        #check name application
        if not self.app_label or not self.app_label.isidentifier() or self.app_label == 'None':
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
            #create application
            os.makedirs(path_application)
            os.makedirs(os.path.join(path_application, 'application'))
            os.makedirs(os.path.join(path_application, f'templates/{self.app_label}'))
            os.makedirs(os.path.join(path_application, 'staticfiles'))
            #template
            f = open(os.path.join(path_application, f'templates/{self.app_label}', 'home.html'), 'w+')
            f.write(DEFAULT_DIRECTORY_INDEX_TEMPLATE)
            f.close()
            #init
            f = open(os.path.join(path_application, 'application', '__init__.py'), 'w+')
            f.close()
            f = open(os.path.join(path_application, 'application', 'models.py'), 'w+')
            f.write(import_models)
            f.close()
            f = open(os.path.join(path_application, 'application', 'views.py'), 'w+')
            f.write(import_view)
            f.close()
            f = open(os.path.join(path_application, 'application', 'tests.py'), 'w+')
            f.write(import_test)
            f.close()
            #setting
            f = open(os.path.join(path_application, 'settings.py'), 'w+')
            f.write(import_settings)
            f.close()
            #copy file
            with open(os.path.join(path_application, 'mask.py'), 'w+') as file:
                file.write(manager_file)
            #verify emplacement
            sleep(0.5)

