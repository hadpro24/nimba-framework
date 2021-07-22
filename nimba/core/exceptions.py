class ImproperlyRoute(Exception):
	pass

class PathNotFound(Exception):
	""" Path Not found """
	pass

class ImproperlyMethodsConfig(Exception):
	pass


class AppNameIncorrect(Exception):
	pass

class CommandError(Exception):
	pass

class NoReverseFound(Exception):
	pass
	