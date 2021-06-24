from framework.nimba.http import router
from framework.nimba.http import render

@router('/')
def home(request):
	return "hello, word!"

@router('/about')
def about(request):
	assert False
	return "About home"

@router('/articles')
def article(request):
	return "List articles, Merci"
