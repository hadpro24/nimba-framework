import unittest
import importlib
import select
import socket
import threading
import os
import sys
import wsgiref.simple_server
import pathlib
from io import BytesIO
import urllib
import urllib.request
import logging
import http.client
import json
from collections import namedtuple

from nimba.http.request import Request
from nimba.http.response import Response
from nimba.core.welcom import home_default

logging.getLogger("urllib.request").setLevel(logging.WARNING)

def get_free_port():
    """Finds an available TCP/IP port"""
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port

class BaseServer:
    __stop_marker = 'stop'

    def __init__(self, app, host='localhost', port=8888):
        self.app = app
        self.host = host
        self.port = port

        self.stop_read, self.stop_write = os.pipe()
        self.started = False


    def _run(self):
        httpd = wsgiref.simple_server.make_server(
            self.host, self.port, self.app
        )
        # Don't to log
        # log_request = httpd.RequestHandlerClass.log_request
        # no_logging = lambda *args, **kwargs: None
        # httpd.RequestHandlerClass.log_request = no_logging

        self.ready.set()
        while True:
            ready, dummy, dummy = select.select(
                [httpd, self.stop_read], [self.stop_write], []
            )
            if httpd in ready:
                httpd.handle_request()

            if self.stop_read in ready:
                os.read(self.stop_read, len(self.__stop_marker))
                # httpd.RequestHandlerClass.log_request = log_request
                break


    def start(self):
        """
            Lauches the server in thread
        """
        if not self.started:
            self.ready = threading.Event()
            self.server_thread = threading.Thread(target=self._run)
            self.server_thread.setDaemon(True)
            self.server_thread.start()


            self.ready.wait()
            self.started = True

    def stop(self):
        """
            Stop and kill server and thread
        """
        if self.started:
            self.server_thread.do_run = False
            self.ready.set()
            self.server_thread.join(0.01)
            self.started = False

class TestCase(unittest.TestCase):
    errors = BytesIO()

    @classmethod
    def setUpClass(cls):
        cls.port = get_free_port() #port arbitrary
        cls.base_url = 'http://localhost:{}'.format(cls.port)
        #load applicaton views
        try:
            view_module = importlib.import_module(
                os.environ.get('APP_MASK_VIEW', 'app.views')
            )
            for attr in dir(view_module):
                if hasattr(attr, '__call__'):
                    locals()[attr] = getattr(view_module, attr)
        except ModuleNotFoundError:
            pass
        finally:
            cls.server = BaseServer(home_default, port=cls.port)
            cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def get(self, path, data=None, secure=False):
        """Construct a GET request."""
        data = {} if data is None else data
        if data:
            query_string = urllib.parse.urlencode(data)
            url = path+'?'+query_string
        else:
            url = urllib.parse.quote(path)

        url = self.base_url+url
        res = {}
        f = open(os.devnull, 'w')
        old_target = sys.stdout
        sys.stdout = f
        try:
            response = urllib.request.urlopen(url)
            res['status_code'] = response.code
            res['text'] = response.read().decode('utf-8')
        except urllib.error.HTTPError as error:
            res['status_code'] = error.code
            # response['text'] = e.msg
            res['text'] = error.file.read().decode('utf-8')
        except urllib.error.URLError as error_sys:
            res['status_code'] = error_sys.code
            res['text'] = error_sys.read().decode('utf-8')
        f.close()
        sys.stdout = old_target
        return res

    def post(self, path, data=None, secure=False,
        content_type='multipart/form-data; boundary=BoUnDaRyStRiNg'):
        data = self._encode_json({} if data is None else data, content_type)
        query_string = urllib.parse.urlencode(data)
        data = query_string.encode('ascii')
        path = self.base_url+path
        with urllib.request.urlopen(path, data) as response:
            response_text = response.read()
        return response_text

    def _encode_json(self, data, content_type):
        """
        Return encoded JSON if data is a dict, list, or tuple and readlinescontent_type
        is application/json.
        """
        # should_encode = JSON_CONTENT_TYPE_RE.match(content_type) and isinstance(data, (dict, list, tuple))
        return str(json.dumps(data)).encode('utf-8')


