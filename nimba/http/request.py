import urllib.parse
import cgi
import ast
# import multipart

# from nimba.http.cookies import SimpleCookie, set_cookie_header

class Request:
	def __init__(self, environ):
		self.environ = environ
		self._method = self.environ['REQUEST_METHOD'].upper()
		self.fields = {}
		self.files  = {}
		# self.cookies = SimpleCookie()
		self.COOKIES = {}
		if self._method == 'GET':
			try:
				self.request_body_size = int(environ.get('CONTENT_LENGTH', 0))
			except (ValueError, KeyError):
				self.request_body_size = 0
			self.request_body = self.environ['wsgi.input'].read(self.request_body_size)
		else:
			post = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ, keep_blank_values=True)
			self.fields = dict(post)
			#print('humm...', post)
			
			# environ.setdefault('QUERY_STRING', '')
			# multipart_headers = {'Content-Type': environ['CONTENT_TYPE']}
			# multipart_headers['Content-Length'] = environ['CONTENT_LENGTH']
			# multipart.parse_form(multipart_headers, environ['wsgi.input'], self.on_field, self.on_file)

	def on_field(self, field):
		self.fields[field.field_name] = field.value

	def on_file(self, file):
		self.files[file.field_name] = {'name': file.file_name, 'file_object': file.file_object}

	@property
	def GET(self):
		get_args = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
		return {k:v[0] for k,v in get_args.items()}

	@property
	def POST(self):
		return {k: v.value for k,v in self.fields.items()}

	@property
	def FILES(self):
		return {k.decode('utf-8'): v for k,v in self.files.items()}

	@property
	def method(self):
		return self._method

	# def set_coookie(self, key, value='', max_age=None, expires=None, 
	# 	path='/', secure=False, ):
	# 	"""
	# 		set cookies
	# 	"""
	# 	self.cookies[key] = value
	#	self.cookies[key]['httponly'] = True
