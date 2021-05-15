import http.client
from wsgiref.headers import Headers

class Response:
	def __init__(self, response=None, status=200, charset='utf-8', content_type='text/html'):
		self.response = [] if response is None else response
		self.charset  = charset
		self.headers  = Headers()
		ctype         = f'{content_type}; charset={charset}'
		self.headers.add_header('content-type', ctype)
		self._status  = status
	
	@property
	def status(self):
		status_string = http.client.responses.get(self._status, 'UNKNOWN')
		return f'{self._status} {status_string}'
	
	def __iter__(self):
		for k in self.response:
			if isinstance(k, bytes):
				yield k
			else:
				yield k.encode(self.charset)
				