import unittest
import pathlib
import sys
import io
import os
import shutil
from unittest.mock import patch

import nimba.commands
from nimba.commands.createapp import CreateApp
from nimba.core.exceptions import AppNameIncorrect, CommandError

class TestCommandUtility(unittest.TestCase):
	def setUp(self):
		self.path = pathlib.Path(__file__).parent.absolute()
		self.valid_app_name_test = 'app_test'
		self.path_app = os.path.join(
			self.path, f'../{self.valid_app_name_test}')
		#create app similator
		self.create_app(self.valid_app_name_test)

	def create_app(self, name):
		app = CreateApp(name, self.path)
		app.handle()

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_create_invalid_app_name(self, mock):
		with self.assertRaises(AppNameIncorrect) as error:
			name = "invalid name"
			self.create_app(name)
		# self.assertIn(f"AppNameIncorrect: Your name '{name}' is not a valid app name.", 
		# 	error.msg)
		with self.assertRaises(AppNameIncorrect) as error:
			name = ""
			self.create_app(name)
		#duplicate
		with self.assertRaises(CommandError) as error:
			name = self.valid_app_name_test
			self.create_app(name)

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_run_mask_without_create_app(self, mock):
		#set invalid path
		os.environ['APP_MASK_VIEW'] = 'app_wrong.app.views'
		sys.argv = ["python3", "mask.py"]
		nimba.commands.mont_nimba(
			sys.argv,
			pathlib.Path(__file__).parent.absolute(),
		)
		self.assertIn(
			"Warning: The 'app' or 'views' module not found",
			mock.getvalue(), 
		)

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_run_mask_only(self, mock):
		#set default
		with self.assertRaises(SystemExit) as error:
			os.environ.setdefault("APP_MASK_VIEW", "app_test.app.views")
			os.environ['APP_MASK_VIEW'] = 'app_test.app.views'
			sys.argv = ["mask.py",]
			nimba.commands.mont_nimba(
				sys.argv,
				pathlib.Path(__file__).parent.absolute(),
			)
		self.assertEqual(error.exception.code, 2)
		self.assertIn("Usage: mask.py [OPTIONS] MODULE:EXPRESSION", 
			mock.getvalue())


		with self.assertRaises(SystemExit) as error:
			os.environ.setdefault("APP_MASK_VIEW", "app_test.app.views")
			os.environ['APP_MASK_VIEW'] = 'app_test.app.views'
			sys.argv = ["mask.py", "help"]
			nimba.commands.mont_nimba(
				sys.argv,
				pathlib.Path(__file__).parent.absolute(),
			)
		self.assertEqual(error.exception.code, 2)
		self.assertIn("Usage: mask.py [OPTIONS] MODULE:EXPRESSION", 
			mock.getvalue())

		with self.assertRaises(SystemExit) as error:
			os.environ.setdefault("APP_MASK_VIEW", "app_test.app.views")
			os.environ['APP_MASK_VIEW'] = 'app_test.app.views'
			sys.argv = ["mask.py", "--version"]
			nimba.commands.mont_nimba(
				sys.argv,
				pathlib.Path(__file__).parent.absolute(),
			)
		self.assertEqual(error.exception.code, 2)
		self.assertIn("Nimba Framework version installed", 
			mock.getvalue())


	@patch('sys.stdout', new_callable=io.StringIO)
	def test_params_without_value(self, mock):
		# test param without value
		with self.assertRaises(SystemExit) as error:
			os.environ.setdefault("APP_MASK_VIEW", "app_test.app.views")
			os.environ['APP_MASK_VIEW'] = 'app_test.app.views'
			sys.argv = ["mask.py", "serve", "-H"]
			nimba.commands.mont_nimba(
				sys.argv,
				pathlib.Path(__file__).parent.absolute(),
			)
		self.assertEqual(error.exception.code, 2)
		# self.assertIn("error: -H option requires 1 argument", 
		# 	mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_params_without_value_port(self, mock):
		# test param without value
		with self.assertRaises(SystemExit) as error:
			os.environ.setdefault("APP_MASK_VIEW", "app_test.app.views")
			os.environ['APP_MASK_VIEW'] = 'app_test.app.views'
			sys.argv = ["mask.py", "serve", "-P"]
			nimba.commands.mont_nimba(
				sys.argv,
				pathlib.Path(__file__).parent.absolute(),
			)
		self.assertEqual(error.exception.code, 2)
		# self.assertIn("error: -H option requires 1 argument", 
		# 	mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_params_without_value_version(self, mock):
		# test param without value
		with self.assertRaises(SystemExit) as error:
			os.environ.setdefault("APP_MASK_VIEW", "app_test.app.views")
			os.environ['APP_MASK_VIEW'] = 'app_test.app.views'
			sys.argv = ["mask.py", "-V"]
			nimba.commands.mont_nimba(
				sys.argv,
				pathlib.Path(__file__).parent.absolute(),
			)
		self.assertEqual(error.exception.code, 2)
		# self.assertIn("error: -H option requires 1 argument", 
		# 	mock.getvalue())

	@patch('sys.stdout', new_callable=io.StringIO)
	def test_params_without_invalid_value(self, mock):
		# test param without value
		with self.assertRaises(SystemExit) as error:
			os.environ.setdefault("APP_MASK_VIEW", "app_test.app.views")
			os.environ['APP_MASK_VIEW'] = 'app_test.app.views'
			sys.argv = ["mask.py", "serve", "--wrong"]
			nimba.commands.mont_nimba(
				sys.argv,
				pathlib.Path(__file__).parent.absolute(),
			)
		self.assertEqual(error.exception.code, 2)
		# self.assertIn("error: -H option requires 1 argument", 
		# 	mock.getvalue())


	def tearDown(self):
		#delete app
		try:
			shutil.rmtree(self.path_app)
		except Exception as e:
			print("Error: %s - %s." % (e.filename, e.strerror))
			