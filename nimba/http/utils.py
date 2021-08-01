import os
import io
import re
import http.client
from wsgiref.headers import Headers
import pathlib
import urllib.parse
from collections.abc import Iterable

import traceback
import mimetypes
import sys

from wsgiref import util
from jinja2 import Template
from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape
from jinja2 import BaseLoader
import tempfile
import json

from nimba.http.request import Request
from nimba.http.response import Response
from nimba.http.resolver import (
	resolve_pattern,
	check_pattern,
	is_valid_method
)
from nimba.http.errors import (
	error_401,
	error_404,
	error_500
)
from nimba.core.exceptions import (
	NoReverseFound
)

ROUTES = {}
REVERSE_ROUTE_INFO = {}
PROJECT_MASK = 'PROJECT_MASK_PATH'

def json_render(data, status=200):
	"""
		render json data
	"""
	data = json.dumps(data)
	headers = Headers()
	headers.add_header('Content-Type', 'application/json')
	status_string = http.client.responses.get(status, 'UNKNOWN')
	response = {
		'status': f'{status} {status_string}',
		'content': [data.encode('utf-8')],
		'headers': headers,
	}
	return response

def reverse(name_path, *args, **kwargs):
	"""
		Reverse path using name or function name str
		Example:
			@router('/', name='home')
			def home(request):
				return 'welcom home'

			@router('/article/<int:id>', name='article')
			def home(request, id):
				return 'welcom article'

			@router('/about')
			def home(request):
				return 'welcom about'

			reverse('name') ==> '/'
			reverse('article', id=5) ==> '/article/5'
			reverse('about') ==> '/about'
	"""
	if (not isinstance(name_path, str) or
		 not re.match(r"^[^\d\W][\w-]*\Z", name_path)):
			raise ValueError("Name path must but a valid identifier name.")
			
	args = kwargs.get('args') or args or {}
	kwargs.pop('args', None)
	kwargs = kwargs.get('kwargs') or kwargs or {}
	
	if args and kwargs:
		raise ValueError(("You can't mix *args and **kwargs."))
	if not isinstance(args, Iterable) or not isinstance(kwargs, dict):
	    raise ValueError("*args or **kwargs must be list and dict respectively")
	    
	path, view = REVERSE_ROUTE_INFO.get(name_path) or (None, None)
	original_path = path
	if not path:
		raise NoReverseFound(f"Reverse for {name_path} not found.")
	regex = r'<(?:(?P<converter>[^>:]+):)?(?P<parameter>[^>]+)>'
	url  = re.compile(regex, 0)
	params_path = list(url.finditer(path))
	got_params = args or kwargs
	if len(params_path) != len(got_params):
	    raise ValueError((f"The view `{view}` expects {len(params_path)} " 
	    	f"parameters but has received {len(got_params)}"))
	if args:
		for arg, match in zip(args, params_path):
			path = re.sub(
				original_path[match.start():match.end()], 
				urllib.parse.quote(str(arg)), 
				path
			)
	else:
		for match in params_path:
			value = kwargs.get(match['parameter'])
			if not value:
				raise NoReverseFound((f"Reverse for `{name_path}` not found. " 
					"Keyword arguments '%s' not found." % match['parameter']))
			path = re.sub(
				original_path[match.start():match.end()], 
				urllib.parse.quote(str(value)), 
				path
			)
	return path

def redirect(to, partial=False):
	"""
		redirect http
	"""
	status = '302 Found' if partial else '301 Moved Permanently'
	path = reverse(to)
	headers = Headers()
	headers.add_header('Location', path)
	response = {
		'status': status,
		'content': [b''],
		'headers': headers,
	}
	return response

def load_static(value):
	return os.path.join('/staticfiles/', value)

