import re
import string
import uuid
from functools import lru_cache

from nimba.core.exceptions import ImproperlyRoute
from nimba.core.exceptions import ImproperlyMethodsConfig

class IntConverter:
    regex = '[0-9]+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)


class StringConverter:
    regex = '[^/]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class UUIDConverter:
    regex = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    def to_python(self, value):
        return uuid.UUID(value)

    def to_url(self, value):
        return str(value)


class SlugConverter(StringConverter):
    regex = '[-a-zA-Z0-9_]+'


class PathConverter(StringConverter):
    regex = '.+'

DEFAULT_CONVERTERS = {
    'int': IntConverter(),
    'path': PathConverter(),
    'slug': SlugConverter(),
    'str': StringConverter(),
    'uuid': UUIDConverter(),
}

@lru_cache(maxsize=None)
def get_converter(raw_converter):
    return DEFAULT_CONVERTERS[raw_converter]

def resolve_pattern(pattern, callback):
	original_route = pattern
	parts = ['^']
	converters = {}

	regex = r'<(?:(?P<converter>[^>:]+):)?(?P<parameter>[^>]+)>'
	url  = re.compile(regex, 0)
	while True:
		match = url.search(pattern)
		if not match:
			parts.append(re.escape(pattern))
			break
		parts.append(re.escape(pattern[:match.start()]))
		pattern = pattern[match.end():]
		parameter = match['parameter']
		if not parameter.isidentifier():
			raise ImproperlyRoute(f"[Error] - URL route '{pattern}' uses view name {callback} which isn't a valid")
		raw_converter = match['converter'] if match['converter'] else 'str'
		try:
			converter = get_converter(raw_converter)
		except Exception as e:
			raise ImproperlyRoute(f'[Error] - URL route {pattern} uses invalid converter {raw_converter}.')
		converters[parameter] = converter
		parts.append('(?P<' + parameter + '>' + converter.regex + ')')
	#add end parts and terun valid url
	parts.append('$')
	return ''.join(parts), converters


def check_pattern(pattern:str) -> None:
	if not isinstance(pattern, str):
		raise ImproperlyRoute(f'Invalid format URL {pattern}. The must be a string.')
	if not set(pattern).isdisjoint(string.whitespace):
		raise ImproperlyRoute(f'Format URL {pattern} pattern invalid, the must content white space')
	if not pattern.startswith(('/', '^/', '^\\/')):
		raise ImproperlyRoute(f'[Error] - Your URL pattern {pattern} has not a route beginning with a '/'. Add this')


def is_valid_method(methods:list) -> None:
	if not isinstance(methods, list) or len(methods) > 2 or len(methods) < 0:
		raise ImproperlyMethodsConfig('ErrorConfig : methods must be list and use the valid element GET or POST.')

	