def error_404(request, endpoint, path_available):
	print(f'404 Not Found {endpoint}')
	path_list = [
		f"('{route_name[1][2]}', {route_name[1][0].__name__})" for route_name in path_available.items()
	]
	contexts = {
		'page_name': endpoint,
		'route_error': True,
		'available_route': path_list,
		'request': request,
	}
	return 'errors/404.html', contexts, 404

def error_500(request, endpoint, e):
	print(f'{e}')
	contexts = {
		'page_name': endpoint,
		'error_in_view': True,
		'exceptions': e,
		'request': request,
	}
	return 'errors/500.html', contexts, 500

def error_401(request, endpoint, method, e):
	print(f'UnauthorizedError : Methods {method} Unauthorized')
	contexts = {
		'page_name': endpoint,
		'exceptions': e,
		'message': method
	}
	return 'errors/401.html', contexts, 401