def render(template, contexts=None, status=200, charset='utf-8', content_type='text/html'):
	"""
		Rendering template
	"""
	contexts = contexts or {}
	os.environ.setdefault(PROJECT_MASK, 'wrong-template')
	relative_path = os.path.join(os.path.dirname(__file__), '../')
	mask_path = os.path.join(relative_path, f'templates/{template}')
	project_path = os.path.join(os.environ.get(PROJECT_MASK), f'templates/{template}')

	path = mask_path if os.path.exists(mask_path) else project_path
	#set header
	_status = status
	headers = Headers()
	ctype   = f'{content_type}; charset={charset}'
	headers.add_header('Content-type', ctype)
	env = Environment(
	    loader=BaseLoader(),
	    autoescape=select_autoescape(['html', 'xml'])
	)
	#load env jinja2
	contexts['load_static'] = load_static
	contexts['reverse'] = reverse
	with open(path, 'r') as content_file:
		content = content_file.read()
		html_render = env.from_string(content)
	html_render = io.BytesIO(html_render.render(contexts).encode())
	content_response = util.FileWrapper(html_render)

	# headers.add_header('Content-Length', str(len(content)))
	status_string = http.client.responses.get(_status, 'UNKNOWN')
	status = f'{_status} {status_string}'
	response = {
	  'status': status,
	  'headers': headers,
	  'content': content_response,
	}
	return response


def router(path, methods=['GET'], name=None):
	"""
		Routing app
	"""
	def request_response_application(callback):
		global ROUTES
		is_valid_method(methods)
		#validate path
		check_pattern(path)
		#format url value url
		new_path, converters = resolve_pattern(path, callback)
		ROUTES[new_path] = (callback, converters, path, methods)

		# if: pass
		REVERSE_ROUTE_INFO[name or callback.__name__] = path, callback.__name__
		def application(environ, start_response):
			request = Request(environ)
			#authorized
			route = f"/{environ['PATH_INFO'][1:]}"
			realCallback = None
			kwargs       = None
			realMethods  = None
			#render favicon
			if route == '/favicon.ico':
				headers  = Headers()
				ctype    = 'image/png; charset=utf-8'
				headers.add_header('content-type', ctype)
				start_response('404 Not Found', headers.items())
				return [b'Not found']
			relative_path = os.path.join(os.path.dirname(__file__), '../')
			mask_path = str(relative_path)+str(route)
			project_path = str(os.environ.get(PROJECT_MASK)) + str(route)
			static_path = mask_path if os.path.exists(mask_path) else project_path
			# render static files
			if route.startswith('/staticfiles') and os.path.exists(static_path) and not os.path.isdir(static_path):
				headers  = Headers()
				mime = mimetypes.MimeTypes().guess_type(static_path)[0]
				ctype    = f'{mime}; charset=utf-8'
				headers.add_header('content-type', ctype)
				start_response('200 OK', headers.items())
				return iter(util.FileWrapper(open(static_path, 'rb')))
			# render media files comming...
			#get routing
			for new_path, callback_converter in ROUTES.items():
				match = re.search(new_path, route)
				if match:
					realCallback = callback_converter[0]
					converters   = callback_converter[1]
					realMethods  = callback_converter[3]
					kwargs = []
					for name, value in match.groupdict().items():
						kwargs.append(converters[name].to_python(value))
			if realCallback:
				#verify method
				#verify request
				if request.method not in realMethods:
					#unothorize method
					response = render(*error_401(request, route, 401, '401 Unauthorized'))
				else:
					#Response
					try:
						response =  realCallback(request, *tuple(kwargs))
					except Exception as e:
						response = render(*error_500(request, route, traceback.format_exc(100), e))
					#check
					if isinstance(response, str):
						headers = Headers()
						ctype   = f'text/html; charset=utf-8'
						headers.add_header('Content-type', ctype)
						html_render = Template(response)
						contexts = {}
						contexts['load_static'] = load_static
						content_response = io.BytesIO(html_render.render(contexts).encode())
						response = {
							'status': '200 OK',
							'content': content_response,
							'headers': headers,
						}
					# check if redirect
					# check if serializer
			else:
				response = render(*error_404(request, route, ROUTES))
			start_response(response['status'], response['headers'].items())
			return iter(response['content'])
		return application
	return request_response_application
