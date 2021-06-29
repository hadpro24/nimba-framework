from nimba.http import router

@router('/about')
def about(request):
	return "<h1> Hello, <h2> Welcom to my app page"
	