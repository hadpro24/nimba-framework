import platform
import signal
import socket
import socketserver
import threading
import subprocess
from datetime import datetime

import argparse
import sys
import os
import importlib
from wsgiref import simple_server
import optparse

import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler

LISTEN_QUEUE = 128
can_open_by_fd = not platform.system() == "Windows" and hasattr(socket, "fromfd")

class Application:
    def __init__(self, path_file, app_view):
        self.name = '.'.join(str(path_file)[1:].split('/'))
        self.app_path = path_file
        self.httpd = None
        self.server_process = None
        self.port = 8000
        self.host = '127.0.0.1'
        self.app_view = app_view
        os.environ.setdefault('PROJECT_MASK_PATH', str(path_file))


    def create_subprocess(self, app_path):
        py_command = 'python' if sys.platform == 'win32' else 'python3'
        shell_arg = [py_command] + [   
            arg for arg in sys.argv if arg != '--reload'
        ]+['--noreload'] #for new
        self.server_process = subprocess.Popen(
            shell_arg,
            stdout=sys.stdout, stderr=sys.stderr
        )

    def watch_and_serve(self, host, port, app_path):
        from watchdog.observers import Observer
        from watchdog.events import (
            FileSystemEventHandler, FileSystemMovedEvent, FileModifiedEvent,
            DirModifiedEvent
        )
        print('Monitoring for changes...')
        self.create_subprocess(app_path)

        parent = self

        class EventHandler(PatternMatchingEventHandler):
            lock = threading.Lock()

            def should_reload(self, event):
                for t in (
                    FileSystemMovedEvent, FileModifiedEvent, DirModifiedEvent
                ):
                    if isinstance(event, t):
                        return True
                return False

            def on_modified(self, event):
                if self.should_reload(event) and self.lock.acquire(False):
                    print(f"Change on {event.src_path}. reloading...")
                    print()
                    parent.server_process.kill()
                    parent.create_subprocess(app_path)
                    time.sleep(1)
                    self.lock.release()

        event_handler = EventHandler(
            patterns=["*.py", "*.pyc", "*.zip"],
            ignore_patterns=[
                "*/__pycache__/*",
                "*/.git/*",
                "*/.hg/*",
            ],
        )
        observer = Observer()
        observer.schedule(event_handler, app_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def log_server_status(self, host, port):
        now = datetime.now().strftime('%B %d, %Y - %X')
        print(now)
        if host == '0.0.0.0':
            print(
                'serving on 0.0.0.0:%s, view at http://127.0.0.1:%s' %
                (port, port)
            )
        else:
            print('Serving on http://%s:%s' % (host, port))
        quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'
        print(f'Quit the server with {quit_command}.')

    def _serve(self, host, port):
        host, port = host, int(port)
        srv = simple_server.make_server(
            host, port, self.app_view
        )
        print('Starting server in PID %s' % os.getpid())
        self.log_server_status(host, port)
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass

    def run(self, rload, options):
        self.host, self.port, = options.host, options.port
        #start realod
        if rload == '--noreload':
            #no reload
            self._serve(self.host, self.port)
        else:
            try:
                self.watch_and_serve(self.host, self.port, self.app_path)
            except ImportError:
                print('`watchdog` require to be installed.')
                print('$ pip install watchdog')
        
