import io
import os
import pathlib
import unittest
import shutil
import sys
import time
import shutil
import json
from unittest.mock import patch

from nimba.http import (
	router, render, reverse, redirect,
	json_render
)
from nimba.core.server import Application
from nimba.core.exceptions import NoReverseFound

from nimba.test.client import TestCase

from nimba.core.welcom import (
	DEFAULT_DIRECTORY_INDEX_TEMPLATE,
	home_default
)

TEST = 'test'

@router('/about')
def about(request):
	if request.GET.get('id'):
		return 'yes'
	return TEST

@router('/articles', name='articles')
def articles(request):
	return TEST

@router('/article/<int:id>', name='article')
def article(request, id):
	return str(id)

@router('/info', name='info')
def info(request):
	name = request.GET.get('name', '')
	return name

@router('/me')
def me(request):
	return render('awesome_app/me.html')

@router('/to-redirect')
def redirect_to(request):
	return 'Test direct'

@router('/move-partial')
def move_partial(request):
	return redirect('redirect_to', partial=True)

@router('/move', name='move')
def move(request):
	return redirect('redirect_to')

@router('/jsonify-post')
def post_data(request):
	return json_render(
		{'success': True, 'message': 'Email send successfuly!'},
		status=201
	)

@router('/jsonify-get')
def get_data(request):
	return json_render(
		{'success': True, 'data': [4, 5, 6]},
	)

@router('/users/create', methods=['POST'])
def users_post(request):
	return 'Ok'

@router('/users', methods=['GET'])
def users_list(request):
	return 'Ok'

@router('/error-test')
def error_test(request):
	raise ValueError("error")
	return 'Ok'

class TestRouterRender(TestCase):
	def setUp(self):
		os.environ['PROJECT_MASK_PATH'] = str(pathlib.Path(
			__file__
		).parent.absolute())
		self.url = 'tests/templates/awesome_app'
		os.makedirs(self.url)
		#wrtie me
		f = open(os.path.join(self.url, 'me.html'), 'w+')
		f.write('hello, world')
		f.close()

	def test_route_home(self):
		response = self.get('/')
		self.assertEqual(200, response['status_code'])
		self.assertIn(
			"Nimba Framework successfully installed",
			response['text']
		)

	def test_route_about(self):
		response = self.get('/about')
		self.assertEqual(200, response['status_code'])
		self.assertEqual(TEST, response['text'])

	def test_route_about_with_query(self):
		response = self.get('/about', data={'id': 5})
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

	def test_reverse_with_function_name(self):
		url = reverse('about')
		response = self.get(url)
		self.assertEqual(200, response['status_code'])
		self.assertEqual(TEST, response['text'])

	def test_reverse_with_name(self):
		url = reverse('articles')
		response = self.get(url)
		self.assertEqual(200, response['status_code'])
		self.assertEqual(TEST, response['text'])

	def test_method_authorized(self):
		url = reverse('users_post')
		response = self.get(url)
		self.assertEqual(401, response['status_code'])
		response = self.post(url)
		self.assertEqual(200, response['status_code'])

	def test_method_post(self):
		url =reverse('users_list')
		response = self.post(url)
		self.assertEqual(401, response['status_code'])

	def test_error_view(self):
		url = reverse('error_test')
		response = self.get(url)
		self.assertEqual(500, response['status_code'])

	def test_reverse_with_name_and_kwargs(self):
		#error type name path
		with self.assertRaises(ValueError) as error:
			reverse(57885)
		self.assertEqual(str(error.exception), "Name path must but a valid identifier name.")
		#bad name give
		invalid_path = 'invalid-article'
		with self.assertRaises(NoReverseFound) as error:
			reverse(invalid_path)
		self.assertEqual(str(error.exception), f"Reverse for {invalid_path} not found.")
		#give kwargs and args
		with self.assertRaises(ValueError) as error:
			reverse('article', kwargs={'id': 5}, args={'name': 'test'})
		self.assertEqual(str(error.exception), "You can't mix *args and **kwargs.")
		#invalid parmas name
		invalid_params = 'id_wrong'
		with self.assertRaises(NoReverseFound) as error:
			reverse('article', kwargs={invalid_params: 5})
		self.assertEqual(str(error.exception), ("Reverse for `article` not found. " 
					"Keyword arguments 'id' not found."))
		#valid
		_id = 5
		url = reverse('article', kwargs={'id': _id})
		response = self.get(url)
		self.assertEqual(200, response['status_code'])
		self.assertEqual(str(_id), response['text'])

	def test_reverse_with_args(self):
		name = 'Harouna Diallo'
		with self.assertRaises(ValueError) as error:
			url = reverse('info', args={'name': name})
		self.assertEqual(str(error.exception), 
			f"The view `info` expects 0 parameters but has received 1")
		url = reverse('info')
		response = self.get(url, data={'name': name})
		self.assertEqual(200, response['status_code'])
		self.assertEqual(name, response['text'])

	def test_redirect_partial(self):
		response = self.get(reverse('move_partial'))
		self.assertEqual(200, response['status_code'])
		self.assertEqual('Test direct', response['text'])

	def test_redirect_permanente(self):
		response = self.get(reverse('move'))
		self.assertEqual(200, response['status_code'])
		self.assertEqual('Test direct', response['text'])

	def test_json_render(self):
		response = self.get(reverse('post_data'))
		self.assertEqual(response['status_code'], 201)
		data = json.loads(response['text'])
		self.assertEqual(data['success'], True)
		self.assertTrue(data['message'])

	def test_json_render(self):
		response = self.get(reverse('get_data'))
		self.assertEqual(response['status_code'], 200)
		data = json.loads(response['text'])
		self.assertEqual(data['success'], True)
		self.assertTrue(data['data'])

	def tearDown(self):
		try:
			shutil.rmtree('tests/templates')
		except Exception as e:
			print("Error: %s - %s." % (e.filename, e.strerror))
