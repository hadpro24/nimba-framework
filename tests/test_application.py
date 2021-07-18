import unittest
import pathlib
import sys
import socket
from unittest.mock import patch

from nimba.core.server import Application
from nimba.core.welcom import home_default

from nimba.http import router, render

TEST = 'test'

@router('/')
def home(request):
	return TEST

def get_free_port():
    """Finds an available TCP/IP port"""
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port

class TestApplication(unittest.TestCase):
	def setUp(self):
		self.application = Application(
			pathlib.Path(__file__).parent.absolute(),
			home,
		)

	@patch('subprocess.Popen')
	def test_run_application(self, mock):
		class Options:
			host = 'localhost'
			port = get_free_port()
		# self.application.run('--reload', Options())
		self.assertFalse(mock.called)
