import gzip
import os
import sys
import warnings
from importlib import import_module
from time import sleep
import pathlib

from nimba.commands.base import Loader
from nimba.core.exceptions import AppNameIncorrect, CommandError

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
            #setting
            f = open(os.path.join(path_application, 'settings.py'), 'w+')
            f.close()
            #copy file
            original = os.path.basename(sys.argv[0])
            shutil.copyfile(original, os.path.join(path_application, original))
            #verify emplacement
            sleep(0.5)



       