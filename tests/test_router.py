import io
import os
import pathlib
import unittest
import shutil
import sys
import time
import pytest
import shutil
from unittest.mock import patch

from nimba.http import router, render
from nimba.core.server import Application

from nimba.test.client import TestCase

TEST = 'test'

@router('/about')
def about(request):
	if request.GET.get('id'):
		return 'yes'
	return TEST

@router('/articles')
def articles(request):
	return TEST

@router('/article/<int:id>')
def article(request, id):
	return str(id)

@router('/me')
def me(request):
	return render('awesome_app/me.html')

class TestRouterRender(TestCase):
	def setUp(self):
		os.environ['PROJECT_MASK_PATH'] = str(pathlib.Path(
			__file__
		).parent.absolute())
		self.url = 'tests/templates/awesome_app'
		os.makedirs(self.url)
		f = open(os.path.join(self.url, 'home.html'), 'w+')
		f.write(TEST)
		f.close()
		#wrtie me
		f = open(os.path.join(self.url, 'me.html'), 'w+')
		f.write('hello, world')
		f.close()

	def test_route_home(self):
		response = self.get('/')
		self.assertEqual(200, response['status_code'])
		self.assertEqual(TEST, response['text'])

	def test_route_about(self):
		response = self.get('/about')
		self.assertEqual(200, response['status_code'])
		self.assertEqual(TEST, response['text'])

	def test_route_about_with_query(self):
		response = self.get('/about?id=5')
		self.assertEqual(200, response['status_code'])
		self.assertEqual('yes', response['text'])

	def test_route_article_with_id(self):
		response = self.get('/article/5')
		self.assertEqual(200, response['status_code'])
		self.assertEqual('5', response['text'])

	def test_route_404(self):
		response = self.get('/no-exist')
		self.assertEqual(404, response['status_code'])
		self.assertIn("Not found route", response['text'])

	def test_route_with_template(self):
		response = self.get('/me')
		self.assertEqual(200, response['status_code'])
		self.assertIn("hello, world", response['text'])

	def tearDown(self):
		try:
			shutil.rmtree('tests/templates')
		except Exception as e:
			print("Error: %s - %s." % (e.filename, e.strerror))
