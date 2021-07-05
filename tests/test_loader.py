import io
import unittest
from unittest.mock import patch
from nimba.commands.base import Loader

class TestLoaderClass(unittest.TestCase):
	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader(self, mock):
		with Loader("Create application...", "Done!"):
			pass
		self.assertIn("Create application...", mock.getvalue())
		self.assertIn("Done!", mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader_not_message_done(self, mock):
		with Loader("Create application..."):
			pass
		self.assertIn("Create application...", mock.getvalue())
		self.assertIn("Done!", mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader_not_message(self, mock):
		with Loader():
			pass
		self.assertIn("Loading...", mock.getvalue())
		self.assertIn("Done!", mock.getvalue())


	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader_not_message_with_time(self, mock):
		with Loader(timeout=1):
			pass
		self.assertIn("Loading...", mock.getvalue())
		self.assertIn("Done!", mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader_not_message_with_done(self, mock):
		with Loader(desc="Create application...", timeout=1):
			pass
		self.assertIn("Create application...", mock.getvalue())
		self.assertIn("Done!", mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader_message_with_time(self, mock):
		with Loader(desc="Create application...", end='Done!',  timeout=1):
			pass
		self.assertIn('Create application...', mock.getvalue())
		self.assertIn("Done!", mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader_message_line(self, mock):
		ld = Loader(desc="Create application...", end='Done!',  timeout=1)
		ld.start()
		ld.stop()
		self.assertIn('Create application...', mock.getvalue())
		self.assertIn("Done!", mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader__without_message_line(self, mock):
		ld = Loader(desc="Create application...", end='Done!')
		ld.start()
		ld.stop()
		self.assertIn('Create application...', mock.getvalue())
		self.assertIn("Done!", mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader__without_message_line_1(self, mock):
		ld = Loader(desc="Create application...")
		ld.start()
		ld.stop()
		self.assertIn('Create application...', mock.getvalue())
		self.assertIn("Done!", mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader__without_message_line_2(self, mock):
		ld = Loader()
		ld.start()
		ld.stop()
		self.assertIn('Loading...', mock.getvalue())
		self.assertIn("Done!", mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_app_loader__without_message_line_3(self, mock):
		ld = Loader(timeout=1)
		ld.start()
		ld.stop()
		self.assertIn('Loading...', mock.getvalue())
		self.assertIn("Done!", mock.getvalue())
