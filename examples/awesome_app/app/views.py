from nimba.http import router, render

@router('/')
def home(request):
    return render('awesome_app/home.html')


@router('/articles')
def home(request):
    return 'testing <h1>OK</h1>'
